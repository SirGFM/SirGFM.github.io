
from generator.page import PageWriter
from generator.gameListHelper import GetGameList, InsertGameIcons

class Page(PageWriter):
    """Page with every game for a non-LDJAM entry"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        # Create a list with all required JSON files by this page
        self.ggj_list = GetGameList('src/game/ggj/')
        self._1gam_list = GetGameList('src/game/1gam/')

        self.json_list = []
        # Create a single list with every JSON path
        for item in self.ggj_list:
            self.json_list.append(item)
        for item in self._1gam_list:
            self.json_list.append(item)

        super(Page, self).__init__(title='OTHER JAMS', url='/jam', nav=nav, has_game_overlay=True)

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css', 'icon.css', 'game_description.css'],
            script_list=['mouseover.js', 'game_description.js'],
            json_list=self.json_list)

    def insert_content(self):
        """Insert the content of the page"""
        self.write_content('h1', 'Other Jams', style='content')
        self.write_content('p', 'List of games I\'ve made for various other jams.', style='content')

        self.write_content('h2', 'Global Game Jam', style='content')
        InsertGameIcons(self, self.ggj_list)

        self.write_content('h2', 'One Game a Month', style='content')
        InsertGameIcons(self, self._1gam_list)

        self.write_content('h2', 'CampJam', style='content')

        self.write_content('h2', 'Other Jams', style='content')
        self.write_content('p', 'This category has games from jams that I haven\'t taken part of enough '
                'event to warrantry their own separated categories.', style='content')

