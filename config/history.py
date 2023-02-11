from datetime import datetime
import json
from .cor import Color

HISTORY_FILE = 'config/history.json'


def save_history(anime: str, episode: str, season=None):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        time = datetime.strftime(datetime.now(), '%d/%b/%Y')
        data.append({'time': time, 'anime': anime, 'episode': episode, 'season': season})
    with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def show_history():
    with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for d in data:
            time, anime, se, ep = d.values()
            if se is None:
                print(f'{Color.grey(time)} - {Color.blue(anime)} - {Color.yellow(ep)}')
                continue
            print(f'{Color.grey(time)} - {Color.blue(anime)} - {Color.green(se)} - {Color.yellow(ep)}')
