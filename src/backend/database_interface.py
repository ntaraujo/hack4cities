# Script para realizar a interface entre a GUI e a base de dados

import sqlite3 as sql
from os import path


class Database:
    def __init__(self, dbfile="database.db", schema="./database.sql", silent=False):
        # Inicializar Classe
        self.dbfile = dbfile
        self.silent = silent
        self.schema = schema
        self.con = self.cur = None
        self._create_connection()
        self._create_database()
        

    def _create_connection(self):
        # Tentar criar a conexão com a base de dados
        try:
            con = sql.connect(self.dbfile)
            self.con = con
            self.cur = con.cursor()
            # Para razões de debugging
            if not self.silent:
                print(f"\nUsando SQLite3\nVersão: {sql.version}\n")
        except Exception as e:
            print(e)

    def _create_database(self):
        with open(self.schema, 'r') as sql_file:
            sql_script = sql_file.read()
            sql_file.close()
        if not self.silent:
            print("Inserindo tabelas na base de dados...")
        self.cur.executescript(sql_script)

    def get_data(self):
        pass


# Tratamento caso o script seja executado diretamente
if __name__ == "__main__":
    db = Database()
    #raise (Exception(
    #    "ERRO\n\"database_interface.py\" não foi feito para ser executado por si só, pois se trata de uma biblioteca."))
