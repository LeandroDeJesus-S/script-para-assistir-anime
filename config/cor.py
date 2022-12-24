class Color:
    @staticmethod
    def blue(txt):
        return f'\033[34m{txt}\033[m'

    @staticmethod
    def grey(txt):
        return f'\033[37m{txt}\033[m'

    @staticmethod
    def yellow(txt):
        return f'\033[33m{txt}\033[m'

    @staticmethod
    def purple(txt):
        return f'\033[35m{txt}\033[m'

    @staticmethod
    def red(txt):
        return f'\033[31m{txt}\033[m'

    @staticmethod
    def green(txt):
        return f'\033[32m{txt}\033[m'

    @staticmethod
    def cian(txt):
        return f'\033[36m{txt}\033[m'

    @staticmethod
    def white(txt):
        return f'\033[97m{txt}\033[m'
    