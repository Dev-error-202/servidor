from cryptography.fernet import Fernet
import base64 as base

class OpenFile:
    def __init__(self, caminho:str, modo: str['wb', 'rb'], senha: bytes,  errors: str = None):
        self.f = Fernet(senha)
        self.caminho = caminho
        self.modo = modo
        self.errors = errors

    def __enter__(self):
        self.arquivo = open(self.caminho, self.modo, errors=self.errors)
        return self

    def read(self):
        data = self.arquivo.read()
        return self.f.decrypt(data)

    def write(self, text: str | bytes):
        if isinstance(text, str):
            text = text.encode()

        encrypted = self.f.encrypt(text)
        self.arquivo.write(encrypted)

    def seek(self, buffer: int):
        self.arquivo.seek(buffer)

    def truncate(self, size : int | None = None):
        self.arquivo.truncate(size)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.arquivo.flush()
        self.arquivo.close()

    def close(self):
        self.arquivo.close()