import sys
import colorama
from config import utils
from config.argscfg import Arguments
from animes_scrapping.animesonline import AnimesOnline
from config.cor import Color
import requests.exceptions
import logging as log
from dataupdate import up

log.basicConfig(filename='logs.log', filemode='w',
                format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                level=log.DEBUG, encoding='utf-8')
colorama.init()
up.update_data()
ARGS = sys.argv
HELP_MSG = """
-w [anime]                                      leva para a pagina inicial do anime
           -s [season]                          leva para a temporada especifica
           -e [episode]                         leva para o episodio especifico do anime

-add [anime] [url home]                         adiciona um nova anime na base de dados

-new [anime]                                    leva para o episodio mais recente do anime

-le                                             lista os ultimos episodios lançados

-la                                             lista os ultimos animes lançados

-sh                                             leva a pagina inicial do site animesonline
"""

try:
    FIRST_ARG = utils.get_arg(ARGS, 1)
    SECOND_ARG = utils.get_arg(ARGS, 2)
    THIRD_ARG = utils.get_arg(ARGS, 3)
    FOURTH_ARG = utils.get_arg(ARGS, 4)
    FIFTH_ARG = utils.get_arg(ARGS, 5)
    SIXTH_ARG = utils.get_arg(ARGS, 6)

    NUM_ARGS_SENT = len(ARGS)
    ONE_ARG_WAS_SENT = NUM_ARGS_SENT == 2
    TWO_ARGS_WAS_SENT = NUM_ARGS_SENT == 3
    THREE_ARGS_WAS_SENT = NUM_ARGS_SENT == 4
    FOUR_ARGS_WAS_SENT = NUM_ARGS_SENT == 5
    SIX_ARGS_WAS_SENT = NUM_ARGS_SENT == 7

    ep = season = url = is_valid_url = is_valid_season = ''
    FIRST_ARG_IS_LE = utils.is_argument(FIRST_ARG, '-le')
    FIRST_ARG_IS_LA = utils.is_argument(FIRST_ARG, '-la')
    FIRST_ARG_IS_SH = utils.is_argument(FIRST_ARG, '-sh')
    FIRST_ARG_IS_HELP = utils.is_argument(FIRST_ARG, '--help')
    FIRST_ARG_IS_W = utils.is_argument(FIRST_ARG, '-w')
    FIRST_ARG_IS_ADD = utils.is_argument(FIRST_ARG, '-add')
    FIRST_ARG_IS_NEW = utils.is_argument(FIRST_ARG, '-new')

    FIFTH_ARG_SENT_IS_EP = utils.is_argument(FIFTH_ARG, '-e')
    FIFTH_ARG_SENT_IS_SEASON = utils.is_argument(FIFTH_ARG, '-s')
    FIFTH_ARG_IS_EP = FIRST_ARG_IS_W and FIFTH_ARG_SENT_IS_EP
    FIFTH_ARG_IS_SEASON = FIRST_ARG_IS_W and FIFTH_ARG_SENT_IS_SEASON

    THIRD_ARG_IS_SEASON = utils.is_season(THIRD_ARG)
    THIRD_ARG_IS_EPISODE = utils.is_episode(THIRD_ARG)

    JUST_W_WAS_CALLED = FIRST_ARG_IS_W and TWO_ARGS_WAS_SENT
    W_S_E_WAS_CALLED = FIRST_ARG_IS_W and FOUR_ARGS_WAS_SENT or SIX_ARGS_WAS_SENT
    ADD_WAS_CALLED = FIRST_ARG_IS_ADD and THREE_ARGS_WAS_SENT
    NEW_WAS_CALLED = FIRST_ARG_IS_NEW and TWO_ARGS_WAS_SENT

    log.info(f'argumentos enviados: {ARGS[1:]}')
    
    if FIRST_ARG in ['-w', '-add', '-new']:

        ANIME_NAME = SECOND_ARG
        if not ANIME_NAME:
            msg = f'o nome do anime não foi enviado.'
            print(Color.red(msg))
            log.debug(msg)

        if FIRST_ARG_IS_ADD:
            url = THIRD_ARG
            is_valid_url = utils.is_accessible(url)
            if not is_valid_url:
                msg = 'url invalida ou não enviada'
                print(Color.red(msg))
                log.debug(msg)

            log.debug(f'-add anime : {ANIME_NAME} | url: {url}')
            log.debug(f'-add is_valid_url : {is_valid_url}')

        elif THIRD_ARG_IS_SEASON:
            is_valid_season = utils.valid_season_ep_value(THIRD_ARG, FOURTH_ARG)
            season = FOURTH_ARG if is_valid_season else ''

            log.debug(f'-s season : {FOURTH_ARG}')
            log.debug(f'-s is_valid_season : {is_valid_season}')

        elif THIRD_ARG_IS_EPISODE:
            is_valid_ep = utils.valid_season_ep_value(THIRD_ARG, FOURTH_ARG)
            ep = FOURTH_ARG if is_valid_ep else ''

            log.debug(f'-e ep : {FOURTH_ARG}')
            log.debug(f'-s is_valid_ep : {is_valid_ep}')

        elif FIFTH_ARG_IS_SEASON:
            is_valid_season = utils.valid_season_ep_value(FIFTH_ARG, SIXTH_ARG)
            season = SIXTH_ARG if is_valid_season else ''
            log.debug(f'fifth_arg_is_season > season : {season}')
            
        elif FIFTH_ARG_IS_EP:
            is_valid_ep = utils.valid_season_ep_value(FIFTH_ARG, SIXTH_ARG)
            ep = SIXTH_ARG if is_valid_ep else ''
            log.debug(f'fifth_arg_is_ep > ep : {ep}')

        if JUST_W_WAS_CALLED:
            Arguments.watch(ANIME_NAME)
            
        elif W_S_E_WAS_CALLED:
            Arguments.watch_season_ep(ANIME_NAME, season, ep)
            
        elif ADD_WAS_CALLED and is_valid_url:
            Arguments.add_anime(ANIME_NAME, url)
            
        elif NEW_WAS_CALLED:
            log.debug(f'{FIRST_ARG}: {SECOND_ARG}')
            Arguments.new(ANIME_NAME)

    elif FIRST_ARG_IS_LE:
        AnimesOnline.show_last_eps()
        
    elif FIRST_ARG_IS_LA:
        AnimesOnline.show_last_animes()
        
    elif FIRST_ARG_IS_SH:
        AnimesOnline.open_home_page()
        
    elif FIRST_ARG_IS_HELP:
        print(HELP_MSG)
        
    elif NUM_ARGS_SENT > 1:
        print(Color.yellow('argumentos inválidos. Para obter ajuda use: --help'))

except requests.exceptions.ConnectionError:
    msg = 'erro de conexão, verifique se você está conectado a internet'
    print(Color.red(msg))
    log.warning(msg)
    