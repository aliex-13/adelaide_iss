import requests
from datetime import timedelta
from datetime import date
from dateutil.parser import parse
import json
import xmltodict
from email.message import EmailMessage
import smtplib

def email_alert(subject, body, to):
    # This is how our email alerting works. Replace some fields to make it work for you.
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "email@address.com" #FILL ME IN
    msg['from'] = user
    password = "app password" #FILL ME IN.
    #########################################
    #You cannot use normal password for this due to gmail restrictions#
    #To generate the password above - go to https://myaccount.google.com > Security Tab > Turn on 2FA > go Back to Security tab#
    #A new field should appear under 2FA called "App Passwords". Click there > Sign in again > Generate a new password (I chose Other(custom))#
    #Record the key that is provided#
    ######################################## 
    with open('iss_visible.txt', 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='txt', filename='iss_visible.txt')

    # If you aren't using gmail to send, may need to modify below.
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit

def get_details(date):
    # Gets the ISS details if it is passing by. Cleans up return list for display.
    new_list = []
    with open("adelaide_iss.xml") as fd:
        doc = xmltodict.parse(fd.read())

    for title in doc['rss']['channel']['item']:
        if title['title'].startswith(date):
            another_list = title['description'].splitlines()
            for thing in another_list:
                thing = thing.replace("<br/>", "")
                thing = thing.replace("\t" , "")
                new_list.append(thing)
            return new_list


def check_weather(date):
    # For a specific date, Checks the condition. Format's the condition string to check it later.
    f = open("adelaide_weather.json", "r")
    y = json.loads(f.read())
    for i in range(0, len(y["days"])):
        if date == y["days"][i]["datetime"]:
            tester = str(y["days"][i]["conditions"])
            return tester.lower()

def weather_dates(file):
    # Checks the Weather JSON file for dates. Format's the date so we can compare to ISS in compare_dates().
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
    # Checks the ISS XML file for dates. Format's the date so we can compare to weather in compare_dates().
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
    # Comparing weather dates to the ISS pass-by dates. This is the logic of the script.
    with open("iss_visible.txt", "a") as o:
        for dates in list1:
            if dates not in list2:
                o.write("ISS is not coming past Adelaide on: " + dates + "\n")
                o.write("\n")
            else:
                o.write("ISS is coming past Adelaide on: " + dates + "\n")
                weather_description = check_weather(dates)
                o.write("Weather for this day is: " + weather_description + "\n")
                matches = ["rain", "overcast", "cloud"]
                if any(x in weather_description for x in matches):
                    o.write("ISS is not going to be visible due to bad weather\n")
                    o.write("\n")
                    end_print = get_details(dates)
                else:
                    o.write("Perfect weather to watch the ISS - Here are some more details:\n")
                    o.write("\n")
                    end_print = get_details(dates)
                    for entry in end_print:
                        o.write(entry +"\n")

def main():
    # ISS information provided via
    sighting_url = "https://spotthestation.nasa.gov/sightings/xml_files/Australia_South_Australia_Adelaide.xml"

    # Get calculation of dates to check
    with open("iss_visible.txt", "w") as o:
        current_date = date.today()
        current_date_5 = date.today() + timedelta(days=5)
        o.write("Checking for ISS fly-by between the following dates: ")
        o.write(str(current_date))
        o.write(" - ")
        o.write(str(current_date_5))
        o.write("\n\n")


    file_weather = open("adelaide_weather.json", "w")
    file_iss = open("adelaide_iss.xml", "w")
    # For the weather URL below, my API subscription only gives me 5 day maximum forecast (this is free)
    # Please insert your API key at the end which should be available once you create an account.
    weather = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Adelaide/" + str(current_date) + "/" + str(current_date_5) + "?key=GENERATEKEY"

    # API Call
    api_call_weather = requests.get(weather)
    api_call_iss = requests.get(sighting_url)

    # This is how the files are automatically created when running the script
    file_weather.write(api_call_weather.text)
    file_weather.close()
    file_iss.write(api_call_iss.text)
    file_iss.close()

    iss = iss_dates("adelaide_iss.xml")
    weather = weather_dates("adelaide_weather.json")
    compare_dates(weather, iss)

if __name__ == '__main__':
    main()
    # Email is generated with the call below (sub, body and destination)
    email_alert("Aliex's ISS Checker", "Please check the attachment for details on the next ISS fly-by forecast!" , "destination@email.com")
