import datetime

import pandas as pd


def is_letter(s: str) -> bool:
    all_letter = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    return any([let in all_letter for let in list(s)])


def df_to_list(df: pd.DataFrame) -> list:
    if not isinstance(df, pd.DataFrame):
        return []

    data_list = []
    keys = list(df.columns.values)
    for _, row in df.iterrows():
        data_list.append({key: row[key] for key in keys})
    return data_list


def get_today_zero_last() -> tuple:
    now = datetime.datetime.now()
    zero_time = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    last_time = zero_time + datetime.timedelta(hours=24)
    return zero_time, last_time


def get_expire_seconds() -> int:
    pass