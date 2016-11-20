
from generator.page import PageWriter

class Page(PageWriter):
    """The site's homepage"""

    def __init__(self, nav):
        """Initializes this page

        nav -- Navigation object (which should be fed with every page before being inserted)
        """
        super(Page, self).__init__(title='HOME', url='/', nav=nav)

    def insert_content(self):
        """Insert the content of the page"""
        self.write_content('p', 'Hello! I\'m Gabriel Francisco Mandaji (aka, GFM) a software ' +
                'developer and hobbyist game developer.', style='content')
        self.write_content('p', 'I used to play around with RPG Maker and Flash (ActionScript 3 ' +
                '+ Flixel), but nowaday, except for the ocasional Python script (like this site), ' +
                'most of my projects are written in C. Reinventing the wheel is fun and great for ' +
                'learning!', style='content')
        self.write_content('p', 'Here you may find links and descriptions for most of the games ' +
                'I\'ve developed. Select a category above to explore its games. (NOTE: This page ' +
                'is still a WIP and some games may have broken links...)', style='content')

        self.write_content('h1', 'Contact', style='content')
        # TODO Add Twitter, devlog, e-mail & github

        self.write_content('h1', 'Current projects', style='content')

        self.write_content('h2', 'JJAT 1.5', style='content')
        self.write_content('p', 'Enhanced version of JJAT. Play with a friend or control two ' +
                'characters at once on this action platformer.', style='content')
        self.write_content('p', 'Different from the original game, each character will have a ' +
                'distinct role. "Swordy" can attack enemies, is quicker and has double jump. "Gunny"' +
                'is way less agile but has a teleport gun, which actually switch the character and ' +
                'the targeted entity.', style='content')

        self.write_content('h2', 'GFraMe', style='content')
        self.write_content('p', 'My personal framework for making games. It\'s SDL2 based and has ' +
                'features to allow instanced drawing (i.e., it may handle thousands of sprites at ' +
                '120 FPS) and easily rebindable controls. It\'s also integrated with my synthesizer, ' +
                'so songs are usually simple text files (which requires way less storage than sound files).',
                        style='content')
        self.write_content('p', 'It\'s always being enhanced, and the next planned refactor should enable ' +
                'supporting older platforms (e.g.,  Mega Drive/Sega Genesis through ' +
                '<a href="https://github.com/kubilus1/gendev" ">GENDEV</a>). I don\'t know when ' +
                'this new version will be started, though...', style='content')

        self.write_content('h2', 'c_synth', style='content')
        self.write_content('p', 'Synthesizes MML-like songs into waveforms. It uses a custom language ' +
                'that was never properlly documented...', style='content')
        self.write_content('p', 'An enhanced version has been started but is currently stopped. It will ' +
                'have proper documentantion, use a fixed amount of memory and synthesize songs on ' +
                'runtime, allowing some effects to be applied to a song or to its tracks separately.',
                style='content')

    def do_create(self):
        """Create the page, adding every require css/js"""
        self.create(style_list=['page.css'], script_list=[])

