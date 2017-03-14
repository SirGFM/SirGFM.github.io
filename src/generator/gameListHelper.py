
from os import listdir
from os.path import isfile, join
from generator.gameIcon import GameWriter

def GetGameList(dir_path):
    """Retrieve the list of JSON files within a given directory
    
    dir_path -- The inspected directory
    """
    _list = []
    for f in listdir(dir_path):
        path = join(dir_path, f)
        if not isfile(path):
            continue
        elif not path.endswith('.json'):
            continue
        _list.append(path)
    _list.reverse()

    return _list

def InsertGameIcons(page, game_list):
    """ Insert a centered list of game icons

    page -- The page where the icons will be added
    game_list -- The list of games' JSONs
    """
    page.write('<div style="display:table; margin:auto">')
    for path in game_list:
        GameWriter(path).insert(page)
    page.write('</div>')

