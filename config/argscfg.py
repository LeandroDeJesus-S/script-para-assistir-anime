from config import utils
from animes_scrapping.animes import Animes
from database.animes_db import AnimesConfig
from webbrowser import open as webbrowser_open
from config.cor import Color
import logging as log
from animes_scrapping import animesonline
from . import history, season_ep_links


class Arguments(Color):
    @classmethod
    def watch(cls, anime: str):
        """redireciona para a pagina inicial do anime

        Args:
            anime (str): nome do anime
        """
        anime = anime.upper()
        log.debug(f'watch > anime : {anime}')
        
        anime_home_link = Animes.get_anime_home_link(anime)
        log.debug(f'watch > anime_home_link : Animes.get_anime_home_link : {anime_home_link}')
        
        if not anime_home_link:
            AnimesConfig.get_suggestion(anime)
            return
        
        is_anime_home_link_accessible = utils.is_accessible(anime_home_link)
        log_msg = f'watch > is_anime_home_link_accessible : utils.is_accessible : {is_anime_home_link_accessible}'
        log.debug(log_msg)
        if not is_anime_home_link_accessible:
            msg = Color.red('não foi possivel acessar o anime...')
            print(msg)
            return
        
        webbrowser_open(anime_home_link)
        log.info(f'watch > redirecionado para {anime_home_link}')

    @classmethod
    def watch_season_ep(cls, anime: str,  se: int, ep: int):
        """redireciona para anime com temporada e/ou episodio especifico

        Args:
            anime (str): nome do anime
            se (str): numero da temporada
            ep (str): numero do episodio
        """
        from config.utils import is_accessible
        from .season_ep_links import SeasonEp

        if se is None: se = 1
        if ep is None: ep = 1
            
        log.debug(f'NEW_watch_season_ep > anime : {anime} : season : {se} : ep : {ep}')
        anime = anime.upper()
        anime_homelink = Animes.get_anime_home_link(anime)
        log.debug(f'NEW_watch_season_ep > anime_homelink : {anime_homelink}')
        link_to_redirect = SeasonEp(anime_homelink).link_to_season_ep(ep, se)
        log.debug(f'NEW_watch_season_ep > link_to_redirect : {link_to_redirect}')
        if not is_accessible(link_to_redirect):
            print(Color.red('Não foi possivel acessar o link do anime...'))
            return
        webbrowser_open(link_to_redirect)

    @classmethod
    def add_anime(cls, anime_name: str, url: str) -> None:
        """
        adiciona um novo anime na base de dados se não existir e
        a url for valida

        anime_name: nome do anime
        url: url da pagina inicial do anime
        """

        anime_name = anime_name.upper()
        log.debug(f'add_anime > anime_name : {anime_name}')
        finds = AnimesConfig.search_anime(anime_name)
        if finds and anime_name == finds[1]:
            msg = 'anime ja existe.'
            print(cls.yellow(msg))
            log.info(f'add_anime > {anime_name} não adicionado pois já existe')
            return
        
        Animes.add_anime(anime_name, url)
        log.info(f'add_anime > {anime_name} foi adicionado com exito na base de dados')
    
    @classmethod
    def new(cls, anime_name: str) -> None:
        """
        redireciona para o episódio mais recente do anime passado

        anime_name: nome do anime
        """
        anime_name = anime_name.upper()
        log.debug(f'new > anime_name : {anime_name}')

        se_num = Animes.get_latest_season(anime_name)
        log.debug(f'new > se_num : {se_num}')
        ep_num = Animes.get_latest_episode(anime_name)
        log.debug(f'new > ep_num : {ep_num}')
        if not ep_num:
            AnimesConfig.get_suggestion(anime_name)
            return
        
        link = Animes.get_anime_home_link(anime_name)
        log.debug(f'new > link : {link}')
        
        link_to_redirect = season_ep_links.SeasonEp(link).link_to_new(ep_num, se_num)
        
        if not utils.is_accessible(link_to_redirect):
            print(f'Não foi possivel acessar : {link_to_redirect}')
            return
        
        webbrowser_open(link_to_redirect)
        if not se_num: se_num = None
        history.save_history(anime_name, ep_num, se_num)
        log.info(f'new > redirecionado para : {link_to_redirect}')
        
    @classmethod
    def site_home(cls):
        """redireciona para a pagina inicial do site quando -sh é chamado
        """
        animesonline.AnimesOnline.open_home_page()
        
    @classmethod
    def last_animes(cls):
        """mostra os ultimos lançamentos de animes
        """
        animesonline.AnimesOnline.show_last_animes()
        
    @classmethod
    def last_episodes(cls):
        """mostra os ultimos lançamentos de episodios
        """
        animesonline.AnimesOnline.show_last_eps()
        
    @classmethod
    def fetch_animes(cls, fetch: str):
        """busca anime nos animes salvos"""
        
        animes = AnimesConfig.search_anime(fetch, fetch_range='all')
        for _, anime, *_ in animes:
            print(anime)
        
        num_results = len(animes)
        num_results = Color.green(num_results) if num_results > 0 else Color.red(num_results)
        print(f'{num_results} resultados encontrados.')
