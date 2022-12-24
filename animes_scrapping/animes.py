import sqlite3
from database.animes_db import AnimesConfig
import logging as log


class Animes:
    @classmethod
    def add_anime(cls, name: str, home: str):
        """adiciona um anime na base de dados

        Args:
            name (str): nome do anime
            home (str): link da pagina inicial do anime
            se (str): link da pagina de episódios do anime
        """
        from config.cor import Color

        se = cls.get_link_to_season_ep_when_adding(home)
        name = name.upper()
        log.debug(f'add_anime > name : {name} | home : {home}')
        log.debug(f'add_anime > se : get_link_to_season_ep_when_adding : {se}')

        conn = sqlite3.connect('database/animes.db')
        cursor = conn.cursor()

        cmd = 'INSERT OR IGNORE INTO animes (name, home, se) VALUES (?, ?, ?)'
        values = (name, home, se)

        cursor.execute(cmd, values)
        conn.commit()

        cursor.close()
        conn.close()
        log.info(f'add_anime > {name} | {home} | {se} enviados para base de dados')
        print(Color.green(f'{name} adicionado com sucesso'))

    @classmethod
    def get_anime_link_to_season_ep(cls, anime):
        anime = anime.upper()
        log.debug(f'get_anime_link > anime : {anime}')
        fetch = AnimesConfig.search_anime(anime)
        found = False
        link = ''
        for a in fetch:
            if anime == a[1]:
                found = True
                link = a[3]
                break
        log.debug(f'get_anime_link_to_season_ep > link : {link} | found : {found}')
        return link

    @classmethod
    def get_link_to_season_ep_when_adding(cls, anime_url_home: str) -> str:
        """pega link para redirecionar para episodio ou temporada especifica
        apartir da url inicial do anime.
        Args:
            anime_url_home (str): url da pagina inicial do anime
        Returns:
            str: a url configurada para redirecionar para um ep e/ou temporada
        """
        *_, anime_name_url = anime_url_home.split('/anime/')
        anm = anime_name_url.replace('/', '')

        url_season_ep = f'https://animesonline.cc/episodio/{anm}SE-episodio-EP/'
        log.debug(f'get_link_to_season_ep_when_adding > anime_name_url : {anime_name_url}')
        log.debug(f'get_link_to_season_ep_when_adding > anm : {anm}')
        log.debug(f'get_link_to_season_ep_when_adding > url_season_ep : {url_season_ep}')
        return url_season_ep

    @classmethod
    def get_latest_episode(cls, anime_name) -> str:
        """Pega o número do episódio mais recente do anime enviado
        Returns:
            str: número do episódio mais recente ou uma str vazia, caso
            não encontre.
        """
        import requests as rq
        from bs4 import BeautifulSoup

        anime_home_link = cls.get_anime_home_link(anime_name)
        if not anime_home_link:
            return ''

        res = rq.get(anime_home_link)
        soup = BeautifulSoup(res.text, 'html.parser')

        latest_ep_num = ''
        for ep_objs in soup.select('.episodios'):
            for ep_num in ep_objs.select('.numerando'):
                _, _, latest_ep_num = ep_num.text.split()

        log.debug(f'get_latest_episode > anime_name : {anime_name}')
        log.debug(f'get_latest_episode > anime_home_link : {anime_home_link}')
        log.debug(f'get_latest_episode > latest_ep_num : {latest_ep_num}')
        return latest_ep_num

    @classmethod
    def get_anime_home_link(cls, anime: str) -> str:
        """pega o link da pagina inicial do anime

        anime: (str) nome do anime desejado
        returns:
            link da pagina inicial ou string vazia caso não consiga
        """
        founded_anime = AnimesConfig.search_anime(anime)
        home_link = ''
        if founded_anime:
            home_link = founded_anime[2]
        
        log.debug(f'get_anime_home_link > anime : {anime}')
        log.debug(f'get_anime_home_link > home_link : {home_link}')
        return home_link

    @classmethod
    def get_latest_season(cls, anime_name: str) -> str:
        """retorna o número da temporada mais recente sendo ele > 1
        Returns:
            str: numero da temporada mais recente ou uma string vazia
        """
        import requests as rq
        from bs4 import BeautifulSoup

        anime_home_link = cls.get_anime_home_link(anime_name)
        log.debug(f'get_latest_season > anime_name : {anime_name}')
        log.debug(f'get_latest_season > anime_home_link : {anime_home_link}')
        if not anime_home_link:
            return ''
        res = rq.get(anime_home_link)
        soup = BeautifulSoup(res.text, 'html.parser')

        latest_season = ''
        for tmp_objs in soup.select('.tempep'):
            for tmp_num in tmp_objs.select('span'):
                if 'Temporada' not in tmp_num.text:
                    continue
                _, latest_season = tmp_num.text.split()

        greatest_1 = latest_season != '1'
        latest_season = latest_season if greatest_1 else ''
        log.debug(f'get_latest_season > greatest_1 : {greatest_1}')
        log.debug(f'get_latest_season > latest_season : {latest_season}')
        return latest_season


if __name__ == '__main__':
    ...
