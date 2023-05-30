# csgostats_scraper
Utilizes selenium to scrape a few statistics from csgostats.gg

# Project Goal
I created this script to compile a list of friends csgo stats utilizing Selenium on csgostats.gg and exported the data to a google sheet which can be viewed by all of us to talk trash and compare not so meaningful stats.

# Installation/Setup

Firstly the user needs to create their own player dictionary and input the players and their csgostats.gg profile urls on line 11 of main.py. The following format should be used:

players_dict = {
  "EliGE": "https://csgostats.gg/player/76561198066693739",
  "nitr0": "https://csgostats.gg/player/76561197995889730",
  .....
}

## Google Service Account and Google Sheets Setup
Next the user will need to create a project and service account with Google. I followed [this article](https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0) (NOTE: pydrive package not required). After getting the JSON credentials place it in the program root directory. Next create the google sheet and obtain the sheet id from the url. The sheet id can be found after the "gid" in the sheet URL.

## Downloading Chromedriver
Selenium WebDriver uses the ChromeDriver to communicate test scripts with Google Chrome. This will be requiref if using Chrome, as I did. First check the version of google chrome you are using by going to: chrome://version/ and seeing the number at the top. Then go to the [chromedrtiver download page](https://chromedriver.chromium.org/downloads) and download the driver for the approrpiate Chrome version. Once downloaded input the directory into the 'driver_path' variable on line 6 of csgostats_scraper.py

# Results
![csgo-stats](https://github.com/ShayneEvans/csgostats_scraper/assets/70344759/af50f90a-4c17-4f94-b23c-abce51a35d9e)

What the google sheet should look like after the script is finished executing. This is a sorted list (by HLTV rating) of all the players entered into the dictionary. Included in A1 is the timestamp at which the sheet was most recently updated. The blurred image part on the left is a hyperlink to the csgostats.gg profile page of each of the players.

# Future Improvements
- ~~Make it Linux friendly.
  - 5/30/23: Added in headless argument and reinstalled chromium and chromedriver with the following commands:
    - sudo apt-get install chromium-browser
    - sudo apt-get install chromium-chromedriver
  - Default path for chromedriver is: /usr/lib/chromium-browser/chromedriver
  - Program runs a tad bit slower on my Ubuntu Server on Raspberry Pi 3, around 4-5 minutes but now it can be autoamted more easily!
- Optimize the program. I looked into trying to make the use of selenium faster. At the time of upload it takes anywhere from 5-10 seconds per profile to scrape the information, not sure if this is normal or not. Took around 2 minutes for script to run, which is still a lot more fast than doing it manually at the very least.
