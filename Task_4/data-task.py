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

    print(flights.head(3))

if __name__ == '__main__':
    main()