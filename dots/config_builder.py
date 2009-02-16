class ConfigBuilder(dict):
    def __init__(self):
        self['xml'] = _ConfigSection()
        self['translation'] = _ConfigSection()
        self['outputFormat'] = _ConfigSection()

    def __str__(self):
        s = ''
        for key in self.keys():
            s += '%s\n' % key
            for k,v in self[key].items():
                s += '\t%s %s\n' % (k ,v)
        return s

class _ConfigSection(dict):
    pass

if __name__ == "__main__":
    cb = ConfigBuilder()
    cb['xml']['semanticFiles'] = '*,nemeth.sem'
    cb['xml']['internetAccess'] = 'yes'
    cb['translation']['literaryTextTable'] = 'en-us-g2.ctb'
    cb['outputFormat']['cellsPerLine'] = 40
    cb['outputFormat']['linesPerPage'] = 25

    print str(cb)
