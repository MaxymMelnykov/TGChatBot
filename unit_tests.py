import pytest
from user_data import user_data
from utils import calculate_volume_count, calculate_ra_volume_count, clear_user_data


@pytest.fixture
#
def setup_user_data():
    user_id = 12345
    user_data[user_id] = {
        'container_calc_res_ra': 100,
        'area': 50000,
        'apartments': 1500,
    }
    yield user_id
    clear_user_data(user_id)


def test_calculate_volume_count(setup_user_data):
    user_id = setup_user_data
    volume = 10
    result = calculate_volume_count(user_id, volume)
    assert result == 10


def test_calculate_ra_volume_count(setup_user_data):
    user_id = setup_user_data
    result = calculate_ra_volume_count(user_id)
    assert result == 23


def test_clear_user_data(setup_user_data):
    user_id = setup_user_data
    clear_user_data(user_id)
    assert user_id not in user_data
