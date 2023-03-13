from datetime import datetime
from termcolor import colored
import json


class History(object):
    __history_file = 'conf/history.json'
    
    @classmethod
    def save_history(cls, anime: str, episode: str, season=None):
        with open(cls.__history_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            time = datetime.strftime(datetime.now(), '%d/%b/%Y')
            for d in data:
                if d['anime'].lower() == anime.lower():
                    if season > int(float(d['season'])):
                        d['season'], d['episode'] = season, episode
                    elif episode > int(float(d['episode'])):
                        d['episode'] = episode
                        
                    d['time'] = time
                    cls.set_history(data)
                    return
                
            data.append({
                'time': time, 'anime': anime.upper(), 
                'episode': episode, 'season': season
            })
            cls.set_history(data)

    @classmethod
    def set_history(cls, data):
        with open(cls.__history_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def show_history(cls, limit: int=None, filter_name: str=None):
        with open(cls.__history_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if limit:
                data = data[:limit]
                
            for d in data:
                time, anime, ep, se = d.values()
                if filter_name and filter_name.lower() == d['anime'].lower():
                    cls.print_history(time, anime, ep, se)
                    return
                
                if not filter_name:
                    cls.print_history(time, anime, ep, se)

    @staticmethod
    def print_history(time, anime, ep, se):
        if se is None:
            print(
                f'data: {colored(time, "grey")}\n'
                f'anime: {colored(anime, "cyan")}\n'
                f'episódio: {colored(ep, "red")}\n'
            )
            return
                
        print(
            f'data: {colored(time, "grey")}\n'
            f'anime: {colored(anime, "cyan")}\n'
            f'temporada: {colored(se, "green")}\n'
            f'episódio: {colored(ep, "red")}\n'
        )