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


# Future Improvements
- Make it Linux friendly. I attempted to set this script up in an Ubuntu 22.10 environment on my Raspberry Pi 3 but ran into many issues when trying to use selenium and chromdriver/chromium. 
- Optimize the program. I looked into trying to make the use of selenium faster. At the time of upload it takes anywhere from 5-10 seconds per profile to scrape the information, not sure if this is normal or not. Took around 2 minutes for script to run, which is still a lot more fast than doing it manually at the very least.
