class TermColors:
    '''Basic terminal colors class'''

    def __init__(self):
        pass

    def default(self):
        '''Set the foreground color to the default '''
        return "\x1b[39m"

    def reset(self):
        '''Reset terminal'''
        return "\x1b[0m"

    def bold(self):
        '''Set the foreground as bold '''
        return "\x1b[1m"

    def red(self):
        '''Set the foreground color to red '''
        return "\x1b[31m"

    def green(self):
        '''Set the foreground color to green '''
        return "\x1b[32m"

    def yellow(self):
        '''Set the foreground color to yellow '''
        return "\x1b[43m"
