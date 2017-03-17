
from custom_writer import CustomWriter
import json
import sys

def main(src, dst, nav):
    with open(src, 'rt') as fp:
        _decoded = json.load(fp)
    with open(dst, 'wt') as out:
        ctx = CustomWriter(out, nav)

        ctx.style.append('page.css')

        ctx.open_html_tag()
        ctx.write_html_header()
        ctx.write_body_begin()

        title = _decoded['title']
        ctx.write_classy('h1', 'content', title)
        try:
            ctx.write_classy('h2', 'content', _decoded['event']['title'])
        except:
            pass

        for platform in _decoded['distribution']:
            if platform['platform'] == 'web' and 'technology' in platform.keys() and platform['technology'] == 'flash':
                link = platform['link'].replace('.html', '.swf')
                width = platform['width']
                height = platform['height']
                how_to_play = platform['how_to_play']
                break

        ctx.write('<object class="game" classid="clsid:D27CDB6E-AE6D-11cf-96B8-4" '
            'codebase="http://download.macromedia.com" width="{}px" height="{}px" '
            'title="{}">'.format(width, height, title))
        ctx.tab()
        ctx.write('<param name="movie" value="{}" />'.format(link))
        ctx.write('<param name="quality" value="high" />')
        ctx.write('<embed src="{}" quality="high" pluginspage="http://www.macromedia.com/g" '
            'type="application/x-shockwave-flash" width="{}px" height="{}px">'
            '</embed>'.format(link, width, height))
        ctx.untab()
        ctx.write('</object>')

        for p in how_to_play:
            ctx.write_classy('p', 'content', p)

        ctx.write_body_end()
        ctx.close_html_tag()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {} input_file output_file nav_file'
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    nav = sys.argv[3]

    main(src, dst, nav)

