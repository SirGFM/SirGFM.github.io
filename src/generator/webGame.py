
from generator.gameIcon import Game
from generator.page import PageWriter

class WebGamePage(PageWriter):
    """Page for a web game"""

    def __init__(self, nav, path):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        path -- Path to the JSON file describing this game
        """
        self._game = Game(path)
        self._base_link = self._game.web_link().replace('.html', '')

        super(WebGamePage, self).__init__(title=self._game.id(), url=self._base_link, nav=nav, register_nav=False)

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css'], script_list=[])

    def insert_content(self):
        """Insert the content of the page"""

        self.write_content('h1', self._game.title(), style='content')
        subtitle = self._game.subtitle()
        if subtitle:
            self.write_content('h2', subtitle, style='content')

        swf_data = self._game.get_flash_data()
        if swf_data:
            self.write('<object class="game" classid="clsid:D27CDB6E-AE6D-11cf-96B8-4" '
                'codebase="http://download.macromedia.com" width="{}px" height="{}px" '
                'title="{}">'.format(swf_data['width'], swf_data['height'], self._game.title()))
            self.write('    <param name="movie" value="{}" />'.format(self._base_link + '.swf'))
            self.write('    <param name="quality" value="high" />')
            self.write('    <embed src="{}" quality="high" pluginspage="http://www.macromedia.com/g" '
                'type="application/x-shockwave-flash" width="{}px" height="{}px">'
                '</embed>'.format(self._base_link + '.swf', swf_data['width'], swf_data['height']))
            self.write('</object>')

            for p in swf_data['how_to_play']:
                self.write_content('p', p, style='content')

