import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

#Method to get the data of features
def get_data(obj):
    building_name = obj.findAll("h5", {"class": "room__location--title"})
    building_name = building_name[0].text
    room_name = obj.findAll("h1", {"class": "room__title"})
    room_name = room_name[0].text
    location = obj.findAll("div", {"class": "address"})
    location = location[0].text.replace("\n", "")
    room_features = obj.findAll("div", {"class": "room__features"})
    features = []
    room_features = room_features[0].findAll('p')
    for feature in room_features:
        features.append(feature.text)
    capacity_of_persons = obj.findAll("div", {"class": "room__icons hide-for-medium"})[0].find('li').text.replace(" ",
                                                                                                                  "")
    price = obj.find('span', {'class': 'room__sidebar--rate-base'}).text
    data = [building_name, room_name, location, features, capacity_of_persons, price]
    return data

#Method to get the links of hostels/buildings
def get_hostels(se, location):
    url = location
    ss = se.get(url)
    obj = BeautifulSoup(ss.content, 'lxml')
    data = obj.findAll("div", {"class": "card__room"})
    records = []
    for result in data:
        anch = result.find('a', href=re.compile("(https://atira.com/room/)+([A-Za-z0-9_:{}()])+"))
        records.append(anch)
    hostels = []
    for i in records:
        hostels.append(i['href'])
    return hostels

#Method to get the links of locations
def get_locations(obj):
    data = obj.findAll("div", {"class": "row archive__cards-container"})
    anch = data[0].findAll('a', href=re.compile("(https://atira.com/location/)+([A-Za-z0-9_:{}()])+"))
    locations = []
    for i in anch:
        locations.append(i['href'])
    return locations

#Method to create a session
def session():
    with requests.Session() as se:
        se.headers = {
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
        return se

#Method to scrape the web data
def Scrape(url):
    se = session()
    ss = se.get(url)
    obj = BeautifulSoup(ss.content, 'lxml')
    locations = get_locations(obj)
    time.sleep(3)
    driver = webdriver.Chrome()
    df = pd.DataFrame(columns=['building_name', 'room_name', 'location', 'features', 'capacity_of_persons', 'price'])
    for location in locations:
        hostels = get_hostels(se, location)
        time.sleep(3)
        for hostel in hostels:
            driver.get(hostel)
            res = driver.execute_script("return document.documentElement.outerHTML")
            #time.sleep(10)
            #driver.close()
            obj = BeautifulSoup(res, 'lxml')
            data = get_data(obj)
            df = df.append({'building_name': data[0],
                            'room_name': data[1],
                            'location': data[2],
                            'features': data[3],
                            'capacity_of_persons': data[4],
                            'price': data[5]},
                           ignore_index=True)
            time.sleep(3)
    return df

#Main method
def main():
    url = 'https://atira.com/location/'
    df = Scrape(url)
    export_csv = df.to_csv(r'Atira_dataset.csv', index=None, header=True)

if __name__ == '__main__':
    main()