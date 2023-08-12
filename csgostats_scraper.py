from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
from selenium.common.exceptions import NoSuchElementException, JavascriptException
op = webdriver.ChromeOptions()
op.add_argument("--headless=new")

#Uses selenium to obtain stats from csgostats.gg
def scrape_profile(player_profile, hyperlink, queue = None):
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(options = op, executable_path=driver_path)
    url = player_profile
    driver.get(url)

    try:
        meta_tag = driver.find_element(By.XPATH,"//meta[@property='og:description']")
        meta_content = meta_tag.get_attribute("content")
    
        # Find the <div> elements with class="total-stat"
        total_stat_elements = driver.find_elements(By.CLASS_NAME, "total-stat")
        total_games = total_stat_elements[0].find_element(By.CLASS_NAME, "total-value").text
    
        #Find the <div> elements with class="player-ranks"
        try:
            rank_img_url = driver.execute_script("return document.querySelector('div.player-ranks img').getAttribute('src')")
            #Format used to insert image to cell and resize to fit the cell
            rank_img_cell_txt = f"=IMAGE(\"{rank_img_url}\", 2)"
        except JavascriptException:
            rank_img_cell-txt = 'N/A'
    
        driver.quit()
    
        #If not using multiprocessing
        if queue is None:
            return (hyperlink, meta_content, total_games, rank_img_cell_txt)
        else:
            queue.put((hyperlink, meta_content, total_games, rank_img_cell_txt))
    except NoSuchElementException:
            return (hyperlink, Noone, None, None)

def get_stats(user_profile_hyper_link, meta_content, total_games, rank_image_url, find_win_percentage_regex, find_kill_death_ratio_regex, find_hltv_rating_regex, find_headshot_percentage_regex, find_adr_regex):
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

        return (user_profile_hyper_link, hltv_rating, kill_death_ratio, adr, win_percentage, headshot_percentage, total_games, rank_image_url)
    else:
        return (user_profile_hyper_link, '0', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'NOG') 
