import argparse
from datetime import datetime, timedelta, date
from enum import Enum
import pandas as pd
import requests
from pathlib import Path

outfolder =Path.cwd().joinpath('output')

class AustralianState(Enum):
    NSW = "nsw"
    VIC = "vic"
    QLD = "qld"
    WA = "wa"
    SA = "sa"
    TAS = "tas"
    ACT = "act"
    NT = "nt"



def get_annual_holidays(jurisdiction: AustralianState) -> list:
    """
    Get a list of annual holidays for the specified jurisdiction.

    Parameters:
    jurisdiction (AustralianState): The Australian state or territory to retrieve the holidays for.

    Returns:
    list: A list of `date` objects representing the annual holidays for the specified jurisdiction.

    Raises:
    HTTPError: If there was an error retrieving the holiday data from the API.
    """
    url = f'https://data.gov.au/data/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22d256f989-8f49-46eb-9770-1c6ee9bd2661%22%20WHERE%20%22Jurisdiction%22%20LIKE%20%27{jurisdiction}%27'
    try:
        response = requests.get(url)
        holidays = []
        for holiday in response.json()['result']['records']:
            holidays.append(datetime.strptime(holiday['Date'], '%Y%m%d').date())
        return holidays
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.HTTPError(f"Error retrieving holidays data from API for {jurisdiction}: {e}")


def convert_strings_to_dates(str_list: list) -> list:
    """
    Convert a list of date strings in 'YYYYmmdd' format to a list of date objects.

    Parameters:
    str_list (list): A list of date strings in 'YYYYmmdd' format.

    Returns:
    list: A list of date objects corresponding to the input strings.

    """
    date_list = []
    for date_str in str_list:
        date = datetime.strptime(date_str, '%Y%m%d').date()
        date_list.append(date)
    return date_list



def get_next_business_day(datein: date = None, holidays: list = None) -> dict:
    """
    Get the next business day after a given date, accounting for weekends and holidays.

    Parameters:
    - datein (date): The date to start from. If not provided, the current date will be used.
    - holidays (list): A list of date objects representing holidays. If not provided, no holidays will be used.

    Returns:
    - A dictionary with two keys: 'Date' and 'Next Business Day'. 'Date' is the input date, and 'Next Business Day'
      is the date of the next business day after the input date.


    """
    if datein is None:
        datein = date.today()
    if holidays is None:
        holidays = []
    nbd_dict = {'Date': datein, 'Next Business Day': None}
    next_day = datein + timedelta(days=1)
    # Check if the next day is a weekend day or a holiday
    while next_day.weekday() >= 5 or next_day in holidays:
        next_day += timedelta(days=1)
    nbd_dict['Next Business Day'] = next_day
    return nbd_dict


def save_dates_to_excel(nbd_list, filename):
    """
    Save a dictionary of dates to an Excel file.

    Parameters:
    - dates_dict: A dictionary containing dates as keys and values.
    - filename: The filename to save the Excel file to.

    Returns:
    - None.
    """
    df = pd.DataFrame(nbd_list)
    df.to_excel(filename, index=False)


def generate_annual_nbd_lookuptable(year: int, holiday_list: list)-> list:
    """
    Iterate through all days of the specified year and print each day's date.

    Parameters:
    year (int): The year to iterate through.

    Returns:
    None
    """
    nbd_list = []
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        day_pair=get_next_business_day(current_date, holiday_list)
        nbd_list.append(day_pair)
        current_date += delta

    return nbd_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process an Australian state")
    parser.add_argument("state", type=str, help="The Australian state to process")
    args = parser.parse_args()
    state_map = {
        "NSW": "New South Wales",
        "VIC": "Victoria",
        "QLD": "Queensland",
        "WA": "Western Australia",
        "SA": "South Australia",
        "TAS": "Tasmania",
        "NT": "Northern Territory"
    }

    action = "Generating NBD lookup for "
    if args.state in state_map:
        print(f"{action} {state_map[args.state]}")
    else:
        print("Invalid state entered")
        exit(1)
    state = args.state.lower()
    hols = get_annual_holidays(state)
    nbd_lookup_list=generate_annual_nbd_lookuptable(2023, hols)
    outfolder.mkdir(parents=True, exist_ok=False)
    outfile = outfolder.joinpath(f"{state}_nbd_lookup.xlsx")
    print(f"saving data to {state}_nbd_lookup.xlsx")
    save_dates_to_excel(nbd_lookup_list, outfile)
    # Print the results
