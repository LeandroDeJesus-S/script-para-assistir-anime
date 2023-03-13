from animesbr import static_class
from .sites import WebSites
from termcolor import cprint
import webbrowser
import os
from .history import History


class Arguments:
    SITES = WebSites
    def __init__(self) -> None:
        self.__site = self.SITES.animesbr
        self._animesbr = static_class.AnimesBr()
        self._history = History()
        
    @property
    def _site(self):
        return self.__site 
    
    @_site.setter
    def _site(self):
        if not os.path.exists('.site-active'):
            with open('.site-active', mode='w') as f: f.write('animesbr')
            
        with open('.site-active', 'r', encoding='utf-8') as f:
            site = f.read().replace('\n', '')
            
        self.__site = site
        
    def watch(self, anime: str) -> None:
        """redireciona para a pagina inicial do animes

        Args:
            anime (str): nome do anime
        """
        if self.__site == self.SITES.animesbr:
            self._animesbr.anime_homepage = anime
            self._animesbr.go_anime_homepage()
    
    def watch_season_ep(self, anime: str, season: int=None, ep: int=None):
        """redireciona para um episodio e/ou temporada específicos.

        Args:
            anime (str): nome do anime
            season int, optional): numero da temporada. Defaults to 1.
            ep (int , optional): numero do episodio. Defaults to 1.
        """
        if not season: season = 1
        if not ep: ep = 1
        if self.__site == self.SITES.animesbr:
            self._animesbr.anime_homepage = anime
            if not self._animesbr.anime_homepage_is_ok():
                return
            
            try:
                link = self._animesbr.eps_and_links()[f'season {season}'][ep - 1][0]
            except (KeyError, IndexError):
                cprint('Episódio ou temporada inválidos.', 'red')
            else:
                webbrowser.open(link)
                self._history.save_history(anime, ep, season)
    
    def add_anime(self, anime: str, url: str) -> None:
        """adiciona um novo anime na base de dados

        Args:
            anime (str): nome do anime
            url (str): link do anime
        """
        if self.__site == self.SITES.animesbr:
            if not self._animesbr.url_is_ok(url):
                print('A url enviada não é ou não está acessível.')
                return
            self._animesbr.add_anime_to_db(anime, url)
            cprint(f'"{anime.upper()}" adicionado com sucesso.', 'light_green')

    def site_home(self) -> None:
        """redireciona para a pagina inicial do site"""
        if self.__site == self.SITES.animesbr:
            self._animesbr.open_homepage()
            
    def list_episodes(self, limit: int=None) -> None:
        """lista episódios lançados recentemente"""
        if self.__site == self.SITES.animesbr:
            self._animesbr.last_episodes(limit)
            self._animesbr.add_eps_to_database()
    
    def list_animes(self, limit: str=None) -> None:
        """lista os animes lançados recentemente"""
        if self.__site == self.SITES.animesbr:
            self._animesbr.last_animes(limit)
            self._animesbr.add_animes_to_database()
    
    def new(self, anime:str):
        """redireciona para o episodio e temporada mais recentes.

        Args:
            anime (str): nome do anime
        """
        if self.__site == self.SITES.animesbr:
            season, ep = self._animesbr.go_to_most_recent_season_and_ep(anime)
            self._history.save_history(anime, ep, season)
    
    def update(self):
        pass
    
    def fetch(self, animename:str) -> None:
        pass
    
    def history(self, limit: int=None, filter_name:str=None) -> None:
        self._history.show_history(limit, filter_name)
    
    def list_websites(self) -> None:
        """lista os sites disponíveis"""
        for site in self.SITES:
            print(site.name)
            
    def set_website(self, website) -> None:
        """seleciona um dos sites disponíveis para usar"""
        site = [site for site in self.SITES if website == site.name]
        if not site:
            return

        self.__site = site[0].name
        with open('.site-active', 'w') as f:
            f.write(f'{site[0].name}')

    def createsite(self, site_name: str) -> None:
        """cria um diretório com arquivos de base para implementar um
        novo site

        Args:
            site_name (str): nome do diretório que sera criado
        """
        import os, sys
        from pathlib import Path
        
        path = Path(sys.argv[0]).parent / site_name
        files = ['anime.py', 'anime_releases.py', 'base_class.py',
                 'episode_releases.py', 'static_class.py']
        
        if os.path.exists(path):
            cprint('Site já existe.', 'yellow')
            return
        
        os.mkdir(path)
        for file in files:
            Path(path / file).touch()
            
        