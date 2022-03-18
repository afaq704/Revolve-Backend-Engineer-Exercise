import pytest
import pandas as pd
from datetime import datetime as dt, timedelta
import os
import numpy as np

from main import question_five, question_one, question_two


def test_question_one():
    start_date = dt.strptime("2015/01/01", "%Y/%m/%d")
    end_date = dt.strptime("2021/01/01", "%Y/%m/%d")
    years = []
    months = []
    days = []
    total_days = 0
    while start_date != end_date:
        years.append(start_date.year)
        months.append(start_date.month)
        days.append(start_date.day)
        start_date += timedelta(days=1)
        total_days += 1

    df = pd.DataFrame({"year": years, "month": months, "day": days})
    df.to_csv("test_data.csv", index=False)
    calculated_days = question_one("test_data.csv")
    os.remove("test_data.csv")
    assert calculated_days == total_days


def test_question_two():
    origin = "AACCEEGGIIKKMMOOQQSSUUWWYY"
    all_cities = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    weights = np.random.randint(1, 100, 26)
    rows = []
    for i in range(26):
        for j in range(weights[i]):
            rows.append([origin[i], all_cities[i]])
    rows = np.array(rows)
    np.random.shuffle(rows)
    df = pd.DataFrame(rows, columns=["origin", "dest"])
    df.to_csv("test_flights.csv")
    df = pd.DataFrame(
        {"IATA_CODE": list(all_cities), "CITY": list(all_cities)})
    df.to_csv("test_airports.csv")

    result = question_two("test_flights.csv", "test_airports.csv")

    assert result == len(list(set(list(origin))))


def test_question_five():
    codes = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    weights = np.random.randint(1, 100, 26)
    idx = (weights + weights[::-1]).argmax()
    codes_rev = codes[::-1]
    rows = []
    for i in range(26):
        for j in range(weights[i]):
            rows.append([codes[i], codes_rev[i]])
    rows = np.array(rows)
    np.random.shuffle(rows)
    df = pd.DataFrame(rows, columns=["origin", "dest"])
    df.to_csv("test_flights.csv")
    df = pd.DataFrame({"IATA_CODE": list(codes), "CITY": list(codes)})
    df.to_csv("test_airports.csv")

    result = question_five("test_flights.csv", "test_airports.csv")

    assert list(result) == sorted([codes[idx], codes_rev[idx]])
