# adelaide_iss

I created this script to basically use information that is readily available to us from two separate sources, and combine the two.

Currently, the only way I am notified if the ISS is coming past Adelaide is through social media apps and news outlets letting us know. 
I also have to be lucky enough to pass by this article in time.

Another factor is weather.
Most websites that provide basic passing hours of the ISS in Adelaide don't actually provide information on whether it will be visible or not.

This tool will check for any sort of bad weather - Clouds, Overcast, Rain in a forecast of 5 days, and check this against the next couple weeks worth of ISS passes.


## Things I didn't do

- Wasn't able to narrow down in specific ISS time passing + Weather at that specific time. This tool checks the weather for the day across the board.
(Could be a next iteration).

- Notifications are not complete yet.. Struggled to find ICS creation + attendee tools. But that is going to be another iteration.

- Will be run as a cronjob.


## Things you will need to do

- You will need to generate an API key at https://weather.visualcrossing.com and replace <GENERATE KEY> in the "check_iss_clean.py" script.
- This will allow you to get relevant information for the script to run and store XML/JSON files which have information.
 

  
 
