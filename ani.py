import argparse as ap
from config import argscfg, utils
from dataupdate import up
import colorama
from sys import argv
import logging as log

log.basicConfig(filename='logs.log', filemode='w',
                format='%(asctime)s - %(levelname)s - %(filename)s : %(message)s',
                level=log.DEBUG, encoding='utf-8')

colorama.init()
up.Updater.make_updates()
HELP_MSG = f"""
{argv[0]}\t[-w [ANM] [-s [SE] ] [-e [EP] ] ]
\t[-add [ANM] [URL]]
\t[-new [ANM]]
\t[-sh]
\t[-la]
\t[-le]
""".expandtabs(20)
cli = ap.ArgumentParser(usage=HELP_MSG)

W_HELP = 'leva para a pagina inicial do anime'
S_HELP = 'passa uma temporada especifica'
E_HELP = 'passa um episódio especifico'
ADD_HELP = 'adiciona um novo anime'
SH_HELP = 'Leva a pagina inicial do site'
LE_HELP = 'Lista os ultimos episódios lançados'
LA_HELP = 'Lista os ultimos animes lançados'
NEW_HELP = 'Leva ao episódio mais recente do anime passado'

cli.add_argument('-w', nargs=1, type=str, metavar='[ANM]', help=W_HELP)
cli.add_argument('-s', nargs=1, type=int, metavar='[SE]', help=S_HELP)
cli.add_argument('-e', nargs=1, type=int, metavar='[EP]', help=E_HELP)
cli.add_argument('-add', nargs=2, type=str, metavar=('[ANM]', '[URL]'), help=ADD_HELP)
cli.add_argument('-sh', action='store_true', help=SH_HELP)
cli.add_argument('-le', action='store_true', help=LE_HELP)
cli.add_argument('-la', action='store_true', help=LA_HELP)
cli.add_argument('-new', nargs=1, type=str, metavar='[ANM]', help=NEW_HELP)
args = cli.parse_args()

def get_arg_or_empty_str(arg) -> str:
    return arg[0] if arg else ''

W = get_arg_or_empty_str(args.w)
NEW = get_arg_or_empty_str(args.new)
S = get_arg_or_empty_str(args.s)
E = get_arg_or_empty_str(args.e)
ADD = {'anime': args.add[0], 'url': args.add[1]} if args.add else ''
SH = args.sh
LA = args.la
LE = args.le

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
