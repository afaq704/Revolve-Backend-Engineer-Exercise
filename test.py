import pytest
import pandas as pd
from datetime import datetime as dt, timedelta
import os
import numpy as np

from main import question_five, question_four, question_one, question_two


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
    os.remove("test_flights.csv")
    os.remove("test_airports.csv")
    assert result == len(list(set(list(origin))))


def test_question_four():
    flights = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    weights_a = np.random.randint(50, 100, 13)
    weights_b = np.random.randint(1, 50, 13)
    rows = []
    manufacturers = []
    for i in range(26):
        if i % 2:
            weight = weights_a[i // 2]
            manufacturers.append([flights[i] * 3, "MANUFACTURER_A"])
        else:
            weight = weights_b[i // 2]
            manufacturers.append([flights[i] * 3, "MANUFACTURER_B"])
        for j in range(weight):
            dep_delay = np.random.randint(1, 20)
            arr_delay = np.random.randint(1, 20)
            rows.append([flights[i] * 3, dep_delay, arr_delay])
    rows = np.array(rows)
    manufacturers = np.array(manufacturers)
    np.random.shuffle(rows)
    np.random.shuffle(manufacturers)
    df = pd.DataFrame(rows, columns=["tailnum", "dep_delay", "arr_delay"])
    df.to_csv("test_flights.csv")

    df = pd.DataFrame(manufacturers, columns=["tailnum", "manufacturer"])
    df.to_csv("test_manufacturer.csv")

    result = question_four("test_flights.csv", "test_manufacturer.csv")

    os.remove("test_flights.csv")
    os.remove("test_manufacturer.csv")
    assert result == "MANUFACTURER_A"


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
    os.remove("test_flights.csv")
    os.remove("test_airports.csv")
    assert list(result) == sorted([codes[idx], codes_rev[idx]])
