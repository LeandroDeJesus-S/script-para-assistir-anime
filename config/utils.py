import logging as log


def is_accessible(url: str) -> bool:
    import requests
    from config.cor import Color

    log.debug(f'is_accessible > url : {url}')
    try: 
        is_valid = requests.get(url).status_code == 200
        log.debug(f'is_accessible > is_valid : {is_valid}')
    except requests.exceptions.MissingSchema as exp:
        msg = Color.red('Erro. Formato de url invalido...')
        print(msg)
        log.debug(f'is_accessible > Exception : {exp}')
        return False
    except requests.exceptions.ConnectionError as exp:
        msg = Color.red('Erro de conexão, por favor verifique sua internet...')
        print(msg)
        log.debug(f'is_accessible > Exception : {exp}')
        return False
    else:
        return is_valid


def is_season(arg: str) -> bool:
    validation = arg == '-s'
    log.debug(f'is_season > arg : {arg}')
    log.debug(f'is_season > validation : {validation}')
    return validation


def is_episode(arg: str) -> bool:
    validation = arg == '-e'
    log.debug(f'is_episode > arg : {arg}')
    log.debug(f'is_episode > validation : {validation}')
    return validation


def is_argument(arg: str, value: str) -> bool:
    validation = arg == value
    log.debug(f'is_argument > arg : {arg} | value : {value}')
    log.debug(f'is_argument > validation : {validation}')
    return validation


def get_arg(arg, arg_num: int) -> str:
    log.debug(f'get_arg > arg : {arg} | arg_num : {arg_num}')
    try: 
        argument_getter = arg[arg_num]
    except IndexError as exp: 
        log.debug(f'get_arg > Exception : {exp} | args sent : {arg[1:]} | arg_called : {arg_num}')
        return ''
    else:
        log.debug(f'get_arg > argument_getter : {argument_getter}')
        return argument_getter


def valid_season_ep_value(arg, value):
    """
    verifica se o argumento foi passado e se ele é numerico

    arg: recebe o argumento com o parametro
    value: recebe o argumento do parametro
    :return: True se for valido ou False se não for
    """
    from config.cor import Color
    
    log.debug(f'valid_season_ep_value > arg : {arg} | value : {value}')
    if not value:
        msg = f'o argumento não foi enviado para {arg}'
        print(Color.red(msg))
        log.debug(f'valid_season_ep_value > {msg}')
        return False
    if not value.isnumeric():
        msg = f'o argumento para {arg} é inválido'
        print(Color.red(msg))
        log.debug(f'valid_season_ep_value > {msg}')
        return False

    log.debug('is_valid_season_ep_value > True')
    return True
