import json
from os import makedirs
from os.path import dirname

class Users:
    def __init__(self, local):
        makedirs(dirname(local), exist_ok=True)
        try:
            self.arquivo = open(local, 'r+', encoding='UTF-8')
        except FileNotFoundError:
            self.arquivo = open(local, 'w+', encoding='UTF-8')

        self.date: dict = json.load(self.arquivo)


    def getusers(self) -> dict:
        return self.date

    def commit(self):
        """
        Salva os valores no arquivo
        :return:
        """
        self.arquivo.seek(0)
        self.arquivo.write(json.dumps(self.date, indent=4, ensure_ascii=False))
        self.arquivo.truncate()

    def cadrastro(self, usuario, **kwargs):
        if usuario in self.date.keys():
            raise ValueError('Usuário ja existente')

        self.date.update({usuario: kwargs})

    def update(self, usuario, **kwargs):
        '''
        Altera um ou mais valores dentro do tabela de usuarios
        :param usuario: Usuario existente no banco de dador
        :param kwargs: Parametros de atualização ou inclusão
        :return:
        '''
        self.date[usuario].update(kwargs)



