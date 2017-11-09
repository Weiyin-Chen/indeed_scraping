from bs4 import BeautifulSoup
import urllib
import re
import collections
from time import sleep


# get lists of job title and companies from a single webpage
def get_title_company(url):
    try:
        html = urllib.request.urlopen(url).read()
    except:
        print('invalid url!')
        return
    soup = BeautifulSoup(html, "lxml")
    titles = soup.find_all('a', {'data-tn-element': 'jobTitle'})  # find all job title tags
    companies = soup.find_all('span', {'class': 'company'})  # find all company tags
    company_list, title_list = [], []  # they are used to store title and company strings

    #  remove sponsor jobs
    for title in titles:
        if title['class'] == ['turnstileLink']:
            title_list.append(title.get_text())
    for company in companies:
        if company.parent['class'] != ['sjcl']:
            company_list.append(company.get_text("|", strip=True))

    return {'titles': title_list, 'companies': company_list, 'soup': soup}


# help function to update result list
def update_result(final, temp):
    final['titles'].extend(temp['titles'])
    final['companies'].extend(temp['companies'])
    next_page = temp['soup'].find("span", {"class": "np"}, text=re.compile("Next"))
    return next_page


# core function
def indeed_scraping(query, city, province):
    base_url = 'https://www.indeed.ca'
    curr_url = base_url + '/jobs?q=' + query + '&l=' + city + '%2C+' + province
    result = {'titles': [], 'companies': []}
    temp_result = get_title_company(curr_url)
    next_page = update_result(result, temp_result)
    while next_page is not None:
        sleep(1)
        curr_url = base_url + next_page.parent.parent.get('href')
        temp_result = get_title_company(curr_url)
        next_page = update_result(result, temp_result)
    return result


a = indeed_scraping('python', 'Calgary', 'AB')
titles_stat = collections.Counter(a['titles'])
companies_stat = collections.Counter(a['companies'])
print(titles_stat)
print('\n')
print(companies_stat)
print('\n')

# debug part
# print(len(a['titles']))
# print('\n')
# for b in a['titles']:
#     print(b)
# print('\n')
# print(len(a['companies']))
# print('\n')
# for b in a['companies']:
#     print(b)
