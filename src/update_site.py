
import pkgutil
import page
import sys
from generator.navigator import Navigator
from generator.webGame import WebGamePage

def main(web_game_list=[]):
    nav = Navigator()
    pages = []
    # List every page
    for _, modname, ispkg in pkgutil.iter_modules(page.__path__):
        if not ispkg:
            p = __import__('page.' + modname, fromlist="Page")
            pages.append(p.Page(nav))
    if len(web_game_list) > 0:
        # Overwrite the list with the list of web games
        pages = []
        for path in web_game_list:
            pages.append(WebGamePage(nav, path))
    # Create every page
    for p in pages:
        p.do_create()

if __name__ == '__main__':
    i = 0
    web_game_list = []
    while i < len(sys.argv):
        if sys.argv[i] == '--webgame' or sys.argv[i] == '-w':
            if i + 1 >= len(sys.argv):
                print 'Missing required parameter for "--webgame" argument'
                sys.exit(1)
            web_game_list.append(sys.argv[i + 1])
            i += 1
        i += 1
    main(web_game_list)

