import argparse as ap
from .help_messages import *


def get_arg_or_empty_str(arg) -> str:
    return arg[0] if arg else ''


cli = ap.ArgumentParser(usage=MAIN_HELP_MSG)

cli.add_argument('-w', nargs=1, type=str, metavar='[ANM]', help=W_HELP)
cli.add_argument('-s', nargs=1, type=int, metavar='[SE]', help=S_HELP)
cli.add_argument('-e', nargs=1, type=int, metavar='[EP]', help=E_HELP)
cli.add_argument('-add', nargs=2, type=str, metavar=('[ANM]', '[URL]'), help=ADD_HELP)
cli.add_argument('-sh', action='store_true', help=SH_HELP)
cli.add_argument('-le', action='store_true', help=LE_HELP)
cli.add_argument('-la', action='store_true', help=LA_HELP)
cli.add_argument('-new', nargs=1, type=str, metavar='[ANM]', help=NEW_HELP)
cli.add_argument('--update', action='store_true', help=UPDATE_HELP)
cli.add_argument('--fetch', nargs=1, type=str, metavar='[ANM]', help=FETCH_HELP)
cli.add_argument('--history', action='store_true', help=None)
args = cli.parse_args()

W = get_arg_or_empty_str(args.w)
NEW = get_arg_or_empty_str(args.new)
S = get_arg_or_empty_str(args.s)
E = get_arg_or_empty_str(args.e)
ADD = {'anime': args.add[0], 'url': args.add[1]} if args.add else ''
SH = args.sh
LA = args.la
LE = args.le
UPDATE = args.update
FETCH = get_arg_or_empty_str(args.fetch)
HISTORY = args.history
