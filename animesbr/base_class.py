import requests
from bs4 import BeautifulSoup
import webbrowser
from database.db import Database


class AnimesBrBase:
    DATABASE = 'animesbr.sqlite'
    ANIMES_TABLE = 'animes_release'
    ANIME_FIELDS = '(id, name, rate)'
    EPISODES_TABLE = 'episodes_release'
    EPISODE_FIELDS = '(id, anime, ep)'
    LINKS_TABLE = 'anime_links'
    LINKS_FIELDS = '(id, anime, link)'
    def __init__(self) -> None:
        self.db = Database(self.DATABASE)
        self.home = 'https://animesbr.cc/'
        self.episodes = [
            'https://animesbr.cc/episodio/',
            'https://animesbr.cc/episodio/page/2/',
            'https://animesbr.cc/episodio/page/3/',
        ]
        self.animes = [
            'https://animesbr.cc/anime/',
            'https://animesbr.cc/anime/page/2/',
            'https://animesbr.cc/anime/page/3/',
        ]
        self.is_online = True
        if not self.is_online:
            print('Site offline')
            return
    
    @property
    def is_online(self):
        return self._is_online
    
    @is_online.setter
    def is_online(self, _):
        try:
            self._is_online = self.url_is_ok(self.home)
        except:
            self._is_online = False
        
    def url_is_ok(self, url):
        if url is not None and requests.get(url).status_code == 200:
            return True
        return False
        
    def go_home(self):
        webbrowser.open(self.home)
        
    def get_animes(self) -> list[str]:
        animes = []
        for page in range(3):
            html = requests.get(self.animes[page]).content
            soup = BeautifulSoup(html, 'html.parser')
            animes += [h3.text for h3 in soup.select('article.item div h3')]
        return animes
    
    def get_anime_rate(self) -> list[str]:
        rates = []
        for page in range(3):
            html = requests.get(self.animes[page]).content
            soup = BeautifulSoup(html, 'html.parser')
            rates += [div.text for div in soup.select('div.rating')]
        return rates
    
    def get_anime_and_rate(self) -> list[dict[str, str]]:
        animes = [
            {'name': a, 'rate': r} for a, r in zip(self.get_animes(), 
                                                    self.get_anime_rate())
        ]
        return animes
    
    def get_episodes(self) -> list[dict[str, str]]:
        episodes = []
        for page in range(3):
            html = requests.get(self.episodes[page]).content
            soup = BeautifulSoup(html, 'html.parser')
            for div in soup.select('div.eptitle'):
                *name, ep_num = div.text.split()
                name = ' '.join(name).replace('Episódio', '').strip()
                episodes.append({'name': name, 'ep': ep_num})
        return episodes
    
    