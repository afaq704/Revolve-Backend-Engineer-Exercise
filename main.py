import pandas as pd


def question_one(flights_path):
    flights_df = pd.read_csv(flights_path)

    def generate_date(df):
        return f"{df['year']}/{df['month']}/{df['day']}"

    flights_df["date"] = flights_df.apply(generate_date, axis=1)
    flights_df["date"] = pd.to_datetime(flights_df["date"], format="%Y/%m/%d")
    return flights_df["date"].nunique()


def question_two(flights_path, airports_path):
    flights_df = pd.read_csv(flights_path)
    airports_df = pd.read_csv(airports_path)

    merge_df = pd.merge(
        flights_df, airports_df, left_on=["origin"], right_on=["IATA_CODE"]
    )
    return merge_df["CITY"].nunique()


def question_three():
    sol = (
        "Flights data contains the data about any flight service like "
        "departure time, arrival time, flight timings etc. Planes data "
        "contains specifications about any particular airplane. Both these "
        "datasets contains a commom attribute: tailnum, which relates a "
        "flight service to its airplane specifications."
    )
    return sol


def question_four(flights_path, planes_path):
    flights_df = pd.read_csv(flights_path)
    planes_df = pd.read_csv(planes_path)

    def is_delayed(df):
        if df["dep_delay"] > 0 or df["arr_delay"] > 0:
            return 1
        else:
            return 0

    flights_df["is_delayed"] = flights_df.apply(is_delayed, axis=1)
    merge_df = pd.merge(
        flights_df, planes_df, left_on=["tailnum"], right_on=["tailnum"]
    )
    delayed = merge_df.groupby("manufacturer").sum()["is_delayed"]
    return delayed.reset_index().loc[delayed.argmax(), "manufacturer"]


def question_five(flights_path, airports_path):
    flights_df = pd.read_csv(flights_path)
    airports_df = pd.read_csv(airports_path)

    def travel(df):
        org = df["origin"]
        dest = df["dest"]
        if org < dest:
            return f"{org}-{dest}"
        else:
            return f"{dest}-{org}"

    flights_df["travel"] = flights_df.apply(travel, axis=1)
    mode = flights_df["travel"].mode()[0]
    city_a, city_b = mode.split("-")
    city_a = airports_df[airports_df["IATA_CODE"] == city_a]["CITY"].values[0]
    city_b = airports_df[airports_df["IATA_CODE"] == city_b]["CITY"].values[0]
    return city_a, city_b


print("Solution 1:", question_one("data/flights.csv"))
# 365

print("Solution 2:", question_two("data/flights.csv", "data/airports.csv"))
# 2

print("Solution 3:", question_three())
# Flights data contains the data about any flight service like departure time,
# arrival time, flight timings etc. Planes data contains specifications about
# any particular airplane. Both these datasets contains a commom attribute:
# tailnum, which relates a flight service to its airplane specifications.

print("Solution 4:", question_four("data/flights.csv", "data/planes.csv"))
# BOEING

print("Solution 5:", question_five("data/flights.csv", "data/airports.csv"))
# ('New York', 'Los Angeles')
