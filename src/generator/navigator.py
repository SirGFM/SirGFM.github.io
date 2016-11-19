
import baseWriter
import defer

class Navigator(baseWriter.BaseWriter):
    """The navigation bar

    Every page that is accessible through the navigation bar has to be registered into it.
    """

    class _Page():
        """Encapsulates the details for each page"""
        def __init__(self, title, url):
            """Initializes a page

            title -- The page's title (i.e., how it will appear on the nav bar)
            url -- The page's address
            """
            self.title = title
            self.url = url

    def __init__(self):
        """Initializes the navigator"""
        self._pages = []

    def register(self, title, url):
        """Register a new page into the navigation bar

        title -- The page's title (i.e., how it will appear on the nav bar)
        url -- The page's address
        """
        self._pages.append(Navigator._Page(title, url))

    def insert(self, page):
        """Insert the navigation bar into the current page

        page -- The current page
        """
        defer_ = defer.Defer()

        self.set_output(page.get_output())
        self.set_indent(page.get_indent())
        defer_.push(lambda :self.set_output(None))

        self.write('<div id="page-sidebar" class="sidebar">')
        defer_.push(lambda :self.write('</div> <!-- sidebar -->'))
        defer_.push(self.untab)
        self.tab()

        for p in self._pages:
            self.write('<a class="sidebar" href="{}"> {} </a>'.format(p.url, p.title))

        defer_.run()

