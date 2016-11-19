
from generator.page import PageWriter

class Page(PageWriter):
    """The site's homepage"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        super(Page, self).__init__(title='HOME', url='/', nav=nav)

    def insert_content(self):
        """Insert the content of the page"""
        self.write_content('p', "WIP example page")

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css'], script_list=[])

