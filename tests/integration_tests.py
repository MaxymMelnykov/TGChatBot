import unittest
from user_data import user_data

from handlers import get_ra_area, get_ra_apartments


class TestGetRaAreaAndApartments(unittest.TestCase):
    def setUp(self):
        self.chat_id = "516166196"

    def test_get_ra_area_and_apartments_valid_input(self):
        valid_area_input = "50"  # Правильне значення площі
        message_area = type('obj', (object,), {"chat": type('obj', (object,), {"id": self.chat_id}), "text": valid_area_input})

        get_ra_area(message_area)

        self.assertEqual(user_data[self.chat_id]['area'], 50, "Площа не була збережена правильно.")

        valid_apartments_input = "3"
        message_apartments = type('obj', (object,), {"chat": type('obj', (object,), {"id": self.chat_id}), "text": valid_apartments_input})

        get_ra_apartments(message_apartments)

        self.assertEqual(user_data[self.chat_id]['apartments'], 3, "Кількість квартир не була збережена правильно.")

