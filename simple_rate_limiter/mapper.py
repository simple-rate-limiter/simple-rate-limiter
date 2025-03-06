class Mapper:
    @staticmethod
    def key(*args, **kwargs) -> str:
        return ""

    @staticmethod
    def tokens(*args, **kwargs):
        return 1

    @staticmethod
    def preprocess(tokens, *args, **kwargs):
        return args, kwargs
