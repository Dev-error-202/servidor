import json
import os
import secrets
import base64
import hashlib

class Users:
    def __init__(self, local):
        self.local = local
        os.makedirs(os.path.dirname(local), exist_ok=True)

        if not os.path.exists(local):
            with open(local, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        with open(local, 'r', encoding='utf-8') as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {}

    def getusers(self) -> dict:
        return self.data

    def commit(self):
        temp_file = self.local + ".tmp"

        print(self.data)
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

        os.replace(temp_file, self.local)  # write atômico

    def cadastro(self, usuario: str, password: str, **kwargs):

        if usuario in self.data:
            raise ValueError('Usuário já existente')

        cod = secrets.token_hex(16)
        user_id = '-'.join(cod[i:i+8] for i in range(0, len(cod), 8)).upper()

        kwargs['id'] = user_id
        kwargs['salt'] = base64.b64encode(os.urandom(16)).decode()
        self.data[usuario] = kwargs

        return user_id  # útil pra criar pasta

    def update(self, usuario, **kwargs):
        if usuario not in self.data:
            raise ValueError('Usuário não existe')

        self.data[usuario].update(kwargs)

    def delUser(self, usuario):
        del self.data[usuario]

    def gerar_token(self, senha: str, salt: bytes | str):
        chave = hashlib.pbkdf2_hmac(
            'sha256',
            senha.encode(),
            salt if isinstance(salt, bytes) else base64.b64decode(salt),
            200_000  # aumenta segurança
        )
        return base64.urlsafe_b64encode(chave)

f = Users(r'C:\Users\aecin\Documents\PythonProjects\Testes\users.json')

salt = f.getusers()['aecio']['salt']
gg = f.gerar_token('aeciosilva1702', salt)

print(gg)
f.commit()

