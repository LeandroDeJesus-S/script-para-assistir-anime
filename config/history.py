from datetime import datetime
import json
from .cor import Color


class History(object):
    __history_file = 'config/history.json'
    
    @classmethod
    def save_history(cls, anime: str, episode: str, season=None):
        with open(cls.__history_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            time = datetime.strftime(datetime.now(), '%d/%b/%Y')
            for d in data:
                if d['anime'] == anime:
                    d['episode'], d['season'], d['time'] = episode, season, time
                    cls.set_history(data)
                    return
                
            data.append({'time': time, 'anime': anime, 'episode': episode, 'season': season})
            cls.set_history(data)

    @classmethod
    def set_history(cls, data):
        with open(cls.__history_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def show_history(cls):
        with open(cls.__history_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for d in data:
                time, anime, ep, se = d.values()
                if se is None:
                    print(
                        f'data: {Color.grey(time)}\n'
                        f'anime: {Color.blue(anime)}\n'
                        f'episódio: {Color.red(ep)}\n'
                    )
                    continue
                
                print(
                    f'data: {Color.grey(time)}\n'
                    f'anime: {Color.cian(anime)}\n'
                    f'temporada: {Color.green(se)}\n'
                    f'episódio: {Color.red(ep)}\n'
                )
