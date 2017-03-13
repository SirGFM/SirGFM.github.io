
import json
from generator.baseWriter import BaseWriter
from generator.defer import Defer

from datetime import date

class Game(object):
    """Wraps a game that may be inserted as an icon, that may have its own page and stuff"""

    def __init__(self, json_file):
        """Initialize a new game from a JSON file

        json_file -- Name of the JSON file for the game
        """
        # TODO Try-except this
        fp = open(json_file, 'rt')
        self._decoded = json.load(fp)
        fp.close()

    def id(self):
        """Try to retrieve the component's ID"""
        try: return self._decoded['id']
        except: return 'no-id'

    def icon(self):
        """Try to retrieve the component's icon (must be located at img/game/icon/)"""
        try: return self._decoded['image']
        except: return 'no_image.png'

    def title(self):
        """Try to retrieve the component's title"""
        try: return self._decoded['title']
        except: return 'No Title'

    def release_date(self):
        """Try to retrieve the component's release date"""
        try: return self._decoded['release_date']
        except: return 'No release date'

    def was_released(self):
        """Check if the game has been released (i.e., if the release date is in the past)"""
        today = date.today().isoformat().split('-')
        release_date = self.release_date().split('-')
        return today[0] > release_date[0] or today[1] > release_date[1] or today[2] > release_date[2]

    def event(self):
        """Try to retrieve the component's event"""
        try:
            if 'event_edition' in self._decoded:
                return '{} {}'.format(self._decoded['event'], self._decoded['event_edition'])
            else:
                return self._decoded['event']
        except: return 'No Event'

    def has_event(self):
        """Check if the game has a listed event"""
        return 'event' in self._decoded

    def repo(self):
        """Try to retrieve the component's source code URL"""
        try: return self._decoded['source_code']
        except: return 'No source'

    def has_repo(self):
        """Check if the game has a listed repository"""
        return 'source_code' in self._decoded

    def short_desc(self):
        """Try to retrieve the component's short description"""
        try: return self._decoded['short_description']
        except: return 'No short description'

    def is_on_itchio(self):
        """Check if the game is available through Itch.io"""
        try: return 'itch.io' in self._decoded['distribution']
        except: return False

    def is_on_directlink(self):
        """Check if the game is available through a direct link"""
        try: return 'direct_link' in self._decoded['distribution']
        except: return False

    def directlink_platforms(self):
        """Try to retrieve the component's downlod URL for each platform"""
        try: return self._decoded['distribution']['direct_link']
        except: return {'No platform': 'No_url'}

    def itch_link(self):
        """Try to retrieve the component's Itch.io URL"""
        try: return self._decoded['distribution']['itch.io']['url']
        except: return 'No Itch.io URL'

    def itch_platforms(self):
        """Try to retrieve the component's list of available platforms (on Itch.io)"""
        try:
            plat = self._decoded['distribution']['itch.io']['platforms']
            if len(plat) <= 1:
                return plat
            else:
                return ', '.join(plat[:-1]) + ' and ' + plat[-1]
        except: return 'No platform'

class GameWriter(BaseWriter):
    """Writes HTML for 'Game's objects"""

    def __init__(self, json_file):
        """Create a new writer for a game

        json_file -- Name of the JSON file for the game
        """
        super(GameWriter, self).__init__()
        try:
            self._game = Game(json_file)
        except Exception:
            print "Failed to parse {}".format(json_file)
            raise

    def set_game(self, game):
        """Set the writer's game

        game -- The game
        """
        self._game = game

    def insert(self, page):
        """Insert this component (game icon + description) into a page
        
        page -- The writer of the current page
        """
        defer_ = Defer()
        self.set_indent(page.get_indent())
        self.set_output(page.get_output())

        self.write('<div id="{}" class="gamelisting" '
                   'onclick="SetGameDescription(this); ToggleGameDescriptionVisibility()">'.format(self._game.id()))
        defer_.push(lambda :self.write('</div> <!-- {} gamelisting -->'.format(self._game.id())))
        defer_.push(self.untab)
        self.tab()

        self.insert_icon()

        defer_.run()

    def insert_icon(self):
        """Insert this component's icon into a page"""
        defer_ = Defer()

        self.write('<div id="{}-icon" class="gameicon" onmouseover="ShowGameDetails(this)" '
                   'onmouseout="HideGameDetails(this)" '
                   'style="background-image:url(\'/img/game/icon/{}\')">'.format(self._game.id(), self._game.icon()))
        defer_.push(lambda: self.write('</div> <!-- {}-icon -->'.format(self._game.id())))
        defer_.push(self.untab)
        self.tab()

        self.write('<div id="{}-overlay" class="gameiconoverlay">'.format(self._game.id()))
        defer_.push(lambda: self.write('</div> <!-- {}-overlay -->'.format(self._game.id())))
        defer_.push(self.untab)
        self.tab()

        self.write('<div id="{}-inner-title" class="gameicontitle noselect" >'.format(self._game.id()))
        defer_.push(lambda: self.write('</div> <!-- {}-inner-title -->'.format(self._game.id())))
        defer_.push(self.untab)
        self.tab()

        # NOTE: This headding inherits its color/formatting from its parent div
        self.write_content('h1', self._game.title())

        defer_.run()

