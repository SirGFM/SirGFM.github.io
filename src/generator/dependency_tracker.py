
import sys
import re

def main(src, output_name):
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

    txt = '{} {}: {}'.format(d_name, html_name, src)
    l_txt = len(txt)
    with open(src, 'rt') as fp:
        # Iterate through the file looking for a 'import game' and output that
        # (neatly so it shouldn't go over 80 characters)
        for line in fp:
            m = pattern.match(line)
            if m:
                l = len(m.group(1))
                if l + l_txt > 80:
                    print txt + ' \\'
                    txt = m.group(1)
                    l_txt = l
                else:
                    txt += ' ' + m.group(1)
                    l_txt += l + 1
        if l_txt != 0:
            print txt

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: {} input_file output_name'
        print 'NOTE: Output is printed to stdout'
        sys.exit(1)

    src = sys.argv[1]
    output_name = sys.argv[2]

    main(src, output_name)

