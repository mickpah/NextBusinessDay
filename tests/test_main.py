import pytest
from datetime import date

from ..main import get_annual_holidays, convert_strings_to_dates, get_next_business_day, save_dates_to_excel, generate_annual_nbd_lookuptable, AustralianState

@pytest.fixture
def sample_holiday_list():
    return [date(2023, 1, 1), date(2023, 12, 25), date(2023, 12, 26)]

def test_get_annual_holidays():
    assert len(get_annual_holidays(AustralianState.NSW.value)) > 0
    assert isinstance(get_annual_holidays(AustralianState.NSW.value)[0], date)

def test_convert_strings_to_dates():
    str_list = ['20230101', '20231225', '20231226']
    result = convert_strings_to_dates(str_list)
    assert len(result) == 3
    assert isinstance(result[0], date)

def test_get_next_business_day(sample_holiday_list):
    assert get_next_business_day(date(2023, 2, 17), sample_holiday_list)['Next Business Day'] == date(2023, 2, 20)
    assert get_next_business_day(date(2023, 12, 24), sample_holiday_list)['Next Business Day'] == date(2023, 12, 27)

def test_save_dates_to_excel(tmpdir):
    nbd_list = [{'Date': date(2023, 2, 20), 'Next Business Day': date(2023, 2, 21)}, {'Date': date(2023, 2, 21), 'Next Business Day': date(2023, 2, 22)}]
    filename = tmpdir.join('test_nbd_lookup.xlsx')
    save_dates_to_excel(nbd_list, filename)
    assert filename.check()
    assert filename.ext == '.xlsx'

def test_generate_annual_nbd_lookuptable(sample_holiday_list):
    nbd_list = generate_annual_nbd_lookuptable(2023, sample_holiday_list)
    assert len(nbd_list) == 365
    assert isinstance(nbd_list[0]['Date'], date)
    assert isinstance(nbd_list[0]['Next Business Day'], date)
