import requests
import pytz
import datetime


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
    server_time = datetime.datetime.utcfromtimestamp(user['timestamp'])
    client_time = pytz.timezone(user['timezone']).fromutc(server_time)
    if MIDNIGHT <= client_time.hour < EARLY_MORNING:
        return user['username'], client_time
    else:
        return None


if __name__ == '__main__':
    for user_record in load_attempts():
        midnighter = get_midnighter_candidate(user_record)
        if midnighter:
            midnighter_nick, midnighter_time = midnighter
            print('{} at {}'.format(
                midnighter_nick,
                midnighter_time.strftime('%d.%m.%Y %H:%M:%S')
            ))
