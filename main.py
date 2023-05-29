from datetime import datetime
import csgostats_scraper
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import re
import time

#USER SPECIFIC
players_dict = {
    "EliGE": "https://csgostats.gg/player/76561198066693739",
    "nitr0": "https://csgostats.gg/player/76561197995889730",
    #.....
}

#Used to get unix timestamp X months ago. Unix timestmap start and end time are used for a range of data on csgostats.gg
def get_unix_timestamp_x_months_ago(months):
    current_date = datetime.now()
    three_months_ago = current_date - timedelta(months * 30)
    timestamp = int(time.mktime(three_months_ago.timetuple()))
    return timestamp

#Used to add start and end time to URLs
def add_date_range_to_url(players_dict, date_start, date_end):
    for player in players_dict:
        players_dict[player] = f'{players_dict[player]}?type=comp&date_start={date_start}&date_end={date_end}'

    return players_dict

#Creates hyperlinks for google sheets 1st column
def create_hyperlinks(players_dict):
    hyperlinks_list = []
    for i in range(0, len(players_dict)):
        hyperlinks_list.append(f'=HYPERLINK("{list(players_dict.values())[i]}", "{list(players_dict.keys())[i]}")')

    return hyperlinks_list

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

if __name__ == '__main__':
    #Variable used to create the start date. 1 month is considered 30 days
    #Set to 0 if you want all time stats with no date range.
    months_ago = 3

    #User has entered a specified number of months, calculate unix start time and change URLs
    if months_ago != 0:
        end_time = int(time.time())
        start_time = get_unix_timestamp_x_months_ago(months_ago)
        players_dict = add_date_range_to_url(players_dict, start_time, end_time)

    hyperlinks = create_hyperlinks(players_dict)
    all_player_info = []

    find_win_percentage_regex = re.compile(r"Win:(.*?) KPD:")
    find_kill_death_ratio_regex = re.compile(r'KPD:(.*?) Rating')
    find_hltv_rating_regex = re.compile(r'Rating:(.*?) HS:')
    find_headshot_percentage_regex = re.compile(r'HS:(.*?) ADR:')
    find_adr_regex = re.compile(r'ADR:(.*?)\\')

    #Getting all of the updated player info
    for player in players_dict:
        profile_meta_data, total_games = csgostats_scraper.scrape_profile(players_dict[player])
        player_info = csgostats_scraper.get_stats(profile_meta_data,
                                                  total_games,
                                                  find_win_percentage_regex,
                                                  find_kill_death_ratio_regex,
                                                  find_hltv_rating_regex,
                                                  find_headshot_percentage_regex,
                                                  find_adr_regex)
        all_player_info.append(player_info)

    players_df = pd.DataFrame(all_player_info, index = hyperlinks ,columns=['HLTV Rating', 'KDR', 'ADR', 'Win %', 'Headshot %', 'Total Games Played'])
    upload_to_google_sheets(players_df.sort_values('HLTV Rating', ascending=False))
