"""
    Arquivo de manipulação direta do banco de dados
    gerencia a pasta de dados de cada usuario de maneira mas otimizada,
"""

import os
import sys
import sqlite3 as sql
from os.path import join, exists
import platform
from pandas import read_sql_query, DataFrame
import pandas
# from Criptografia import OpenFile



class BancoCore:
    def __init__(self, user):
        self.pathdir = ('C:/Program Files/BancoSystem' if platform.system() == 'Windows' else '/opt/BancoSystem')
        self.path_user = join(self.pathdir, user)
        self.banco_sql = join(self.path_user, 'BancoDeDados.db')
        self.ntfs_dir = join(self.path_user, 'NTFs')
        self.user_conf = join(self.path_user, 'cache.conf')
        self.table = None
        self.banco_conect = None

        if not exists(self.pathdir):
            os.mkdir(self.pathdir)

    def loadBanco(self):
        """
        Carrega o banco para manipulação interna do programa
        :return: None
        """
        self.banco_conect = sql.connect(self.banco_sql)



    def creatUser(self):
        os.makedirs(self.path_user, exist_ok=True)
        os.makedirs(self.ntfs_dir, exist_ok=True)
        # with OpenFile(self.banco_sql, 'rb', password) as file:
        #     data = file.read()
        banco = sql.connect(self.banco_sql)
        cursor = banco.cursor()
        cursor.execute(
        '''CREATE TABLE entradas (
            id INTEGER PRIMARY KEY,
            tipo TEXT,
            icone TEXT,
            valor INTEGER,
            data INTEGER
            )
    ''')
        cursor.execute(
            '''
            CREATE TABLE saidas ( id INTEGER PRIMARY KEY, 
            valor INTEGER,
            tipo TEXT,
            comprovante TEXT,
            dia INTEGER,
            mes INTEGER,
            ano INTEGER)
            '''
        )

        cursor.execute('''
        CREATE TABLE contas (
        id INTEGER PRIMARY KEY,
        valor INTEGER,
        tipo TEXT,
        nome TEXT, 
        dia TEXT,
        meses TEXT)
        ''')
        # coloquei os meses em texto pq consigo tranformar valores de texto em numeros, mas tambem consigo deixar uma conta
        # fixa apenas com esssa manobra

        banco.commit()

    def loadUserDate(self, table) -> DataFrame:
        """
        Carrega o banco de dados do usuario em memoria criando um load para cada usuario.
        com o core carregando e retornando uma tabela de manipulação sql injection não ocorre.
        :return: DataFrame do pandas para manipulação de dados mais facilmente
        """
        banco = sql.connect(self.banco_sql)

        if not table in ['saidas', 'contas', 'entradas']:
            raise ValueError('O Valor não se encontra em uma tabela valida')
        else:
            comando = f'SELECT * FROM {table}'
            self.table = table
            return  read_sql_query(comando, banco)


    def saveUserDate(self, tabela_pandas: DataFrame, tabela_sql: str = None):
        """
        Recria a tabela dentro do banco (CUIDADO) isso apaga os valores ja existente dentro do banco

        :param tabela_pandas: DataFrame com os dados
        :param tabela_sql: o nome da tabela sql caso queria salvar em uma especifica
        :return:
        """
        if self.table is None and tabela_sql is None:
            raise FileNotFoundError('Tabela não definida, escolha uma')

        if tabela_sql is not None:
            self.table = tabela_sql

        if self.banco_conect is None:
            raise ConnectionError('Banco não carregado')

        if tabela_sql not in ['saidas', 'constas', 'entradas']:
            raise ValueError('Tabela não definida')

        tabela_pandas.to_sql(self.table, con=self.banco_conect, if_exists='replace')










