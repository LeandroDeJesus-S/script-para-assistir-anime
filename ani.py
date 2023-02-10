#!/usr/bin/env python3
import colorama
import logging as log
from dataupdate import up
from config import argscfg, utils
from config.arguments import W, S, E, ADD, NEW, SH, LA, LE, UPDATE, FETCH

log.basicConfig(filename='logs.log', filemode='w',
                format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                level=log.DEBUG, encoding='utf-8')

colorama.init()
up.Updater.make_updates()

if W and not S and not E:
    argscfg.Arguments.watch(W)

elif W and S or E:
    argscfg.Arguments.watch_season_ep(W, str(S), str(E))
    
elif ADD:
    if utils.is_accessible(ADD['url']):
        argscfg.Arguments.add_anime(ADD['anime'], ADD['url'])

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
