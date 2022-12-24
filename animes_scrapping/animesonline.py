from bs4 import BeautifulSoup
import requests as rq
from config.cor import Color
import logging as log


class AnimesOnline(Color):
    home = 'https://animesonline.cc/tv/'
    last_episodes = (
        'https://animesonline.cc/episodio/',
        'https://animesonline.cc/episodio/page/2/',
        'https://animesonline.cc/episodio/page/3/'
    )

    last_animes = (
        'https://animesonline.cc/anime/',
        'https://animesonline.cc/anime/page/2/',
        'https://animesonline.cc/anime/page/3/'
    )

    def __init__(self):
        super().__init__()

    @classmethod
    def open_home_page(cls) -> None:
        """abre a pagina inicial do site"""
        import webbrowser
        from config import utils
        from config.cor import Color

        is_accessible = utils.is_accessible(cls.home)
        log.debug(f'open_home_page > is_accessible : {is_accessible}')
        if not is_accessible:
            print(Color.red('não foi acessar o site no momento...'))
            return
        webbrowser.open(cls.home)
        log.info(f'open_home_page > redirecionado para : {cls.home}')

    @classmethod
    def get_last_eps(cls) -> list:
        """pega uma lista dos episódios mais recentes

        Returns:
            list: lista com tipo de tradução, nome do anime, e numero do ep
        """
        print('buscando por ultimos lançamentos de episodios...')

        releases = []
        for page in cls.last_episodes:
            response = rq.get(page)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            releases.extend([i.text for i in soup.select('.item.se.episodes')])
        log.info(f'get_last_eps > releases : {len(releases)} eps encontrados.')
        return releases

    @classmethod
    def show_last_eps(cls) -> None:
        """show formatted latest eps releases from animesonline"""
        from database.episodes_db import EpsConfig

        animes = EpsConfig.get_last_eps_in_database()

        animes_in_database = [f'{i[0]} {i[1]} {i[2]}' for i in animes]
        last_episodes_releases = [i.strip() for i in cls.get_last_eps()]

        news = 0
        for anime in last_episodes_releases:
            log.debug(f'show_last_eps > {anime} in {animes_in_database}')
            if anime not in animes_in_database:
                print(cls.green(anime))
                news += 1
                continue
            print(anime)
        log.info(f'show_last_eps > animes : {len(animes)} puxados da base de dados.')
        log.info(f'show_last_eps > animes > news : {news} animes são novos')

    @classmethod
    def get_last_animes(cls) -> list[list[str, str]]:
        print('buscando por ultimos lançamentos de animes...')
        all_animes_releases = []
        for page in cls.last_animes:
            res = rq.get(page)
            soup = BeautifulSoup(res.text, 'html.parser')

            all_animes_in_page = []
            for i in soup.select('div.content'):
                for animes in i.select('article'):
                    rate, *name = animes.text.split()
                    all_animes_in_page.append([rate, ' '.join(name)])
                all_animes_releases.extend(all_animes_in_page)
        log.info(f'get_last_animes > all_animes_releases : {len(all_animes_releases)} animes encontrados')
        return all_animes_releases

    @classmethod
    def show_last_animes(cls):
        from database.animes_db import AnimesConfig

        animes_in_db = AnimesConfig.get_last_animes_in_database()
        animes_releases = cls.get_last_animes()
        for rate, anime in animes_releases:
            try:
                new_anime = (float(rate), anime)
                if new_anime in animes_in_db:
                    anime = cls.grey(anime)
                else:
                    cls.blue(anime)
                    log.info(f'show_last_animes > anime : {anime} é novo')
                print(f'Anime: {anime}')
                rate = float(rate)
                color_rate = cls.colorize_rate_anime(rate)
                print(f'Classificação: {color_rate}\n')
            except ValueError:
                print(f'Anime: {cls.grey(anime)}')
                print('rate: ')
                log.warning(f'show_last_animes > {(rate, anime)} rate não pode ser convertida')
                pass
        log.debug(f'show_last_animes > animes_in_db : {len(animes_in_db)} animes encontrados na base de dados')
        log.debug(f'show_last_animes > animes_releases : {len(animes_releases)} lançamentos de animes encontrados')

    @classmethod
    def colorize_rate_anime(cls, rate):
        if rate >= 9:
            return cls.purple(rate)
        if rate >= 7:
            return cls.green(rate)
        if rate >= 5:
            return cls.yellow(rate)
        return cls.red(rate)


if __name__ == '__main__':
    AnimesOnline.show_last_animes()
