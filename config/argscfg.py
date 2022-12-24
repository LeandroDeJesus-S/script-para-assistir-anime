from config import utils
from animes_scrapping.animes import Animes
from database.animes_db import AnimesConfig
from webbrowser import open as webbrowser_open
from config.cor import Color
import logging as log


class Arguments(Color):
    @classmethod
    def watch(cls, anime):
        log.debug(f'watch > anime : {anime}')
        anime_home_link = Animes.get_anime_home_link(anime)
        log.debug(f'watch > anime_home_link : Animes.get_anime_home_link : {anime_home_link}')
        if not anime_home_link:
            AnimesConfig.get_suggestion(anime)
            return
        is_anime_homelink_accessible = utils.is_accessible(anime_home_link)
        log_msg = f'watch > is_anime_homelink_accessible : utils.is_accessible : {is_anime_homelink_accessible}'
        log.debug(log_msg)
        if not is_anime_homelink_accessible:
            msg = Color.red('não foi possivél acessar o anime...')
            print(msg)
            return
        webbrowser_open(anime_home_link)
        log.info(f'watch > redirecionado para {anime_home_link}')

    @classmethod
    def watch_season_ep(cls, anime: str,  se: str, ep: str):
        from config.utils import is_accessible

        link = Animes.get_anime_link_to_season_ep(anime)
        log.debug(f'watch_season_ep > link : Animes.get_anime_link_to_season_ep : {link}')
        link = link.replace('SE', f'-{se}') if se else link.replace('SE', '')
        log.debug(f'watch_season_ep > link.replace SE: {link}')
        link = link.replace('EP', ep) if ep else link.replace('EP', '')
        log.debug(f'watch_season_ep > link.replace EP: {link}')
        is_accessible = is_accessible(link)
        log.debug(f'watch_season_ep > is_accessible : {is_accessible}')
        msg = cls.red('verifique se o numero do episódio ou da temporada está correto.')
        if not is_accessible:
            print(msg)
            return
        webbrowser_open(link)
        log.info(f'watch_season_ep > redirecionado para {link}')

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
        anime_already_exists = False
        for anim in finds:
            anime_already_exists = anime_name == anim[1]
            if anime_already_exists:
                anime_already_exists = True
                print(cls.yellow('anime ja existe.'))
                break
        else:
            Animes.add_anime(anime_name, url)

        log.debug(f'add_anime > anime_already_exists : {anime_already_exists}')

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
        link = Animes.get_anime_link_to_season_ep(anime_name)
        log.debug(f'new > link : {link}')
        link = link.replace('SE', f'-{se_num}') if se_num else link.replace('SE', '')
        log.debug(f'new > link replaced SE: {link}')
        link = link.replace('EP', f'{ep_num}') if ep_num else link.replace('EP', '')
        log.debug(f'new > link replaced EP: {link}')
        webbrowser_open(link)
        log.info(f'new > redirecionado para : {link}')


if __name__ == '__main__':
    ...
