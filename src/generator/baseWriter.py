
class BaseWriter(object):
    """Helpers to write HTML pages"""

    def __init__(self):
        """Initialize a writer"""
        self._fp = None
        self._indent = 0

    def set_indent(self, indent):
        """Set the current indentation

        indent -- The new indentation
        """
        self._indent = indent

    def get_indent(self):
        """Retrieve the current indentation"""
        return self._indent

    def set_output(self, fp):
        """Set the current output file"""
        self._fp = fp

    def get_output(self):
        """Return the current output file"""
        return self._fp

    def close_output(self):
        """Closes the current file"""
        self._fp.close()
        self._fp = None

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

    def write_github_link(self, relative_link, style=None):
        """Insert a simple link to a Github repository

        relative_link -- The path to a repository within Github, e.g.: SirGFM/GFraMe
        style -- CSS class to be used with the tag
        """
        self.write_content('p', '<a href="https://github.com/{}"> Check it out on Github </a>'.format(relative_link),
                style=style)

    def write_image(self, image_link, position, style=None):
        """Insert an image on the given relative position

        image_link -- Path to the image
        position -- Relative position of the image ('left', 'right', 'center')
        style -- CSS class to be used with the tag
        """
        pos_style = ''

        if position == 'left':
            pos_style = 'style="float:left;"'
        elif position == 'right':
            pos_style = 'style="float:right;"'
        elif position == 'center':
            pos_style = 'style="margin-left: auto; margin-right: auto; display: block;"'

        if style is not None:
            self.write('<img class="{}" {} src="{}"> </img>'.format(style, pos_style, image_link))
        else:
            self.write('<img {} src="{}"> </img>'.format(pos_style, image_link))

