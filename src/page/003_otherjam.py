
from os import listdir
from os.path import isfile, join
from generator.page import PageWriter
from generator.gameIcon import GameWriter

def getGameList(dirPath):
    """Retrieve the list of JSON files within a given directory
    
    dirPath -- The inspected directory
    """
    _list = []
    for f in listdir(dirPath):
        path = join(dirPath, f)
        if not isfile(path):
            continue
        elif not path.endswith('.json'):
            continue
        _list.append(path)
    _list.reverse()

    return _list

class Page(PageWriter):
    """Page with every game for a non-LDJAM entry"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        # Create a list with all required JSON files by this page
        self.ggj_list = getGameList('src/game/ggj/')

        self.json_list = []
        # Create a single list with every JSON path
        for item in self.ggj_list:
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
        self.write_content('p', 'List of games I\'ve made for various jams.', style='content')

        self.write_content('h2', 'Global Game Jam', style='content')
        for path in self.ggj_list:
            GameWriter(path).insert(self)

        self.write_content('h2', 'One Game a Month', style='content')

        self.write_content('h2', 'CampJam', style='content')

        self.write_content('h2', 'Other Jams', style='content')
        self.write_content('p', 'This category has games from jams that I haven\'t taken part of enough '
                'event to warrantry their own separated categories.', style='content')

