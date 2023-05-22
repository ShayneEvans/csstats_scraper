from selenium import webdriver
from selenium.webdriver.common.by import By
import re

def scrape_profile(player_profile):
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    url = player_profile
    driver.get(url)
    meta_tag = driver.find_element(By.XPATH,"//meta[@property='og:description']")
    meta_content = meta_tag.get_attribute("content")
    driver.quit()
    return meta_content

def get_stats(meta_content, find_win_percentage_regex, find_kill_death_ratio_regex, find_hltv_rating_regex, find_headshot_percentage_regex, find_adr_regex):
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

        return (hltv_rating, kill_death_ratio, adr, win_percentage, headshot_percentage)