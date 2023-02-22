# Next business day

This is a simple Python application that calculates the next business day for a given Australian state over a 12 month period. The calculation takes into account weekends and public holidays specific to the chosen state.

## Dependencies

* Python 3.9 or later
* Poetry package manager
* Internet access to download dependencies and public holiday data

## Installation

To install the required Python dependencies, run the following command:

```bash
poetry install

```

## Executing program


* run the command to get the next business day for a given state (capitalised)
```
python3 main.py --state NSW
```

You can replace `NSW` with the abbreviation for the Australian state you want to get the next business day for.

## Testing

To run the tests and generate a coverage report, use the following command:

```
poetry run pytest -cov=main tests/  --cov-report lcov:cov.info
```

## Further Information

* Information on poetry inculding installation can be found https://python-poetry.org/docs/


* the application uses an api at data.gov.au to get the holidays for a given state
https://data.gov.au/dataset/ds-dga-b1bc6077-dadd-4f61-9f8c-002ab2cdff10/details

#### Note Queensland showday holidays are not included in the api
A list of Queensland showday holidays can be found at https://www.qld.gov.au/recreation/travel/holidays/showday
These will need to be added to the output manually for the region of interest

## Version History

* 0.1
    * Initial Release

## Author
Michael Paholski