import logging as log
from database.animes_db import AnimesConfig
from database.episodes_db import EpsConfig


def updatetime_in_timestamp() -> float:
    from datetime import datetime

    with open('dataupdate/friday.txt', 'r') as t:
        date_time = datetime.strptime(t.read(), '%Y-%m-%d %H:%M:%S.%f')
        finaltime_in_timestamp = date_time.timestamp()
        log.debug(f'get_time > date_time : {date_time} ')
        log.debug(f'get_time > finaltime_in_timestamp : {finaltime_in_timestamp}')
        return finaltime_in_timestamp


def a_week_later(timestamp) -> bool:
    from datetime import datetime, timedelta

    timestamp_to_date = datetime.fromtimestamp(timestamp)
    today = datetime.now()
    time_a_week_later = timestamp_to_date + timedelta(days=7)
    validation = True if today >= time_a_week_later else False

    log.debug(f'a_week_later > timestamp : {timestamp}')
    log.debug(f'a_week_later > timestamp_to_date : {timestamp_to_date}')
    log.debug(f'a_week_later > today : {today}')
    log.debug(f'a_week_later > time_a_week_later : {time_a_week_later}')
    log.debug(f'a_week_later > validation : {validation}')
    return validation


def update_time() -> None:
    from datetime import datetime

    new_time = datetime.now()
    with open('dataupdate/friday.txt', 'w') as ts:
        ts.write(str(new_time))
    log.debug(f'update_friday > new_friday : {new_time}')


def update_data():
    timestamp = updatetime_in_timestamp()
    passed_a_week = a_week_later(timestamp)
    log.debug(f'update_data > timestamp : updatetime_in_timestamp : {timestamp}')
    log.debug(f'update_data > passed_a_week_later : a_week_later : {passed_a_week}')
    if passed_a_week:
        AnimesConfig.update_last_animes_database()
        log.info('Base de dados de animes atualizada')
        EpsConfig.update_last_eps_database()
        log.info('Base de dados de episodios atualizada')
        update_time()
        log.info('Data para update atualizada')


