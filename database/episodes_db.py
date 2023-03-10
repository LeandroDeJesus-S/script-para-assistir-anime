import sqlite3
import logging as log


class EpsConfig:
    database = 'db.sqlite3'
    @classmethod
    def save_last_eps(cls, traduction: str, name: str, ep: int):
        import sqlite3

        log.debug(f'save_last_eps > traduction : {traduction} | name : {name} | ep : {ep}')
        connection = sqlite3.connect(cls.database)
        cursor = connection.cursor()

        cmd = 'INSERT OR IGNORE INTO last_eps (traduction, name, ep) VALUES (?, ?, ?)'
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
        log.info(
            f'sent_last_eps_to_database > releases : {len(releases)} eps enviados para base de dados'
        )

    @classmethod
    def get_last_eps_in_database(cls, limit=None) -> list[tuple[str, str, int]]: #
        if limit is not None:
            limit = F'LIMIT {limit}'
        connection = sqlite3.connect(cls.database)
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM last_eps {limit}')

        eps = cursor.fetchall()

        cursor.close()
        connection.close()
        log.info(f'get_last_eps_in_database > eps : {len(eps)} episódios encontrados')
        return eps

    @classmethod
    def update_last_eps_database(cls) -> None:
        from animes_scrapping.animesonline import AnimesOnline
        from config.cor import Color

        print(Color.yellow('Atualizando episódios da base de dados...'))
        new_episodes = AnimesOnline.get_last_eps()
        cls.sent_last_eps_to_database(new_episodes)
        print(Color.blue('Base de dados atualizada!\n'))
        log.info(f'update_last_eps_database > new_episodes enviados para base de dados')


if __name__ == '__main__':
    print(EpsConfig.get_last_eps_in_database())
