from .base_class import AnimesBrBase
from termcolor import cprint

class AnimesBrEpisode(AnimesBrBase):
    def __init__(self):
        super().__init__()
        
    def show_episodes(self, limit=None):
        """mostra os episódios mais recentes. 
        """
        episodes = self.get_episodes()  
        if limit is not None:
            episodes = self.get_episodes()[:limit]
            
        for ep in episodes:
            ep_out = f"{ep['name']}  {ep['ep']}"
            if ep['name'] in self.new_episodes():
                cprint(ep_out, 'magenta')
                continue
            cprint(ep_out, 'white')
    
    def add_eps_to_database(self):
        self.db.connect_db()
        
        animes_ep = self.get_episodes()
        for anime in animes_ep:
            ep_num = int(float(anime['ep']))
            self.db.save_in_database(
                self.EPISODES_TABLE, self.EPISODE_FIELDS, 
                (None, anime['name'], ep_num)
            )
        
        self.db.close_db()
        
    def episodes_in_database(self):
        self.db.connect_db()  
        episodes = self.db.get_all_data(self.EPISODES_TABLE)
        self.db.close_db()
        return episodes
    
    def new_episodes(self):
        eps_in_db = self.episodes_in_database()
        ep_names_from_db = {i[1]: i[2] for i in eps_in_db}
        eps = self.get_episodes()
        news = []
        for ep in eps:  # TODO: resolver problem de eps ja na db
            ep_name_not_in_database = ep['name'] not in ep_names_from_db
            ep_num_is_most_recent = ep['name'] in eps_in_db and int(float(ep['ep'])) > ep_names_from_db[ep['name']]
            # print('EP SITE:', ep['name'], ep['ep'], 'EP DB:', ep_names_from_db[ep['name']])
            if ep_name_not_in_database or  ep_num_is_most_recent:
                news += [ep['name']]
        
        print(news)
        return news
    
    def most_recent(self): # TODO: most_recent function
        ...
