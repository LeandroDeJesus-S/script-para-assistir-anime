#!/usr/bin/env python3
import colorama
import logging as log
from dataupdate import up
from config import argscfg, utils
from config.arguments import *
from config import history

log.basicConfig(filename='logs.log', filemode='w',
                format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                level=log.DEBUG, encoding='utf-8')

colorama.init()
up.Updater.make_updates()

if W and not S and not E:
    argscfg.Arguments.watch(W)

elif W and S or E:
    argscfg.Arguments.watch_season_ep(W, S, E)
    
elif ADD:
    if utils.is_accessible(ADD['url']):
        argscfg.Arguments.add_anime(ADD['anime'], ADD['url'])
    else:
        print('Não foi possivel adicionar o anime, url inválida ou não acessivel.')

elif NEW:
    argscfg.Arguments.new(NEW)
    
elif SH:
    argscfg.Arguments.site_home()
    
elif LA:
    argscfg.Arguments.last_animes()
    
elif LE:
    argscfg.Arguments.last_episodes()

elif UPDATE:
    up.Updater.make_manual_updates()

elif FETCH:
    argscfg.Arguments.fetch_animes(FETCH)

elif HISTORY:
    history.History.show_history()
