import datetime
import json
import time
from typing import List

import cachetools.func
import pandas as pd
import requests
import schedule
from retry import retry


def get_all_district_ids():
    district_df_all = None
    for state_code in range(1, 40):
        response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code),
                                timeout=3)
        district_df = pd.DataFrame(json.loads(response.text))
        district_df = pd.json_normalize(district_df['districts'])
        if district_df_all is None:
            district_df_all = district_df
        else:
            district_df_all = pd.concat([district_df_all, district_df])

        district_df_all.district_id = district_df_all.district_id.astype(int)

    district_df_all = district_df_all[["district_name", "district_id"]].sort_values("district_name")
    return district_df_all


@cachetools.func.ttl_cache(maxsize=200, ttl=30 * 60)
@retry(KeyError, tries=5, delay=2)
def get_data(URL):
    #Go to http://httpbin.org/user-agent to find out your browser User-Agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    response = requests.get(URL, timeout=3, headers=headers)
    data = json.loads(response.text)['sessions']
    return data


def get_availability(days: int, district_ids: List[int], min_age_limit: int):
    base = datetime.datetime.today()  #+ datetime.timedelta(days=1)
    date_list = [base + datetime.timedelta(days=x) for x in range(days)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    INP_DATE = date_str[-1]

    all_date_df = None

    for district_id in district_ids:
        print(f"checking for INP_DATE:{INP_DATE} & DIST_ID:{district_id}")
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(
            district_id, INP_DATE)
        data = get_data(URL)
        df = pd.DataFrame(data)
        if len(df):
            df = df[["date", "min_age_limit", "available_capacity", "pincode", "name", "state_name", "district_name",
                     "block_name", "fee_type", "vaccine"]]
            if all_date_df is not None:
                all_date_df = pd.concat([all_date_df, df])
            else:
                all_date_df = df

    if all_date_df is not None:
        all_date_df = all_date_df.drop(["block_name"], axis=1).sort_values(
            ["date", "min_age_limit", "district_name", "available_capacity"], ascending=[True, True, True, False])
        all_date_df = all_date_df[all_date_df.min_age_limit == min_age_limit]
        all_date_df = all_date_df[all_date_df.available_capacity > 0]
        return all_date_df
    return pd.DataFrame()


def telegram_bot_sendtext(bot_message):
    bot_token = '<your_bot_token>'
    channel_id = '<your_channel_id>'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + channel_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    print(response.json())
    return response.json()


def create_telegram_messages(availability_data):
    for index, row in availability_data.iterrows():
        bot_message = "Centre Name = " + row['name'] + "\nPincode = " + str(row['pincode']) + "\nAge Group = " + str(
            row['min_age_limit']) + "+" + "\nDate = " + row['date'] + "\nAvailable Capacity = " + str(
            row['available_capacity']) + "\nVaccine = " + row['vaccine'] + "(" + row['fee_type'] + ")"
        telegram_bot_sendtext(bot_message)

def main():
    #Change district here, can add multiple districts in the list as well
    #Refer districts.csv for district_id
    Singrauli = 330

    dist_ids = [Singrauli]
    next_n_days = 1
    min_age_limit = 18

    availability_data = get_availability(next_n_days, dist_ids, min_age_limit)
    create_telegram_messages(availability_data)


if __name__ == "__main__":
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
