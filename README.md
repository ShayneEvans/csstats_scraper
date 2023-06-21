# csgostats_scraper - Compare Your Stats With Friends in Minutes!
Utilizes selenium to scrape a stats from csgostats.gg with customizable start and end date parameters and display them to a google sheet.

# Project Goal
I created this script to compile a list of friends csgo stats utilizing Selenium on csgostats.gg and exported the data to a google sheet which can be viewed by all of us to talk trash and compare not so meaningful stats.  

![csgostats](https://github.com/ShayneEvans/csgostats_scraper/assets/70344759/e7ae3ea1-cbd2-4cec-94f0-d5d1045270cc)  

What the google sheet should look like after the script is finished executing. This is a sorted list (by HLTV rating) of all the players entered into the dictionary. Included in A1 is the timestamp at which the sheet was most recently updated. The blurred image part on the left is a hyperlink to the csgostats.gg profile page of each of the players.

# Installation/Setup

Firstly the user needs to create their own player dictionary and input the players and their csgostats.gg profile urls on line 11 of main.py. The following format should be used:

```python
players_dict = {
  "EliGE": "https://csgostats.gg/player/76561198066693739",
  "nitr0": "https://csgostats.gg/player/76561197995889730",
  #....
}
```

## Google Service Account and Google Sheets Setup
Next the user will need to create a project and service account with Google. I followed [this article](https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0) (NOTE: pydrive package not required). After getting the JSON credentials place it in the program root directory. Next create the google sheet and obtain the sheet id from the url. The sheet id can be found after the "gid" in the sheet URL.

### Windows
Selenium WebDriver uses the ChromeDriver to communicate test scripts with Google Chrome. This will be required if using Chrome, as I did. First check the version of google chrome you are using by going to: chrome://version/ and seeing the number at the top. Then go to the [chromedrtiver download page](https://chromedriver.chromium.org/downloads) and download the driver for the approrpiate Chrome version. Once downloaded input the directory into the 'chromedriver_path' variable on line 10 of csgostats_scraper.py

### Linux
Run the following commands:
- sudo apt-get install chromium-browser
- sudo apt-get install chromium-chromedriver

Once downloading the chromedriver input the directory into the 'chromedriver_path' variable on line 10 of csgostats_scraper.py. The default path should be: 
/usr/lib/chromium-browser/chromedriver

# Future Improvements
- ~~Make it Linux friendly.~~
  - 5/30/23: Added in headless argument and reinstalled chromium and chromedriver with the following commands:
    - sudo apt-get install chromium-browser
    - sudo apt-get install chromium-chromedriver
  - Default path (Linux) for chromedriver is: /usr/lib/chromium-browser/chromedriver, but I found /usr/bin/chromedriver to work better (found with where chromedriver command)
  - Program runs a tad bit slower on my Ubuntu Server on Raspberry Pi 3, around 4-5 minutes but now it can be autoamted more easily!
- ~~Optimize the program.~~
  - 6/21/23: Added options for multiprocessing and multithreading from within the script. Toggeable by changing the "option_selected" variable in main.py. Options are:
    - Sequential (seq)
    - Multithreading (mt)
    - Multiprocessing (mp)
  - Tested on my Windows machine and is with utilization of 15 threads the program executes ~30 seconds with 25 users. Lacked hardware for testing parallel programming approaches on Linux so testing still need to be done there.

# Automation (LINUX)
I automate the program by using a crontab on Ubuntu. The following works for me:
0 * * * * . $HOME/.profile; cd /path/to/program/directory && xvfb-run --auto-servernum path/to/python3 /path/to/main.py

0 * * * *   
This means that the script will be executed at minute 0 of every hour of the day. To get exactly what you want I would reccomend using [crontab guru](https://crontab.guru/).  

. $HOME/.profile;  
This is used to execute the contents of .profile, this is important if using enviornment variables, ignore if not.  

cd /path/to/program/directory && xvfb-run --autoservernum path/to/python3 /path/to/main.py  
This first changes the directory to the program folder and then runs xvfb-run to set up ap virtual server to work as a 'screen' for selenium. This is important if using the script in a headless enviornment such as a terminal. The script would not run through crontab without this because Selenium needed a graphical interface even though it was being run in headless mode. With xvfb-run --autoservernum this problem was resolved. Lastly the absolute path of python and main.py are used to execute the script.
