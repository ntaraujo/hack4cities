# Script para realizar a interface entre a GUI e a base de dados

import sqlite3 as sql


class Database:
    def __init__(self, dbfile, silent=False):
        # Inicializar Classe
        self.dbfile = dbfile
        self.silent = silent
        self.create_connection()

    def create_connection(self):
        # Tentar criar a conexão com a base de dados
        con = None
        try:
            con = sql.connect(self.dbfile)
            # Para razões de debugging
            if not self.silent:
                print(f"\nUsando SQLite3\nVersão: {sql.version}\n")
        except Exception as e:
            print(e)
        finally:
            self.con = con
            self.cur = con.cursor()


# Tratamento caso o script seja executado diretamente
if __name__ == "__main__":
    raise (Exception(
        "ERRO\n\"database_interface.py\" não foi feito para ser executado por si só, pois se trata de uma biblioteca."))
