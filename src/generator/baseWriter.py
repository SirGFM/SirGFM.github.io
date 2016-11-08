
class BaseWriter:
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

    def close_output():
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

