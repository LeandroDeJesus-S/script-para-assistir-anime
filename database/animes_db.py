import sqlite3
import logging as log


class AnimesConfig:
    @classmethod
    def search_anime(cls, name: str, limit='') -> list[tuple[int, str, str, str]]:
        """busca o nome do anime no banco de dados e retorna os animes
        onde se encontram o valor passado.
        """
        if limit:
            limit = f" LIMIT {limit}"
        
        name = name.upper()
        connection = sqlite3.connect('animes.db')
        cursor = connection.cursor()

        cursor.execute(f'SELECT * FROM animes WHERE name LIKE ?{limit}', (f'{name}%',))

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        log.debug(f'search_anime > name : {name} | limit : {limit}')
        log.debug(f'search_anime > result : {result}')
        return result
    
    @classmethod
    def get_suggestion(cls, anime_name):
        from config.cor import Color

        anime_result = cls.search_anime(anime_name)[1]
        if anime_name.upper() not in anime_result:
            return
        msg = Color.red('Anime não encontrado...')
        suggestion = Color.blue(anime_result)
        msg1 = Color.yellow(f'Você quiz dizer: "{suggestion}\033[33m" ?')
        print(f'{msg}\n{msg1}')

        log.debug(f'get_suggestion > anime_result : {anime_result}')
    
    @classmethod
    def save_last_animes(cls, rate: str, name: str):
        import sqlite3

        try:
            rate = float(rate)
            connection = sqlite3.connect('database/ultimosAnimes.db')
            cursor = connection.cursor()

            cmd = 'INSERT OR IGNORE INTO last_animes (rate, name) VALUES (?, ?)'
            values = (rate, name)

            cursor.execute(cmd, values)
            connection.commit()

            cursor.close()
            connection.close()
        except ValueError:
            pass

    @classmethod
    def sent_last_animes_to_database(cls, releases: list[list[str, str]]) -> None:
        for anime in releases:
            rate, name = anime[0], anime[1]
            cls.save_last_animes(rate, name)
        log.info(f'sent_last_animes_to_database > {len(releases)} animes enviados para base de dados')

    @classmethod
    def get_last_animes_in_database(cls) -> list[tuple[str, str, int]]:
        connection = sqlite3.connect('database/ultimosAnimes.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM last_animes')

        animes = cursor.fetchall()

        cursor.close()
        connection.close()
        log.info(f'get_last_animes_in_database > animes : {len(animes)} puxados da base de dados')
        return animes

    @classmethod
    def update_last_animes_database(cls):
        from animes_scrapping.animesonline import AnimesOnline
        from config.cor import Color

        print(Color.yellow('Atualizando animes da base de dados...'))
        new_releases = AnimesOnline.get_last_animes()
        log.debug(f'update_last_animes_database > {len(new_releases)} novos animes encontrados')
        cls.sent_last_animes_to_database(new_releases)
        log.info(f'update_last_animes_database > {len(new_releases)} animes enviados para base de dados')
        print(Color.blue('Animes atualizados com sucesso!\n'))


if __name__ == '__main__':
    AnimesConfig.get_suggestion('bo')
