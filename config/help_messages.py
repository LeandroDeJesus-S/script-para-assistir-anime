from sys import argv

MAIN_HELP_MSG = f"""
{argv[0]}\t[-w [ANM] [-s [SE] ] [-e [EP] ] ]
\t[-add [ANM] [URL]]
\t[-new [ANM]]
\t[-sh]
\t[-la]
\t[-le]

\t[--fetch [ANM]]
\t[--update]
\t[--history]
""".expandtabs(20)

W_HELP = 'leva para a pagina inicial do anime'
S_HELP = 'passa uma temporada especifica'
E_HELP = 'passa um episódio especifico'
ADD_HELP = 'adiciona um novo anime'
SH_HELP = 'Leva a pagina inicial do site'
LE_HELP = 'Lista os ultimos episódios lançados'
LA_HELP = 'Lista os ultimos animes lançados'
NEW_HELP = 'Leva ao episódio mais recente do anime passado'
UPDATE_HELP = 'Atualiza os eps e animes da base de dados manualmente'
FETCH_HELP = 'Busca animes salvos na base de dados'
HISTORY_HELP = 'Mostra o historico com o anime ep e temporada registrados'
