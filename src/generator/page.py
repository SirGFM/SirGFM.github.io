
from generator import const
from generator.baseWriter import BaseWriter
from generator.defer import Defer
from os import path

class PageWriter(BaseWriter):
    """Writer for a complete page

    The expected way to use this is:
        - Inherit this class and override its 'insert_content' method (to output the actual page)
        - Call 'insert' with the required *.css and *.js.
    """

    def __init__(self, title, url, nav, has_game_overlay=False, register_nav=True):
        """Initializes a PageWriter.
        Note that the page is registered into the navigator as soon as it's instantiated

        title -- Title used on the navigation bar
        url -- Page's address. Also used to generate the page's output file (by appending .html and removing the leading '/')
        nav -- Navigation object (which should be fed with every page before being inserted)
        has_game_overlay -- Whether this game should have a 'game overlay'
        register_nav -- Whether this page should register itself on the navigation menu
        """
        super(PageWriter, self).__init__()
        if url == '/':
            self._out = 'index.html'
        else:
            self._out = url[1:] + '.html'
            url += '.html'
        self._nav = nav
        if register_nav:
            self._nav.register(title, url)
        self._has_game_overlay = has_game_overlay

    def insert_content(self):
        """Overwrite this function on sub-classes to create new pages"""
        return

    def create(self, style_list=['page.css'], script_list=[], json_list=[]):
        """Creates the HTML described by its sub-class

        style_list -- List of style (*.css) files to be included in this page
        script_list -- List of scripts (*.js) to be included in this page
        json_list -- List of JSON files(*.json) to be included as a script. Its id shall be set to 'filename-json'.
        """
        self.set_output(open(self._out, 'wt'))
        self.write('<!DOCTYPE html>')
        self.write('<html lang="en">')
        self.tab()

        self._insert_head(style_list, script_list, json_list)
        self._insert_body()

        self.untab()
        self.write('</html>')
        self.close_output()

    def _insert_head(self, style_list=['page.css'], script_list=[], json_list=[]):
        """Inserts the page's <head>, which should be common to all pages

        style_list -- List of style (*.css) files to be included in this page
        script_list -- List of scripts (*.js) to be included in this page
        json_list -- List of JSON files(*.json) to be included as a script. Its id shall be set to 'filename-json'.
        """
        defer_ = Defer()

        self.write('<head>')
        defer_.push(lambda :self.write('</head>'))
        defer_.push(self.untab)
        self.tab()

        self.write('<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1" />')
        self.write_content('title', const.PAGE_TITLE)
        self.write('<meta name="keywords" content="{}" />'.format(const.PAGE_KEYWORDS))
        self.write('<meta name="description" content="{}" />'.format(const.PAGE_DESCRIPTION))
        self.write('<meta name="author" content="{}" />'.format(const.PAGE_AUTHOR))
        self.write('<link rel="shortcut icon" href="{}" />'.format(const.PAGE_ICON))

        for style in style_list:
            self.write('<link rel="stylesheet" type="text/css" href="/style/{}" />'.format(style))
        for script in script_list:
            self.write('<script type="text/javascript" src="/script/{}"></script>'.format(script))
        for jfile in json_list:
            filename = path.basename(jfile)
            filename = filename.replace('.json', '')
            self.write('<script type="application/json" id="{}-json">'.format(filename))
            with open(jfile, 'rt') as f:
                for line in f:
                    self.write(line, do_break=False)
            self.write('</script>')

        defer_.run()

    def _insert_body(self):
        """Inserts the page's <body>. Every page is divided into four 'sections':
        a header, a navigation, a content and a footer"""
        self.write('<body>')
        self.tab()

        if self._has_game_overlay:
            self._insert_game_overlay()
        self._insert_body_header()
        self._nav.insert(self)
        self._insert_content()
        self._insert_footer()

        self.untab()
        self.write('</body>')

    def _insert_game_overlay(self):
        """Inserts the page's game overlay (i.e., a floating div that displays the selected game)"""
        defer_ = Defer()

        self.write('<div id="floating-game-detail" class="game_description">')
        defer_.push(lambda :self.write('</div> <!-- floating-game-detail -->'))
        defer_.push(self.untab)
        self.tab()

        self.write('<h1 id="detail-title" class="game_description"> </h1>')
        self.write('<h2 id="detail-jam-title" class="game_description"> </h2>')
        self.write('<div id="detail-jam-content" class="game_description_content"> </div>')
        self.write('<h2 id="detail-about-title" class="game_description"> </h2>')
        self.write('<div id="detail-about" class="game_description_content"> </div>')
        self.write('<h2 id="detail-download-title" class="game_description"> </h2>')
        self.write('<div id="detail-download" class="game_description_content"> </div>')
        self.write('<p id="detail-close" class="close_game_description" onclick="HideGameDescription()"> Close </p>')

        defer_.run()

    def _insert_body_header(self):
        """Inserts the page's title (i.e., the header on the top of the page)"""
        defer_ = Defer()

        self.write('<div id="page-header" class="header">')
        defer_.push(lambda :self.write('</div> <!-- header -->'))
        defer_.push(self.untab)
        self.tab()

        self.write('<a class="header" href="/">')
        self.tab()
        self.write('<img class="header nearest-neighbor" src="/img/title/01_gfms.png"> </img>')
        self.write('<img class="header nearest-neighbor" src="/img/title/02_game.png"> </img>')
        self.write('<img class="header nearest-neighbor" src="/img/title/03_corner.png"> </img>')
        self.untab()
        self.write('</a>')

        self.write('<a class="header" href="https://github.com/SirGFM/ld36" title="Check out my projects on Github">')
        self.tab()
        self.write('<img class="socialbt" src="/img/button/GitHub-Mark-Light-32px.png"> </img>')
        self.untab()
        self.write('</a>')

        self.write('<a class="header" href="https://twitter.com/SirGFM" title="Follow me on Twitter">')
        self.tab()
        self.write('<img class="socialbt" src="/img/button/Twitter_Social_Icon_Circle_Color.png"> </img>')
        self.untab()
        self.write('</a>')

        defer_.run()

    def _insert_content(self):
        """Inserts the page's content. Two components are added: a 'sidebar' (from the navigator
        passed as argument on the constructor) and a 'content', which is dependent on each actual page
        """
        defer_ = Defer()

        self.write('<div id="page-content" class="content">')
        defer_.push(lambda :self.write('</div> <!-- content -->'))
        defer_.push(self.untab)
        self.tab()

        # Call the sub-class's function
        self.insert_content()

        defer_.run()

    def _insert_footer(self):
        """Inserts the page's footer. Two components are added: a 'sidebar' (from the navigator
        passed as argument on the constructor) and a 'content', which is dependent on each actual page
        """
        defer_ = Defer()

        self.write('<div id="page-footer" class="footer">')
        defer_.push(lambda :self.write('</div> <!-- footer -->'))
        defer_.push(self.untab)
        self.tab()

        self.write_content('p', const.PAGE_FOOTER, style="footer")

