
import json
import defer
from datetime import date

class Game:
    def __init__(self, json_file):
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
        # TODO Create this default image on img/game/icon/
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

class GameWriter:
    def __init__(self, json_file):
        self._game = Game(json_file)
        self._fp = None
        self._indent = 0

    def set_game(self, game):
        self._game = game

    def set_output(self, fp):
        """Set the current output file"""
        self._fp = fp

    def tab(self):
        """Increase the indentation"""
        self._indent += 1

    def untab(self):
        """Decrease the indentation"""
        self._indent -= 1
        if self._indent < 0:
            self._indent = 0

    def write(self, string, do_break=True):
        """Write an indented component at the stored file

        string -- String component to be written
        do_break -- Whether a new line should be added after the component
        """
        self._fp.write('    ' * self._indent)
        self._fp.write(string)
        if do_break:
            self._fp.write('\n')

    def write_content(self, tag, string, style=None):
        """Write an auto-contained (i.e., a paragraph) content

        tag -- Content's HTML tag
        string -- String component to be written
        style -- CSS class to be used with the tag
        """
        if style is not None:
            self.write('<{} class="{}"> {} </{}>'.format(tag, style, string, tag))
        else:
            self.write('<{}> {} </{}>'.format(tag, string, tag))

    def insert_repo(self):
        """Insert a image linked to the repository. If no URL was specified, this functions does nothing"""
        if not self._game.has_repo():
            return
        self.write('<a href="{}" title="Clone the game\'s source">'.format(self._game.repo()))
        self.tab()
        self.write('<img id="{}-repo-img" class="gamebutton" src="/img/button/GitHub-Mark-32px.png">'
                   '</img>'.format(self._game.id()))
        self.untab()
        self.write('</a>')

    def insert(self, fp):
        """Insert this component (game icon + description) into a page
        
        fp -- The output file
        """
        defer_ = defer.Defer()
        self.set_output(fp)
        self.write('<div id="{}" class="gamelisting" onclick="ShowGameDesc(this)">'.format(self._game.id()))
        defer_.push(lambda :self.write('</div> <!-- {} gamelisting -->'.format(self._game.id())))
        defer_.push(self.untab)
        self.tab()

        self.insert_icon(fp)
        self.insert_description(fp)

        defer_.run()

    def insert_icon(self, fp):
        """Insert this component's icon into a page
        
        fp -- The output file
        """
        defer_ = defer.Defer()

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

    def insert_description(self, fp):
        """Insert this component's description
        
        fp -- The output file
        """
        defer_ = defer.Defer()

        self.write('<div id="{}-desc" class="gamedesc-hidden">'.format(self._game.id()))
        defer_.push(lambda: self.write('</div> <!-- {}-desc -->'.format(self._game.id())))
        defer_.push(self.untab)
        self.tab()

        self.write_content('h1', self._game.title(), style='gamedesc')
        if self._game.has_event():
            self.write_content('h2', 'Made for {}'.format(self._game.event()), style='gamedesc')
        if self._game.was_released():
            self.write_content('h3', 'Published: {}'.format(self._game.release_date()), style='gamedesc')
        else:
            self.write_content('h3', 'Release Date: {}'.format(self._game.release_date()), style='gamedesc')

        self.write_content('p', self._game.short_desc(), style='gamedesc')

        # TODO Download link

        self.insert_repo()

        defer_.run()

