#!/usr/bin/env python

import requests

header = {'Authorization': 'Token 6aceed034b00402020f2d7caf29a525424d0263f'}

data = {
    'age_restriction': '21',
    'description': "Hello",
    'start_date_time': '2020-01-01T00:00:00Z',
    'name': 'Test',
    'ticket_purchase_url': 'http://www.example.com',
    'timezone_name': "Asia/Karachi",
    'call_to_action_id': 1,
    'end_date_time': '2020-05-01T00:00:00Z',
    'website': 'http://www.example.com',
    'ticket_price': 12.0,
    'event_location': {
        'location': "Al Hamra",
        'address': "Gadafi stadium",
        'latitude': 0.0,
        'longitude': 0.0,
        'zip_code': '54000',
        'city': 'Lahore',
        'country': 'Pakistan',
        'state': 'Punjab',
    },
    'theme_url': 'http://www.example.com',
    'event_categories': [
        {'category_id': 1, 'sub_category_id': 2},
    ]
}

url = 'http://localhost:8000'
r = requests.post(f'{url}/ow/events/', json=data, headers=header)

print(r.json())
