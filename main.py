import math
import multiprocessing
import re
import threading
from multiprocessing import Queue, cpu_count
import time
from datetime import datetime
from datetime import timedelta
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import csgostats_scraper

#USER SPECIFIC
players_dict = {
    "EliGE": "https://csgostats.gg/player/76561198066693739",
    "nitr0": "https://csgostats.gg/player/76561197995889730",
    #.....
}

#Uploads dataframe to google sheets
def upload_to_google_sheets(players_df):
    current_time = datetime.today()
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    ###USER SPECIFIC###
    credentials = Credentials.from_service_account_file('/path/to/json/credentials/', scopes=scopes)

    gc = gspread.authorize(credentials)

    # open a google sheet
    gs = gc.open_by_key('google_sheets_id')
    # select a work sheet from its name
    worksheet1 = gs.worksheet('worksheet_name')
    set_with_dataframe(worksheet=worksheet1, dataframe=players_df, include_index=True, include_column_header = True, resize = True)
    worksheet1.update('A1', str(current_time))

# Used to get unix timestamp X months ago. Unix timestmap start and end time are used for a range of data on csgostats.gg
def get_unix_timestamp_x_months_ago(months):
    current_date = datetime.now()
    three_months_ago = current_date - timedelta(months * 30)
    timestamp = int(time.mktime(three_months_ago.timetuple()))

    return timestamp

# Used to add start and end time to URLs
def add_date_range_to_url(players_dict, date_start, date_end):
    for player in players_dict:
        players_dict[player] = f'{players_dict[player]}?type=comp&date_start={date_start}&date_end={date_end}'

    return players_dict

# Creates hyperlink used for google sheet
def create_hyperlink(player_dict_entry):
    hyperlink = f'=HYPERLINK("{players_dict[player_dict_entry]}", "{player_dict_entry}")'

    return hyperlink

# Obtains number of chunks
def get_num_chunks(number_of_cores):
    chunks = math.ceil(len(players_dict) / number_of_cores)

    return chunks

# Function used to gather all player info
def get_all_player_info_sequential(players_dictionary, find_win_percentage_regex, find_kill_death_ratio_regex, find_hltv_rating_regex, find_headshot_percentage_regex, find_adr_regex):
    # List of tuples that will be used to store all player statistics
    all_player_info = []

    for player in players_dictionary:
        # Creating hyperlink for googlesheet player name
        hyperlink = create_hyperlink(player)
        profile_info = csgostats_scraper.scrape_profile(players_dictionary[player], hyperlink)
        player_info_scraped = csgostats_scraper.get_stats(profile_info[0],
                                                          profile_info[1],
                                                          profile_info[2],
                                                          profile_info[3],
                                                          find_win_percentage_regex,
                                                          find_kill_death_ratio_regex,
                                                          find_hltv_rating_regex,
                                                          find_headshot_percentage_regex,
                                                          find_adr_regex)
        all_player_info.append(player_info_scraped)

    return all_player_info

def get_all_player_info_parallel(players_dictionary, option, find_win_percentage_regex, find_kill_death_ratio_regex, find_hltv_rating_regex, find_headshot_percentage_regex, find_adr_regex):
    # List of tuples that will be used to store all player statistics
    all_player_info = []

    tasks = []
    queue = Queue()
    # Getting number of cpu cores - 1
    num_threads = cpu_count() - 1
    # Chunks obtained by dividing number of player profiles by the number of cores
    chunks = get_num_chunks(num_threads)
    chunk_start = 0
    chunk_end = num_threads
    # Dividing up the work by num_threads for each chunk
    for chunk in range(0, chunks):
        chunk_start = chunk * num_threads
        # If not last chunk
        if chunk + 1 != chunks:
            chunk_end = (chunk + 1) * num_threads
        # If last chunk set end chunk index to be the real last element
        else:
            chunk_end = chunk_start + (len(players_dictionary) - num_threads)
        # Using selenium to scrape the necessary data from csgostats
        # Multithreading
        if option == "mt":
            for player in sorted(players_dictionary)[chunk_start:chunk_end]:
                hyperlink = create_hyperlink(player)
                task = threading.Thread(target=csgostats_scraper.scrape_profile, args=(players_dictionary[player], hyperlink, queue,))
                task.start()
                tasks.append(task)
        # Multiprocessing
        elif option == "mp":
            for player in sorted(players_dictionary)[chunk_start:chunk_end]:
                hyperlink = create_hyperlink(player)
                task = multiprocessing.Process(target=csgostats_scraper.scrape_profile, args=(players_dictionary[player], hyperlink, queue,))
                task.start()
                tasks.append(task)

        # Waits for all tasks to end before moving on, all scraping done
        for task in tasks:
            task.join()

    # Using regular expression to extract wanted data from each data_tuple in the queue
    original_queue_size = queue.qsize()
    for i in range(0, original_queue_size):
        player_info = queue.get()
        player_info_scraped = csgostats_scraper.get_stats(player_info[0],
                                                          player_info[1],
                                                          player_info[2],
                                                          player_info[3],
                                                          find_win_percentage_regex,
                                                          find_kill_death_ratio_regex,
                                                          find_hltv_rating_regex,
                                                          find_headshot_percentage_regex,
                                                          find_adr_regex)
        all_player_info.append(player_info_scraped)

    return all_player_info

if __name__ == '__main__':
    # Variable used to create the start date. 1 month is considered 30 days
    # Set to 0 if you want alltime stats with no date range.
    months_ago = 3

    # User has entered a specified range, therefore URLs will be modified to include this range
    if months_ago is not None:
        end_time = int(time.time())
        start_time = get_unix_timestamp_x_months_ago(months_ago)
        players_dictionary = add_date_range_to_url(players_dict, start_time, end_time)

    # Variable used to enable multiprocessing
    # option[0] = Sequential. This is DEFAULT since it should work on all machines, will likely be slowest
    # option[1] = Multithreading. This should work better on Linux machines
    # option[2] = Multiprocessing. This should work better on Windows machines
    # NOTE: Multithreading and Multiprogramming could run into issues dependent on system and may not be the best choice depending on number of cores/threads.
    option = ['seq', 'mt', 'mp']
    selected_option = option[2]

    # Pre compiling regular expressions
    find_win_percentage_regex = re.compile(r"Win:(.*?) KPD:")
    find_kill_death_ratio_regex = re.compile(r'KPD:(.*?) Rating')
    find_hltv_rating_regex = re.compile(r'Rating:(.*?) HS:')
    find_headshot_percentage_regex = re.compile(r'HS:(.*?) ADR:')
    find_adr_regex = re.compile(r'ADR:(.*?)\\')

    # If user selected option 0, use sequential method
    if selected_option == 'seq':
        all_player_info = get_all_player_info_sequential(players_dict,
                                                         find_win_percentage_regex,
                                                         find_kill_death_ratio_regex,
                                                         find_hltv_rating_regex,
                                                         find_headshot_percentage_regex,
                                                         find_adr_regex)

    # Else use either multithreading or multiprocessing approach
    else:
        all_player_info = get_all_player_info_parallel(players_dict, selected_option,
                                                       find_win_percentage_regex,
                                                       find_kill_death_ratio_regex,
                                                       find_hltv_rating_regex,
                                                       find_headshot_percentage_regex,
                                                       find_adr_regex)

    # Getting the 1st column for insert onto google sheet from list of tuples
    index = [player_info[0] for player_info in all_player_info]
    # Rest of the columns
    all_player_info_list = [player_info[1:] for player_info in all_player_info]
    players_df = pd.DataFrame(all_player_info_list, index=index, columns=['HLTV Rating', 'KDR', 'ADR', 'Win %', 'Headshot %', 'Total Games Played', 'Rank'])
    upload_to_google_sheets(players_df.sort_values('HLTV Rating', ascending=False))
