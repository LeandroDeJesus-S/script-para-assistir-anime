from .base_class import AnimesBrBase
from bs4 import BeautifulSoup
import requests
import webbrowser
from termcolor import cprint


class Anime(AnimesBrBase):    
    def __init__(self):
        super().__init__()
        self.anime_homepage = None
        self.most_recent_ep_num = None
        self.most_recent_season_key = None
        self.most_recent_season_num = None
        self.most_recent_ep_link = None
        self.anime_is_online = True
    
    @property
    def anime_homepage(self):
        return self._anime_homepage
    
    @anime_homepage.setter
    def anime_homepage(self, value):
        self.db.connect_db()
        
        if isinstance(value, str):
            value = value.lower()
            
        data = self.db.get_one_data(self.LINKS_TABLE, 'anime', value)
        if not data:
            self._anime_homepage = None
            return
        
        self._anime_homepage = data[-1]
        self.db.close_db()
    
    def anime_homepage_is_ok(self) -> bool:
        """verifica se o link em self.anime_homepage é valido e esta acessível

        Returns:
            bool: True se ok senão False
        """
        if self.anime_homepage is None:
            cprint('Anime não encontrado.', 'yellow')
            return False
        if not self.url_is_ok(self.anime_homepage):
            cprint('Não foi possível acessar a pagina do anime.', 'yellow')
            return False
        
        return True
    
    def get_anime_eps(self) -> list[str]:
        """pega os episódios enumerados no formato season - episodes

        Returns:
            list[str]: [1-1, 1-2, ...]
        """
        if not self.anime_homepage_is_ok():
            return
        html = requests.get(self.anime_homepage).content
        soup = BeautifulSoup(html, 'html.parser')
        eps = [div.text for div in soup.select('div.numerando')]
        return eps
    
    def get_ep_links(self) -> list[str]:
        """pega os links de todos os episódios sem separação de temporadas.

        Returns:
            list[str]: lista com os links dos episódios
        """
        html = requests.get(self.anime_homepage).content
        soup = BeautifulSoup(html, 'html.parser')
        links = [a.get('href') for a in soup.select('div.episodiotitle a')]
        return links
    
    def get_season_ep_links(self) -> dict[str, list[str]]:
        """pega os links dos episódios dividindo por temporadas

        Returns:
            dict[str, list[str]]: {'season x': [link1, link2, ...], ...}
        """
        if not self.url_is_ok(self.anime_homepage):
            return
        
        links = list(reversed(self.get_ep_links()))
        season_ep_links = {}
        c = 0
        for n, link in enumerate(links):
            if 'episodio-1/' in link:
                c += 1
                if f'season {n+1}' not in season_ep_links:
                    season_ep_links[f'season {c}'] = []
                    
                season_ep_links[f'season {c}'].append(link)
                continue
            
            season_ep_links[f'season {c}'].append(link)
        return season_ep_links
    
    def eps_and_links(self) -> dict[str, list[tuple[str, int]]]:
        """retorna um dicionario com a key 'season x' tendo como
        valor uma lista de tuplas sendo o link e o numero do episódio.

        Returns:
            dict[str, list[tuple[str, str]]]: {"season 1": [("link_ep1", 1),],...}
        """
        if not self.url_is_ok(self.anime_homepage):
            return
        
        links = self.get_season_ep_links()
        episodes = self.format_eps_to_dict()

        dic = {}
        for link, ep in zip(links.items(), reversed(episodes.items())):
            dic[link[0]] = list(zip(
                link[1], reversed(ep[1])
            ))
        
        return dic
    
    def format_eps_to_dict(self) -> dict[str, int]:
        if not self.url_is_ok(self.anime_homepage):
            return
               
        fmt_eps = {}
        for se_ep in self.get_anime_eps():
            se, ep = se_ep.split(' - ')
            if f'season {se}' in fmt_eps:
                fmt_eps[f'season {se}'].append(int(float(ep)))
                continue
            fmt_eps.update({f'season {se}' : [int(float(ep))]})
   
        return fmt_eps
        
    def add_anime_to_db(self, anime: str, link: str):
        self.db.connect_db()
        
        self.db.save_in_database(
            self.LINKS_TABLE, self.LINKS_FIELDS, (None, anime.lower(), link)
        )
        
        self.db.close_db()
    
    def go_anime_homepage(self) -> None:
        if not self.anime_homepage_is_ok():
            return
        webbrowser.open(self.anime_homepage)

    def set_most_recent_data(self):
        """seta os valores dos atributos self.most_recent_ep,
        self.most_recent_ep_link e self.most_recent_season.
        """
        if not self.url_is_ok(self.anime_homepage):
            return
        
        ep_links = self.eps_and_links()
        last_season = list(ep_links.keys())[-1]
        last_ep = ep_links[last_season][-1]
        
        self.most_recent_ep_num = last_ep[1]
        self.most_recent_ep_link = last_ep[0]
        self.most_recent_season_key = last_season
        self.most_recent_season_num = int(float(last_season.replace('season ', '')))
    