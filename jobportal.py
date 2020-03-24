import time
import requests
from bs4 import BeautifulSoup
import csv
import os

def session():
    with requests.Session() as se:
        se.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
        return se

pages = [10, 20, 30, 40]

with open('E:/data_scientist.csv', 'a', encoding='utf-8', newline='') as f_output:
    csv_print = csv.writer(f_output)

    file_is_empty = os.stat('E:/data_scientist.csv').st_size == 0
    if file_is_empty:
        csv_print.writerow(['Job_Title', 'Company', 'Location', 'Summary', 'Salary'])
    session = session()

    for page in pages:

        source = session.get('https://www.indeed.com.pk/jobs?q=data+scientist&l=Pakistan&start={}'.format(page)).text
        soup = BeautifulSoup(source, 'lxml')

        for jobs in soup.find_all(class_='result'):

            try:
                title = jobs.find('div', class_='title').text.strip()
            except Exception as e:
                title = None

            try:
                company = jobs.find('span', class_='company').text.strip()
            except Exception as e:
                company = None

            try:
                location = jobs.find('span', class_='location').text.strip()
            except Exception as e:
                location = None

            try:
                summary = jobs.find('div', class_='summary').text.strip()
            except Exception as e:
                summary = None

            try:
                salary = jobs.find('span', class_='no-wrap').text.strip()
            except Exception as e:
                salary = None

            csv_print.writerow([title, company, location, summary, salary])
            print('........................')
            time.sleep(0.5)