
class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension):
        pass

    def lee_archivo(self):
        pass

    @staticmethod
    def convierte_dict_a_csv(data: dict):
        pass


class LectorCSV(Lector):
    def __init__(self, path: str):
        pass

    def lee_archivo(self, datetime_columns=[]):
        pass


class LectorJSON(Lector):
    def __init__(self, path: str):
        pass

    def lee_archivo(self):
        pass


class LectorTXT(Lector):
    def __init__(self, path: str):
        pass

    def lee_archivo(self):
        pass






