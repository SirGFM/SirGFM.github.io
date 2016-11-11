
import baseWriter
import const
import defer

class PageWriter(baseWriter.BaseWriter):
    """Writer for a complete page

    The expected way to use this is:
        - Inherit this class and override its 'insert_content' method (to output the actual page)
        - Call 'insert' with the required *.css and *.js.
    """

    def __init__(self, out, nav):
        """Initializes a PageWriter

        out -- Name of the output file to be generated
        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        super(PageWriter, self).__init__()
        self._out = out
        self._nav = nav

    def insert_content(self):
        return

    def create(self, style_list=['page.css'], script_list=[]):
        """Creates the HTML described by its sub-class

        style_list -- List of style (*.css) files to be included in this page
        script_list -- List of scripts (*.js) to be included in this page
        """
        self.set_output(open(out, 'wt'))
        self.write('<!DOCTYPE html>')
        self.write('<html lang="en">')
        self.tab()

        self._insert_head(style_list, script_list)
        self._insert_body()

        self.untab()
        self.write('</html>')
        self.close_output()

    def _insert_head(self, style_list=['page.css'], script_list=[]):
        """Inserts the page's <head>, which should be common to all pages

        style_list -- List of style (*.css) files to be included in this page
        script_list -- List of scripts (*.js) to be included in this page
        """
        defer_ = defer.Defer()

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

        defer_.run()

    def _insert_body():
        """Inserts the page's <body>. Every page is divided into four 'sections':
        a header, a navigation, a content and a footer"""
        self.write('<body>')
        self.tab()

        self._insert_body_header()
        self._nav.insert()
        self._insert_content()
        self._insert_footer()

        self.untab()
        self.write('</body>')

    def _insert_body_header():
        """Inserts the page's title (i.e., the header on the top of the page)"""
        defer_ = defer.Defer()

        self.write('<div id="page-header" class="header>')
        defer_.push(lambda :self.write('</div> <!-- header -->'))
        defer_.push(self.untab)
        self.tab()

        self.write('<a class="sidebar" href="/">')
        self.tab()
        self.write_content('h1', const.PAGE_TITLE, style="header")
        self.untab()
        self.write('</a>')

        # Since those images use 'float:right;', they must be placed on the
        # reverse order they should be rendered
        self.write('<a href="https://twitter.com/SirGFM" title="Follow me on Twitter">')
        self.tab()
        self.write('<img class="socialbt" src="/img/button/Twitter_Social_Icon_Circle_Color.png"> </img>')
        self.untab()
        self.write('</a>')

        self.write('<a href="https://github.com/SirGFM/ld36" title="Check out my projects on Github">')
        self.tab()
        self.write('<img class="socialbt" src="/img/button/GitHub-Mark-Light-32px.png"> </img>')
        self.untab()
        self.write('</a>')

        defer_.run()

    def _insert_content():
        """Inserts the page's content. Two components are added: a 'sidebar' (from the navigator
        passed as argument on the constructor) and a 'content', which is dependent on each actual page
        """
        defer_ = defer.Defer()

        self.write('<div id="page-content" class="content">')
        defer_.push(lambda :self.write('</div> <!-- content -->'))
        defer_.push(self.untab)
        self.tab()

        # Call the sub-class's function
        self.insert_content()

        defer_.run()

    def _insert_footer():
        """Inserts the page's footer. Two components are added: a 'sidebar' (from the navigator
        passed as argument on the constructor) and a 'content', which is dependent on each actual page
        """
        defer_ = defer.Defer()

        self.write('<div id="page-footer" class="footer">')
        defer_.push(lambda :self.write('</div> <!-- footer -->'))
        defer_.push(self.untab)
        self.tab()

        self.write_content('p', const.PAGE_FOOTER, style="footer")

