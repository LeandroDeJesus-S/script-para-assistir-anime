from .base_class import AnimesBrBase
from termcolor import colored


class AnimesBrAnime(AnimesBrBase):
    def __init__(self):
        super().__init__()
        
    def show_animes(self, limit: str=None):
        animes_and_rate = self.get_anime_and_rate()
        if limit is not None:
            animes_and_rate = self.get_anime_and_rate()[:limit]
            
        for anime in animes_and_rate:
            print(self.highlight_anime(anime['name'], anime['rate']))
    
    def highlight_anime(self, name, rate) ->  str:
        old_animes = [i[1] for i in self.get_animes_in_db()]
        if name not in old_animes:
            name = colored(name, 'light_magenta')
        else:
            name = colored(name, 'white')
            
        try:
            float_rate = float(rate)
            if float_rate >= 9:
                rate = colored(rate, 'magenta')
            
            elif float_rate >= 7:
                rate = colored(rate, 'green')
                
            elif float_rate >= 5:
                rate = colored(rate, 'yellow')
            
            else:
                rate = colored(rate, 'red')
            return f'{name} | {rate}'
                
        except ValueError:
            return f'{name} {rate}'
        
    def get_animes_in_db(self):
        self.db.connect_db()
        
        data = self.db.get_all_data(self.ANIMES_TABLE)
        
        self.db.close_db()
        return data
        
    def add_animes_to_database(self):
        self.db.connect_db()
        
        animes_ep = self.get_anime_and_rate()
        for anime in animes_ep:
            rate = anime['rate']
            rate = float(rate) if rate else 0
            self.db.save_in_database(
                self.ANIMES_TABLE, self.ANIME_FIELDS, 
                (None, anime['name'], rate)
            )
        
        self.db.close_db()
