class SettingsTypeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class KeyWordArgsError(Exception):
    def __init__(self, msg):
        super().__init__(msg)