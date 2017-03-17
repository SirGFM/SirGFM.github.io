
import json
import sys
import re

class BufferedWriter():
    def __init__(self, txt='', max_len=80, out=sys.stdout):
        self._txt = txt
        self._len = len(txt)
        self._max_len = max_len
        self._out = out

    def write(self, txt, force=False):
        """Write some text. If the line were to go beyond the limit,
        print it store the new lew

        txt -- The text to be printed
        force -- Whether it should be printed even if no overflow were to occur
        """
        l = len(txt)
        if self._len + l > self._max_len:
            self._out.write(self._txt + ' \\\n')
            self._txt = txt
            self._len = l
        else:
            self._txt += ' ' + txt
            self._len += l
        if force and self._len > 0:
            self._out.write(self._txt + '\n')
            self._txt = ''
            self._len = 0

def main(src, output_name):
    """Create the list of dependencies for any given page
    """
    pattern = re.compile(r'\$add_game\(.+?, (.+?)\)')

    d_name = ''
    html_name = ''
    if output_name.endswith('.d'):
        d_name = output_name
    elif output_name.endswith('.html'):
        html_name = output_name

    if d_name == '':
        d_name = output_name.replace('.html', '.d')
    elif html_name == '':
        html_name = output_name.replace('.d', '.html')

    is_first = True
    with open(src, 'rt') as fp:
        webgame_list = []
        buff = None
        for line in fp:
            m = pattern.match(line)
            if m:
                json_file = m.group(1)
                # Keep track of the file's dependencies
                if is_first:
                    buff = BufferedWriter(txt='{} {}: {}'.format(d_name, html_name, src))
                    is_first = False
                buff.write(json_file)
                # Also check if it's a webgame which must have its page generated
                with open(json_file, 'rt') as fp:
                    _decoded = json.load(fp)
                try:
                    for value in _decoded['distribution']:
                        if value['platform'] == 'web' and value['technology'] == 'flash':
                            link = value['link']
                            if link.startswith('/'):
                                link = link[1:]
                            webgame_list.append((link, json_file))
                            break
                except:
                    pass
        # Also add the navigation bar as a dependency
        buff.write('src/nav.txt')
        # Append the webgames as dependencies
        if buff is not None:
            for game in webgame_list:
                buff.write(game[0])
            buff.write('', force=True)
            print ''
        # And create the rules to generate its pages
        for game in webgame_list:
            print '{}: {} src/nav.txt'.format(game[0], game[1])
            print '{}: {}'.format(game[0], game[1])
            print '\t@ echo "Rendering $@..."'
            print '\t@ $(PPATH) python src/generator/web_game_renderer.py $(PWD)/$< $(PWD)/$@ $(PWD)/src/nav.txt'
            print ''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: {} input_file output_name'
        print 'NOTE: Output is printed to stdout'
        sys.exit(1)

    src = sys.argv[1]
    output_name = sys.argv[2]

    main(src, output_name)

