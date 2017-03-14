
from generator.page import PageWriter
from generator.gameListHelper import GetGameList, InsertGameIcons

class Page(PageWriter):
    """Page with every LDJam entry"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        self.json_list = GetGameList('src/game/ldjam/')
        super(Page, self).__init__(title='LDJAM', url='/ldjam', nav=nav, has_game_overlay=True)

    def insert_content(self):
        """Insert the content of the page"""
        self.write_content('h1', 'Ludum Dare', style='content')
        self.write_content('p', 'List of games I\'ve made for <a href="http://www.ludumdare.com/" >Ludum Dare</a>'
                ', a 48h-72h game jam.', style='content')
        InsertGameIcons(self, self.json_list)

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css', 'icon.css', 'game_description.css'],
            script_list=['mouseover.js', 'game_description.js'],
            json_list=self.json_list)

