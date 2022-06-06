import requests
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.parser import parse
import json
import xmltodict

def get_details(date):
    print("")
    new_list = []
    with open("adelaide_iss.xml") as fd:
        doc = xmltodict.parse(fd.read())

    for title in doc['rss']['channel']['item']:
        if title['title'].startswith(date):
            shit_list = title['description'].splitlines()
            for thing in shit_list:
                thing = thing.replace("<br/>", "")
                thing = thing.replace("\t" , "")
                new_list.append(thing)
            return new_list


def check_weather(date):
    f = open("adelaide_weather.json", "r")
    y = json.loads(f.read())
    for i in range(0, len(y["days"])):
        if date == y["days"][i]["datetime"]:
            tester = str(y["days"][i]["conditions"])
            return tester.lower()

def weather_dates(file):
    f = open(file, "r")
    if f:
        i = 0
        y = json.loads(f.read())
        weather_dates = []
        while i < len(y["days"]):
            weather_dates.append(y["days"][i]["datetime"])
            i += 1
    return weather_dates

def iss_dates(file):
    new_list = []
    with open(file) as fd:
        doc = xmltodict.parse(fd.read())

    for title in doc['rss']['channel']['item']:
        i =  0
        date = title['description'].splitlines()
        list = []
        while i < len(date):
            string = date[i].replace("<br/>", "")
            string = string.replace("\t" , "")
            list.append(string)
            test = list[0].split()[2:]
            test = " ".join(test)
            format_date = parse(test)
            format_date = str(format_date).split()[:1]
            format_date = " ".join(format_date)
            i += 1
        new_list.append(format_date)
    return new_list

def compare_dates(list1, list2):
    for dates in list1:
        if dates not in list2:
            print("\033[1;31mISS is not coming past Adelaide on: ", dates, "\033[1;0m")
            print("")
        else:
            print("ISS is coming past Adelaide on: ", dates)
            weather_description = check_weather(dates)
            print("Weather for this day is: ", weather_description)
            matches = ["rain", "overcast", "cloud"]
            if any(x in weather_description for x in matches):
                print("\033[1;31mISS is not going to be visible due to bad weather\033[1;0m")
                end_print = get_details(dates)
                # for entry in end_print:
                #     print("\033[1;31m", entry, "\033[1;0m")
                # print("")
            else:
                print("Perfect weather to watch the ISS - Here are some more details:")
                end_print = get_details(dates)
                for entry in end_print:
                    print("\033[1;30m", entry, "\033[1;0m")
                print("")
                print("Booking this one in your calendar to remind you...")

# ISS information provided via
sighting_url = "https://spotthestation.nasa.gov/sightings/xml_files/Australia_South_Australia_Adelaide.xml"

# Get calculation of dates to check
current_date = date.today()
current_date_5 = date.today() + timedelta(days=5)
print("")
print("\033[1;33mChecking for Visible ISS in timeframe: ", current_date, "-" , current_date_5, "\033[1;0m")


file_weather = open("adelaide_weather.json", "w")
file_iss = open("adelaide_iss.xml", "w")
weather = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Adelaide/" + str(current_date) + "/" + str(current_date_5) + "?key=<GENERATEKEY>"
print("")

# API Call
api_call_weather = requests.get(weather)
api_call_iss = requests.get(sighting_url)

file_weather.write(api_call_weather.text)
file_weather.close()
file_iss.write(api_call_iss.text)
file_iss.close()

iss = iss_dates("adelaide_iss.xml")
weather = weather_dates("adelaide_weather.json")
compare_dates(weather, iss)
