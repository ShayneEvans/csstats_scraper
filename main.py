from datetime import datetime
import csgostats_scraper
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import re
import os

#USER SPECIFIC
players_dict = {
    "EliGE": "https://csgostats.gg/player/76561198066693739",
    "nitr0": "https://csgostats.gg/player/76561197995889730",
    #.....
}

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
    gs = gc.open_by_key(os.environ.get('google_sheets_id'))
    # select a work sheet from its name
    worksheet1 = gs.worksheet('Stats')
    set_with_dataframe(worksheet=worksheet1, dataframe=players_df, include_index=True, include_column_header = True, resize = True)
    worksheet1.update('A1', str(current_time))

if __name__ == '__main__':
    hyperlinks = create_hyperlinks(players_dict)
    all_player_info = []

    find_win_percentage_regex = re.compile(r"Win:(.*?) KPD:")
    find_kill_death_ratio_regex = re.compile(r'KPD:(.*?) Rating')
    find_hltv_rating_regex = re.compile(r'Rating:(.*?) HS:')
    find_headshot_percentage_regex = re.compile(r'HS:(.*?) ADR:')
    find_adr_regex = re.compile(r'ADR:(.*?)\\')

    for player in players_dict:
        profile_meta_data = csgostats_scraper.scrape_profile(players_dict[player])
        player_info = csgostats_scraper.get_stats(profile_meta_data,
                                                  find_win_percentage_regex,
                                                  find_kill_death_ratio_regex,
                                                  find_hltv_rating_regex,
                                                  find_headshot_percentage_regex,
                                                  find_adr_regex)
        all_player_info.append(player_info)

    players_df = pd.DataFrame(all_player_info, index = hyperlinks ,columns=['HLTV Rating', 'KDR', 'ADR', 'Win %', 'Headshot %'])
    upload_to_google_sheets(players_df.sort_values('HLTV Rating', ascending=False))
