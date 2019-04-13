import requests
from pytz import timezone
from datetime import datetime
from collections import defaultdict


MIDNIGHT = 0
EARLY_MORNING = 6


def get_devman_api_page(page):
    devman_api = 'https://devman.org/api/challenges/solution_attempts/'
    return requests.get(devman_api, {'page': page}).json()


def load_attempts():
    page_num = 1
    while True:
        attempts_info = get_devman_api_page(page_num)
        yield from attempts_info['records']
        if page_num == attempts_info['number_of_pages']:
            break
        page_num += 1


def get_midnighter_candidate(user):
    client_tz = timezone(user['timezone'])
    client_time = datetime.fromtimestamp(user['timestamp'], tz=client_tz)
    if MIDNIGHT <= client_time.hour < EARLY_MORNING:
        return user['username'], client_time


if __name__ == '__main__':
    midnighters = defaultdict(list)
    for attempt in load_attempts():
        midnighter = get_midnighter_candidate(attempt)
        if midnighter:
            midnighter_nick, midnighter_time = midnighter
            midnighters[midnighter_nick].append(midnighter_time)
    for nick, times in dict(midnighters).items():
        print(nick)
        print('\t{}\n'.format(
            '\n\t'.join([time.strftime('%d.%m.%Y %H:%M:%S') for time in times])
        ))

