from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
op = webdriver.ChromeOptions()
op.add_argument("--headless=new")

#Uses selenium to obtain stats from csgostats.gg
def scrape_profile(player_profile):
    chromedriver_path = '/usr/bin/chromedriver'
    driver = webdriver.Chrome(service=Service(chromedriver_path), options = op)
    url = player_profile
    driver.get(url)
    #Getting the player stats meta tag
    meta_tag = driver.find_element(By.XPATH,"//meta[@property='og:description']")
    meta_content = meta_tag.get_attribute("content")
    #Getting the total number of games layed
    total_stat_elements = driver.find_elements(By.CLASS_NAME, "total-stat")
    total_games = total_stat_elements[0].find_element(By.CLASS_NAME, "total-value").text
    
    driver.quit()
    return meta_content, total_games

#Using regular expressions to exract each individual stat into a variable which is returned in tuple format
def get_stats(meta_content, total_games, find_win_percentage_regex, find_kill_death_ratio_regex, find_hltv_rating_regex, find_headshot_percentage_regex, find_adr_regex):
    if meta_content is not None:
        find_win_percentage = re.search(find_win_percentage_regex, str(meta_content))
        find_kill_death_ratio = re.search(find_kill_death_ratio_regex, str(meta_content))
        find_hltv_rating = re.search(find_hltv_rating_regex, str(meta_content))
        find_headshot_percentage = re.search(find_headshot_percentage_regex, str(meta_content))
        find_adr = re.search(find_adr_regex, str(meta_content))
        win_percentage = find_win_percentage.group(1)
        kill_death_ratio = find_kill_death_ratio.group(1)
        hltv_rating = find_hltv_rating.group(1)
        headshot_percentage = find_headshot_percentage.group(1)
        adr = find_adr.group(1)

        return (hltv_rating, kill_death_ratio, adr, win_percentage, headshot_percentage, total_games)
