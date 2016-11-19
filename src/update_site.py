
import pkgutil
import page
from generator.navigator import Navigator

def main():
    nav = Navigator()
    pages = []
    # List every page
    for _, modname, ispkg in pkgutil.iter_modules(page.__path__):
        if not ispkg:
            p = __import__('page.' + modname, fromlist="Page")
            pages.append(p.Page(nav))
    # Create every page
    for p in pages:
        p.do_create()

if __name__ == '__main__':
    main()

