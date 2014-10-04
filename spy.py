from bs4 import BeautifulSoup
import urllib.request
import re
import json
import csv
import sys

class Country:
  name = ""
  borders = []
  prob = 0
  pre_prob = 0
  def __init__(self, name):
    self.name = name
  def __str__(self):
    return name
 
    
def getSubCountries(name):
  countries = []
  temp = []
  with open("countries.json") as f:
    data = json.loads(f.read())
    for line in data:
      if line["cca3"] == name:
        temp = line["borders"]
        countries = temp
#out of continent
      if "PAN" in countries:
        countries.remove("PAN")
  return countries

def getCountries():
  url = "http://en.wikipedia.org/wiki/List_of_South_American_countries_by_population"
  req = urllib.request.urlopen(url)
  page = req.read()
  scraping = BeautifulSoup(page)
  table = scraping.findAll("table")[1]
  rows = table.findAll("tr")
  del rows[-1]
  countries = []
  for tr in rows[1:]:
    countries.append(tr.findAll("a")[0].text)
  temp = []
  with open("countries.json") as f:
    data = json.loads(f.read())
    for line in data:
      for country in countries:
        if country == line["name"]:
          if line["cca3"] != "FLK":
            temp.append(line["cca3"])
  return temp



countryList = []
print("------------------------------")
print("Initialization countries")
for name in getCountries():
  print(name)
  countryList.append(Country(name))

mp = {}
for i in range(0, 13):
  mp[countryList[i].name] = i
print("------------------------------")
print("Adding borders")

for country in countryList:
  country.borders = getSubCountries(country.name)

#init start country
for country in countryList:
  if country.name == "CHL":
    country.pre_prob = 1

#counting probability after 13 days of running
for i in range(0, 13):
  for country in countryList:
    country.prob = 0
  for k in range(0, len(countryList)):
    for border in countryList[k].borders:
      countryList[mp[border]].prob += countryList[k].pre_prob/len(countryList[k].borders)
  for country in countryList:
    country.pre_prob = country.prob

probList = []
sum = 0
for country in countryList:
  sum += country.prob
  probList.append(country.prob)
  print(country.prob)
print("Total probability: " + str(sum))

print("------------------------------")
for country in countryList:
  if max(probList) == country.prob:
    print("It's " + country.name + " with " + str(max(probList)) + " probability!!!")
