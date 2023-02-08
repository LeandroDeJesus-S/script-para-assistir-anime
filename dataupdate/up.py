import logging as log
from database.animes_db import AnimesConfig
from database.episodes_db import EpsConfig


class Updater:
    time_file = 'dataupdate/timeupdate.txt'
    @classmethod
    def updatetime_in_timestamp(cls) -> float:
        from datetime import datetime

        with open(cls.time_file, 'r') as t:
            date_time = datetime.strptime(t.read(), '%Y-%m-%d %H:%M:%S.%f')
            finaltime_in_timestamp = date_time.timestamp()
            log.debug(f'get_time > date_time : {date_time} ')
            log.debug(f'get_time > finaltime_in_timestamp : {finaltime_in_timestamp}')
            return finaltime_in_timestamp

    @classmethod
    def passed_three_days(cls, timestamp) -> bool:
        from datetime import datetime, timedelta

        timestamp_to_date = datetime.fromtimestamp(timestamp)
        today = datetime.now()
        time_three_days_later = timestamp_to_date + timedelta(days=3)
        validation = True if today >= time_three_days_later else False

        log.debug(f'a_week_later > timestamp : {timestamp}')
        log.debug(f'a_week_later > timestamp_to_date : {timestamp_to_date}')
        log.debug(f'a_week_later > today : {today}')
        log.debug(f'a_week_later > time_three_days_later : {time_three_days_later}')
        log.debug(f'a_week_later > validation : {validation}')
        return validation

    @classmethod
    def update_time(cls) -> None:
        from datetime import datetime

        new_time = datetime.now()
        with open(cls.time_file, 'w') as ts:
            ts.write(str(new_time))
        log.debug(f'update_friday > new_friday : {new_time}')

    @classmethod
    def make_updates(cls):
        """atualiza os animes, episodios e registra a data das atualizações
        """
        timestamp = cls.updatetime_in_timestamp()
        three_days_later = cls.passed_three_days(timestamp)
        log.debug(f'update_data > timestamp : updatetime_in_timestamp : {timestamp}')
        log.debug(f'update_data > three_days_later : passed_three_days : {three_days_later}')
        if three_days_later:
            AnimesConfig.update_last_animes_database()
            log.info('Base de dados de animes atualizada')
            EpsConfig.update_last_eps_database()
            log.info('Base de dados de episodios atualizada')
            cls.update_time()
            log.info('Data para update atualizada')

    @classmethod
    def make_manual_updates(cls):
        AnimesConfig.update_last_animes_database()
        log.info('Base de dados de animes atualizada manualmente')
        EpsConfig.update_last_eps_database()
        log.info('Base de dados de episodios atualizada manualmente')
        cls.update_time()
        log.info('Data para update atualizada manualmente')

