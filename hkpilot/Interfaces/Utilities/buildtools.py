class BuildTools(object):

    def __init__(self, name, path):
        self._type = "default"
        if name != "":
            self._package_name = name
        if name != "":
            self._path = path

    @property
    def type(self):
        return self._type

    @property
    def package_name(self):
        return self._package_name

    def Download(self):
        return False

    def Configure(self):
        return False

    def Build(self):

        return False

    def Install(self):
        return False

    def Check(self):
        return False

