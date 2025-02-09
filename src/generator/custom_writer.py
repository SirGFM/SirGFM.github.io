
from os import path

# Some constants
PAGE_TITLE = 'GFM\'s Game Corner'
PAGE_KEYWORDS = 'gamedev'
PAGE_DESCRIPTION = 'GFM\'s homepage'
PAGE_AUTHOR = 'Gabriel Francisco Mandaji'
PAGE_ICON = '/favicon.ico?'
PAGE_FOOTER = '&copy;GFM (2025)'

class CustomWriter():
    """Encapsulates writes to the output file, so all classes do it from the same context"""

    def __init__(self, out, nav):
        self.setup(out, nav)

    def setup(self, out, nav):
        self._out = out
        self._nav_file = nav
        self._tab = 0
        self.game = {}
        self.style = []
        self.script = []

    def write(self, string, do_break=True):
        self._out.write('    ' * self._tab)
        self._out.write(string)
        if do_break:
            self._out.write('\n')

    def _write_tagged(self, open_tag, string, close_tag, do_break=True):
        self.write('<{}> {} </{}>'.format(open_tag, string, close_tag), do_break)

    def tab(self):
        self._tab += 1

    def untab(self):
        self._tab -= 1
        if self._tab < 0:
            self._tab = 0

    def write_tagged(self, tag, string, id='', do_break=True):
        if id is not None and len(id) > 0:
            self._write_tagged('{} id="{}"'.format(tag, id), string, tag, do_break)
        else:
            self._write_tagged(tag, string, tag, do_break)

    def write_classy(self, tag, style, string, id='', do_break=True):
        if id is not None and len(id) > 0:
            self._write_tagged('{} id="{}" class="{}"'.format(tag, id, style), string, tag, do_break)
        else:
            self._write_tagged('{} class="{}"'.format(tag, style), string, tag, do_break)

    def open_html_tag(self):
        """Open (i.e., write) the main HTML tag"""
        self.write('<!DOCTYPE html>')
        self.write('<html lang="en">')
        self.tab()

    def close_html_tag(self):
        """Close (i.e., write) the main HTML tag"""
        self.untab()
        self.write('</html>')

    def write_html_header(self):
        """Write the HTML header"""
        self.write('<head>')
        self.tab()
        self.write_tagged('title', PAGE_TITLE)
        self.write('<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1" />')
        self.write('<meta name="keywords" content="{}" />'.format(PAGE_KEYWORDS))
        self.write('<meta name="description" content="{}" />'.format(PAGE_DESCRIPTION))
        self.write('<meta name="author" content="{}" />'.format(PAGE_AUTHOR))
        self.write('<link rel="shortcut icon" href="{}" />'.format(PAGE_ICON))
        for style in self.style:
            self.write('<link rel="stylesheet" type="text/css" href="/style/{}" />'.format(style))
        for script in self.script:
            self.write('<script type="text/javascript" src="/script/{}"></script>'.format(script))
        for _list in self.game.values():
            for jfile in _list:
                filename = path.basename(jfile)
                filename = filename.replace('.json', '')
                self.write('<script type="application/json" id="{}-json">'.format(filename))
                self.tab()
                with open(jfile, 'rt') as f:
                    for line in f:
                        self.write(line, do_break=False)
                self.untab()
                self.write('</script>')
        self.untab()
        self.write('</head>')

    def write_sidebar(self):
        self.write('<div id="page-sidebar" class="sidebar">')
        self.tab()
        with open(self._nav_file, 'rt') as fp:
            for line in fp:
                if line == '' or line == '\n' or line.startswith('#'):
                    continue
                arr = line.split(', ')

                _title = arr[0]
                _url = arr[1]

                self.write('<a class="sidebar" href="{}"> {} </a>'.format(_url, _title))
        self.untab()
        self.write('</div> <!-- page-sidebar -->')

    def write_body_begin(self):
        """Write the static part of the beginning of the page's body"""
        self.write('<body>')
        self.tab()
        # Add the game overlay
        if len(self.game) > 0:
            self.write('<div id="floating-game-detail" class="game_description">')
            self.tab()
            self.write_classy('h1', 'game_description', 'None', id='detail-title')
            self.write_classy('h2', 'game_description', 'None', id='detail-jam-title')
            self.write_classy('div', 'game_description_content', 'None', id='detail-jam-content')
            self.write_classy('h2', 'game_description', 'None', id='detail-about-title')
            self.write_classy('div', 'game_description_content', 'None', id='detail-about')
            self.write_classy('h2', 'game_description', 'None', id='detail-download-title')
            self.write_classy('div', 'game_description_content', 'None', id='detail-download')
            # Inject the function through the class, by manually setting up the \"
            self.write_classy('p', 'close_game_description" onclick="HideGameDescription()"', 'Close', id='detail-close')
            self.untab()
            self.write('</div> <!-- floating-game-detail -->')
            self.tab()

        # Add the header
        if True:
            self.write('<div id="page-header" class="header">')
            self.write('<a class="header" href="/">')
            self.tab()
            self.write('<img class="header nearest-neighbor" src="/img/title/01_gfms.png"> </img>')
            self.write('<img class="header nearest-neighbor" src="/img/title/02_game.png"> </img>')
            self.write('<img class="header nearest-neighbor" src="/img/title/03_corner.png"> </img>')
            self.untab()
            self.write('</a>')

            self.write('<a class="header" href="https://github.com/SirGFM" title="Check out my projects on Github">')
            self.tab()
            self.write('<img class="socialbt" src="/img/button/GitHub-Mark-Light-32px.png"> </img>')
            self.untab()
            self.write('</a>')

            self.write('<a class="header" href="https://twitter.com/SirGFM" title="Follow me on Twitter">')
            self.tab()
            self.write('<img class="socialbt" src="/img/button/Twitter_Social_Icon_Circle_Color.png"> </img>')
            self.untab()
            self.write('</a>')

            self.untab()
            self.write('</div> <!-- page-header -->')

        self.write('<div id="page-sidebar" class="content">')
        self.tab()
        self.write_sidebar()
        self.untab()
        self.write('</div> <!-- page-sidebar -->')

        self.write('<div id="page-content" class="content">')
        self.tab()

    def write_body_end(self):
        """Write the static part of the ending of the page's body"""
        self.untab()
        self.write('</div> <!-- content -->')

        self.write('<div id="page-footer" class="footer">')
        self.tab()
        self.write_classy('p', 'footer', PAGE_FOOTER)
        self.untab()
        self.write('</div> <!-- content -->')

        self.untab()
        self.write('</body>')

