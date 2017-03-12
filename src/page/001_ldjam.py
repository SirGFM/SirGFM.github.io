
from os import listdir
from os.path import isfile, join
from generator.page import PageWriter
from generator.gameIcon import GameWriter

class Page(PageWriter):
    """Page with every LDJam entry"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        # Create a list with all required JSON files by this page
        self.json_list = []
        for f in listdir('src/game/ldjam/'):
            path = join('src/game/ldjam/', f)
            if not isfile(path):
                continue
            elif not path.endswith('.json'):
                continue
            self.json_list.append(path)

        super(Page, self).__init__(title='LDJAM', url='/ldjam', nav=nav)

    def insert_content(self):
        """Insert the content of the page"""
        self.write_content('p', 'Here you\'ll find every game I\'ve made for ' +
                '<a href="http://www.ludumdare.com/" >Ludum Dare</a>, a 48h-72h game jam.',
                style='content')
        for path in self.json_list:
            GameWriter(path).insert(self)

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css', 'icon.css'], script_list=['mouseover.js'], json_list=self.json_list)

