
class raschet_ustoichivosti_otkosa_nasipi:
    def __init__(self, **kwargs):
        # Обработка переданных аргументов
        for key, value in kwargs.items():
            setattr(self, key, value)


