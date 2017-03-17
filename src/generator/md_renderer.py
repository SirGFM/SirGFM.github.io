
from custom_writer import CustomWriter
import json
from mistune import BlockLexer, Markdown, Renderer, InlineLexer
import re
import sys

class CustomRenderer(Renderer):
    """Custom renderer with all my markdown extensions.

    It overrides all nodes that should write directly into the file
    """

    def my_setup(self, ctx):
        self._ctx = ctx
        self._header_re = re.compile(r'<(h\d)>')

    def header(self, text, level, raw=None):
        txt = super(CustomRenderer, self).header(text, level, raw)
        if txt != '':
            m = self._header_re.match(txt)
            txt = self._header_re.sub('<{} class="content">'.format(m.group(1)), txt)
            txt += '</{}>'.format(m.group(1))
            self._ctx.write(txt, do_break=True)
        return ''

    def paragraph(self, text):
        if text == '':
            return ''
        txt = super(CustomRenderer, self).paragraph(text)
        if txt != '':
            txt = txt.replace('<p>', '<p class=content>')
            self._ctx.write(txt, do_break=False)
        return ''

class CustomBlockLexer(BlockLexer):
    """Custom block lexer. It adds the following rules:

    \$add_game(list_name, json_file) -- Insert the path to a game's JSON file into a 
                                       list of games. This list is stored in _game.
    \$add_style(css_file) -- Store a css file to be added on the header.
    \$add_script(js_file) -- Store a javascript file to be added on the header.
    \$write_header -- Writes a HTML header to the current file (if any). The presence
                     of any game on _game triggers the addition of the game overlay.
    \$begin_content -- Output the content's "prologue".
    """

    def my_setup(self, ctx):
        self._ctx = ctx

    def enable_custom(self):
        self.enable_add_game()
        self.enable_add_script()
        self.enable_add_style()
        self.enable_write_header()
        self.enable_begin_content()
        self.enable_left_image()

    def enable_add_game(self):
        """Add rule that parses a game"""
        self.rules.add_game = re.compile(r'\$add_game\((.+?), (.+?)\)')
        self.default_rules.insert(0, 'add_game')

    def parse_add_game(self, m):
        """Function called whenever an 'add_game' rule is matched.

        It actually adds the game to a dictionary/list
        """
        _list = m.group(1)
        _json = m.group(2)

        try:
            game_list = self._ctx.game[_list]
        except:
            game_list = []
            self._ctx.game[_list] = game_list

        game_list.append(_json)

        return ''

    def enable_add_script(self):
        """Add rule that parses a script """
        self.rules.add_script = re.compile(r'\$add_script\((.+?)\)')
        self.default_rules.insert(0, 'add_script')

    def parse_add_script(self, m):
        """Function called whenever an 'add_script' rule is matched.

        It actually adds the script to a list
        """
        self._ctx.script.append(m.group(1))

        return ''

    def enable_add_style(self):
        """Add rule that parses a style"""
        self.rules.add_style = re.compile(r'\$add_style\((.+?)\)')
        self.default_rules.insert(0, 'add_style')

    def parse_add_style(self, m):
        """Function called whenever an 'add_style' rule is matched.

        It actually adds the style to a list
        """
        self._ctx.style.append(m.group(1))

        return ''

    def enable_write_header(self):
        """Add rule that outputs the complete header"""
        self.rules.write_header = re.compile(r'\$write_header')
        self.default_rules.insert(0, 'write_header')

    def parse_write_header(self, m):
        """Write the HTML header"""
        self._ctx.write_html_header()

        return ''

    def enable_begin_content(self):
        """Add rule that outputs the content's prologue"""
        self.rules.begin_content = re.compile(r'\$begin_content')
        self.default_rules.insert(0, 'begin_content')

    def parse_begin_content(self, m):
        """Write the prologue for the page's content"""
        self._ctx.write_body_begin()

        return ''

    def enable_left_image(self):
        """Add rule that outputs a left-aligned image"""
        self.rules.left_image = re.compile(r'!<\[(.+)\]\((.+?)\)')
        # TODO Add support to title parameter
        self.default_rules.insert(0, 'left_image')

    def parse_left_image(self, m):
        """Write a left aligned image"""
        alt_text = m.group(1)
        src = m.group(2)

        title = ''
        if len(m.groups()) == 3:
            title = m.group(3)

        self._ctx.write('<img class="content nearest-neighbor" style="float:left;" '
                'src="{}" alt="{}"> {} </img>'.format(src, alt_text, title))

        return ''

class CustomInlineLexer(InlineLexer):
    """Custom inline lexer. It adds the following rules:

    \$insert_game_list(list_name) -- Insert the icons for the given list of games.
    \$end_content -- Output the content's "epilogue" and finish writing to the output.
    """

    def my_setup(self, ctx):
        self._ctx = ctx
        try:
            self.renderer.my_setup(ctx)
        except: pass

    def enable_custom(self):
        self.enable_insert_game_list()
        self.enable_end_content()

    def enable_insert_game_list(self):
        """Add rule that output games from a given list"""
        self.rules.insert_game_list = re.compile(r'\$insert_game_list\((.+?)\)')
        self.default_rules.insert(0, 'insert_game_list')

    def output_insert_game_list(self, m):
        """Insert all games on a given list"""
        game_list = self._ctx.game[m.group(1)]

        self._ctx.write('<div style="display:table; margin:auto">')
        self._ctx.tab()
        for path in game_list:
            fp = open(path, 'rt')
            _decoded = json.load(fp)
            fp.close()

            _id = _decoded['id']
            _icon = _decoded['image']
            _title = _decoded['title']

            self._ctx.write('<div id="{}" class="gamelisting" '
                    'onclick="SetGameDescription(this); '
                    'ToggleGameDescriptionVisibility()">'.format(_id))
            self._ctx.tab()
            self._ctx.write('<div id="{}-icon" class="gameicon" onmouseover='
                    '"ShowGameDetails(this)" onmouseout="HideGameDetails(this)" '
                    'style="background-image:url(\'/img/game/icon/{}\')">'.format(_id, _icon))
            self._ctx.tab()
            self._ctx.write('<div id="{}-overlay" class="gameiconoverlay">'.format(_id))
            self._ctx.tab()
            self._ctx.write('<div id="{}-inner-title" class="gameicontitle noselect" >'.format(_id))
            self._ctx.tab()
            self._ctx.write_classy('h1', 'gameicontitle', _title)
            self._ctx.untab()
            self._ctx.write('</div> <!-- {}-inner-title -->'.format(_id))
            self._ctx.untab()
            self._ctx.write('</div> <!-- {}-overlay -->'.format(_id))
            self._ctx.untab()
            self._ctx.write('</div> <!-- {}-icon -->'.format(_id))
            self._ctx.untab()
            self._ctx.write('</div> <!-- {} gamelisting -->'.format(_id))
        self._ctx.untab()
        self._ctx.write('</div>')

        return ''

    def enable_end_content(self):
        """Add rule that outputs the content's epilogue"""
        self.rules.end_content = re.compile(r'\$end_content')
        self.default_rules.insert(0, 'end_content')

    def output_end_content(self, m):
        """Write the epilogue for the page's content"""
        self._ctx.write_body_end()

        return ''

def main(markdown, src, dst, nav):
    with open(dst, 'wt') as out:
        ctx = CustomWriter(out, nav)
        markdown.inline.my_setup(ctx)
        markdown.block.my_setup(ctx)

        ctx.open_html_tag()
        # The rendered markdown is automatically redirected through the CustomWriter
        txt = ''
        with open(src, 'rt') as fp:
            for line in fp:
                txt += line
        print markdown(txt)

        ctx.close_html_tag()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {} input_file output_file nav_file'
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    nav = sys.argv[3]

    renderer = CustomRenderer()
    block = CustomBlockLexer()
    block.enable_custom()
    inline = CustomInlineLexer(renderer)
    inline.enable_custom()
    markdown = Markdown(renderer, inline=inline, block=block)

    main(markdown, src, dst, nav)

