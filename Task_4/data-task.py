import os
import pandas as pd


def main():
    # Get current working directory
    cwd = os.getcwd()

    # Get the parent directory
    parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))

    flights = pd.read_csv(os.path.join(parent_dir, "candidateEvalData", "flights.csv"))
    airports = pd.read_csv(os.path.join(parent_dir, "candidateEvalData", "airports.csv"))
    weather = pd.read_csv(os.path.join(parent_dir, "candidateEvalData", "weather.csv"))
    airlines = pd.read_csv(os.path.join(parent_dir, "candidateEvalData", "airlines.csv"))

    # 1. Add full airline name to the flights dataframe
    flights_with_airline = pd.merge(flights, airlines, on='carrier') # inner join using carrier column.
    # and show the arr_time, origin, dest and the name of the airline.
    flights_with_airline = flights_with_airline[['arr_time', 'origin', 'dest', 'name']]

    # 2. Filter resulting data.frame to include only flights containing the word JetBlue
    flights_jetblue = flights_with_airline[flights_with_airline['name'].str.contains("JetBlue", na=False)]

    # 3. Summarise the total number of flights by origin in ascending.
    flights_by_origin = flights_jetblue.groupby('origin').size().sort_values(ascending=True).reset_index(name='counts')

    # 4. Filter resulting data.frame to return only origins with more than 100 flights.
    flights_by_origin_more_than_100 = flights_by_origin[flights_by_origin['counts'] > 100]

if __name__ == '__main__':
    main()