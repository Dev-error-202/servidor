from cryptography.fernet import Fernet
import base64 as base

class OpenFile:
    def __enter__(self, caminho, modo, senha, encoding = 'UTF-8', errors = None):
        self.f = Fernet(senha)
        self.arquivo = open(caminho, modo, encoding=encoding, errors=errors)
        self.encoding = encoding

    def _read(self, _b = 0 ):
        return self.f.decrypt(self.arquivo.read(_b))

    def _write(self, text: str | bytes):
        (self.arquivo.write(self.f.encrypt(text)) if isinstance(text, bytes) else
        self.arquivo.write(self.f.encrypt(text.encode(encoding=self.encoding)))
        )

    def _seek(self, buffer: int):
        self.arquivo.seek(buffer)

    def truncate(self, size : int | None = None):
        self.arquivo.truncate(size)


