import argparse as ap
from .help_messages import *
from conf import conf

def get_arg_or_empty_str(arg) -> str:
    return arg[0] if arg else ''

def get_arg_or_none(arg):
    return arg[0] if arg else None


cli = ap.ArgumentParser(usage=MAIN_HELP_MSG)

cli.add_argument('-w', nargs=1, type=str, metavar='[ANM]', help=W_HELP)
cli.add_argument('-s', nargs=1, type=int, metavar='[SE]', help=S_HELP)
cli.add_argument('-e', nargs=1, type=int, metavar='[EP]', help=E_HELP)
cli.add_argument('-add', nargs=2, type=str, metavar=('[ANM]', '[URL]'), help=ADD_HELP)
cli.add_argument('-sh', action='store_true', help=SH_HELP)
cli.add_argument('-le', action='store_true', help=LE_HELP)
cli.add_argument('-l', nargs=1, type=int, metavar='[LIMIT]', help=L_HELP)
cli.add_argument('-la', action='store_true', help=LA_HELP)
cli.add_argument('-new', nargs=1, type=str, metavar='[ANM]', help=NEW_HELP)

cli.add_argument('--update', action='store_true', help=UPDATE_HELP)
cli.add_argument('--fetch', nargs=1, type=str, metavar='[ANM]', help=FETCH_HELP)
cli.add_argument('--history', action='store_true', help=HISTORY_HELP)
cli.add_argument('--filname', nargs=1, type=str, help=None)
cli.add_argument('--list-websites', action='store_true', help=LIST_WEBSITES_HELP)
cli.add_argument('--set-website', nargs=1, type=str, help=SET_WEBSITE_HELP, metavar='[site_name]')
cli.add_argument('--createsite', nargs=1, type=str, metavar='[site_name]', help=CREATESITE_HELP)

args = cli.parse_args()

W = get_arg_or_empty_str(args.w)
NEW = get_arg_or_empty_str(args.new)
S = get_arg_or_none(args.s)
E = get_arg_or_none(args.e)
ADD = {'anime': args.add[0], 'url': args.add[1]} if args.add else None
SH = args.sh
LA = args.la
LE = args.le
L = get_arg_or_none(args.l)
UPDATE = args.update
FETCH = get_arg_or_empty_str(args.fetch)
HISTORY = args.history if not isinstance(args.history, list) else args.history[0]
FILNAME = get_arg_or_empty_str(args.filname)
LIST_WEBSITES = args.list_websites
SET_WEBSITE = get_arg_or_none(args.set_website)
CREATESITE = get_arg_or_none(args.createsite)

arguments = conf.Arguments()
limit = None
if W and not S and not E:
    arguments.watch(W.lower())

elif W and S or E:
    arguments.watch_season_ep(W.lower(), S, E)

elif ADD:
    anime, url = ADD.values()
    arguments.add_anime(anime.lower(), url)
    
elif SH:
    arguments.site_home()
    
elif LE:
    if L:
        limit = L
    arguments.list_episodes(limit)
    
elif LA:
    if L:
        limit = L
    arguments.list_animes(limit)
    
elif NEW:
    arguments.new(NEW.lower())

elif UPDATE:
    pass

elif FETCH:
    pass

elif HISTORY:
    fil = None
    if L:
        limit = L
    if FILNAME:
        fil = FILNAME.lower()
    arguments.history(limit, fil)

elif LIST_WEBSITES:
    arguments.list_websites()

elif SET_WEBSITE:
    arguments.set_website(SET_WEBSITE)

elif CREATESITE:
    arguments.createsite(CREATESITE)
