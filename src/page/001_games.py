
from generator.page import PageWriter
from generator.gameListHelper import GetGameList, InsertGameIcons

class Page(PageWriter):
    """Page with every non-jam game I've made"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        self.json_list = GetGameList('src/game/non-jam/')
        super(Page, self).__init__(title='GAMES', url='/games', nav=nav, has_game_overlay=True)

    def insert_content(self):
        """Insert the content of the page"""
        self.write_content('h1', 'Games', style='content')
        self.write_content('p', 'List of games I\'ve made outside game jams. Those games comes '
                'in two types: simple post-jam versions of game jam entries and "complete*" games.',
                style='content')
        self.write_content('p', 'Usually, my deadlines for post-jam versions are until the next '
                'game jam. For Ludum Dare entries, that would be around 4 months (minus the time '
                'spent rating games).', style='content')
        self.write_content('p', '"Complete" games are those not directly created based on a game '
                'jam entry. The mechanic may be based on a jam entry, but the game itself is a '
                'completely separated work (usually not sharing any code or asset previously made '
                'for a jam).', style='content')
        self.write_content('p', 'Also, I may take breaks from these projects to do other stuff '
                '(like this site or to take part of yet another game jam...). To ensure do I '
                'eventually release them, I usually set a competition as the deadline (like '
                '<a href=\"www.bigfestival.com.br/\">BIG Festival</a>).', style='content')

        InsertGameIcons(self, self.json_list)

        self.write_content('p', '* <strong>Note:</strong> I only wronte "complete" because I '
                'consider any game in this page, one way or another, as complete... even the most '
                'broken ones...', style='content')

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css', 'icon.css', 'game_description.css'],
            script_list=['mouseover.js', 'game_description.js'],
            json_list=self.json_list)

