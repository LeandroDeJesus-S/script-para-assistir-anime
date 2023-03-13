from . import anime_releases, episode_releases, anime
import webbrowser


class AnimesBr(episode_releases.AnimesBrEpisode, anime_releases.AnimesBrAnime, anime.Anime):
    def __init__(self):
        super().__init__()
        if not self.is_online:
            return
        
    def open_homepage(self):
        self.go_home()        

    def last_animes(self, limit: str=None):
        self.show_animes(limit)
        
    def last_episodes(self, limit: int = None):
        self.show_episodes(limit)
    
    def anime_home(self):
        self.go_anime_homepage()
        
    def go_to_most_recent_season_and_ep(self, anime):
        """redireciona para o ep e temp mais recente e retorna o numero da 
        temp e do ep

        Args:
            anime (str): nome do anime

        Returns:
            tuple: (season_num, ep_num)
        """
        self.anime_homepage = anime
        self.set_most_recent_data()
        webbrowser.open(self.most_recent_ep_link)
        return self.most_recent_season_num, self.most_recent_ep_num