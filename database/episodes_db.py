import sqlite3
import logging as log


class EpsConfig:
    episode_releases_database = 'database/ultimosEPS.db'
    @classmethod
    def save_last_eps(cls, traduction: str, name: str, ep: int):
        import sqlite3

        log.debug(f'save_last_eps > traduction : {traduction} | name : {name} | ep : {ep}')
        connection = sqlite3.connect(cls.episode_releases_database)
        cursor = connection.cursor()

        cmd = 'INSERT OR IGNORE INTO last_eps (traducao, nome, episodio) VALUES (?, ?, ?)'
        values = (traduction, name, ep)

        cursor.execute(cmd, values)
        connection.commit()

        cursor.close()
        connection.close()
        log.info(f'save_last_eps > {traduction} | {name} | {ep} enviado para base de dados.')

    @classmethod
    def sent_last_eps_to_database(cls, releases: list[str]) -> None:
        for anime in releases:
            traduction, *name, ep = anime.split()
            name = ' '.join(name)
            EpsConfig.save_last_eps(traduction, name, int(ep))
        log.info(f'sent_last_eps_to_database > releases : {len(releases)} eps enviados para base de dados')

    @classmethod
    def get_last_eps_in_database(cls) -> list[tuple[str, str, int]]:
        connection = sqlite3.connect(cls.episode_releases_database)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM last_eps')

        eps = cursor.fetchall()

        cursor.close()
        connection.close()
        log.info(f'get_last_eps_in_database > eps : {len(eps)} episodios encontrados')
        return eps

    @classmethod
    def update_last_eps_database(cls) -> None:
        from animes_scrapping.animesonline import AnimesOnline
        from config.cor import Color

        print(Color.yellow('Atualizando episodios da base de dados...'))
        new_episodes = AnimesOnline.get_last_eps()
        cls.sent_last_eps_to_database(new_episodes)
        print(Color.blue('Base de dados atualizada!\n'))
        log.info(f'update_last_eps_database > new_episodes enviados para base de dados')


if __name__ == '__main__':
    print(EpsConfig.get_last_eps_in_database())
