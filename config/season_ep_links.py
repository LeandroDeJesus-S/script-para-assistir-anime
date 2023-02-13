import requests as rq
from bs4 import BeautifulSoup

class SeasonEp:
    def __init__(self, anime_homepage) -> None:
        self.anime_homepage = anime_homepage
        self.html = self.get_homepage_anime_content()
    
    def get_homepage_anime_content(self):
        resp = rq.get(self.anime_homepage).content
        return BeautifulSoup(resp, 'html.parser')


    def get_eps(self) -> list[str]:
        """retorna uma lista com o numero dos episodios"""
        
        eps = []
        for i in self.html.select('a'):
            if 'Episodio' not in i.text or len(i.text.split()) < 2:
                continue

            ep = i.text.split()[1]
            ep
            eps.append(ep)

        return eps


    def formatted_seasons(self) -> list[dict[str: list[str]]]:
        """retorna uma lista de dicionarios com a chave 'season %(num)s' e uma lista dos eps da temporada"""
        temp = ''
        for ep in self.get_eps():
            temp += f' {ep}'

        seasons = temp.split(' 1 ')
        x = []
        for i, e in enumerate(seasons):
            e = e.split()
            e.insert(0, '1')
            x.append({f'season {i}': e})
        return x[1:]


    def get_ep_links(self) -> list[str]:
        """retorna uma lista com os links dos episodios"""
        
        links = []
        for i in self.html.select('a'):
            if 'Episodio' not in i.text:
                continue
            links.append(i.get('href'))
        return links[2:]


    def formatted_ep_links(self):    
        c_links = 0
        links_by_seasons = []
        for se in self.formatted_seasons():
            eps = se.values()
            temp = []
            for f in range(len(*eps)):
                temp.append(self.get_ep_links()[c_links])
                c_links += 1
            links_by_seasons.append(temp.copy())
            temp.clear()
        
        return links_by_seasons


    def link_to_season_ep(self, ep, se=1):
        link = self.formatted_ep_links()
        return link[se - 1][ep -1]

    def link_to_new(self, ep, se=1):
        link = self.formatted_ep_links()
        return link[se - 1][ep -1]
        