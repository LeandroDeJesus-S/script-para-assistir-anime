import sqlite3
from conf.sites import WebSites
from typing import Literal


class Database:
    def __init__(self, db):
        self.DATABASE = db
    
    def connect_db(self) -> None:
        """cria conexão com a base de dados, e o atributo de instancia 
        self.cursor
        """
        try:
            self.conn = sqlite3.connect(self.DATABASE)
            self.cursor = self.conn.cursor()
            self.connected = True
        except Exception as error:
            print('Erro durante conexão à DB:', error)
            self.close_db()
            
    def close_db(self):
        """fecha o cursor e encerra a conexão com a base de dados."""
        if not self.connected:
            return
        
        self.cursor.close()
        self.conn.close()
        self.connected = False
    
    def get_tags(self, values):
        """substitui os valores passados por ? para execução do comando sql.

        Args:
            values (any): valores passados ao comando sql.

        Returns:
            str: string no formato: '(?, ...)'
        """
        val_tag = ['?' for value in values]
        val_tag = f"({', '.join(val_tag)})"
        return val_tag
    
    def save_in_database(self, table: str, fields: Literal['(f1, ...)'], values: tuple):
        """
        salva os dados na base de dados
        """   
        try:   
            tags = self.get_tags(values)
            
            cmd = f'INSERT OR IGNORE INTO {table} {fields} VALUES {tags}'
            self.cursor.execute(cmd, values)
            self.conn.commit()
        except:
            self.close_db()
        
    def get_one_data(self, table: str, field: str, value):
        """pega um dado em especifico da base de dados

        Args:
            table (str): nome da tabela do banco de dados
            field (str): campo no qual deseja obter o dados
            value (str): valor que deseja realizar a consulta

        Returns:
            _type_: _description_
        """
        try:
            cmd = f'SELECT * FROM {table} WHERE {field}=:v', {'v': value}

            self.cursor.execute(*cmd)
            return self.cursor.fetchone()
        except:
            self.close_db()
    
    def get_all_data(self, table: str, limit: int=60, where: str='', like: str='') -> list[tuple]:
        """faz um select * na base de dados com limit 60 por padrão.
        para retirar o limit basta passar 0 como valor

        Args:
            table (str): nome da tabela do banco de dados
            limit (int, optional): limite de dados para consulta. Defaults to 60.
            where (str, optional): campo para comando where. Defaults to ''.
            like (str, optional): valor da consulta do where. Defaults to ''.

        Raises:
            ValueError: caso limit não seja do tipo int
            SyntaxError: caso 'where' seja enviado sem o 'like' ou o inverso.

        Returns:
            list[tuple]: resultado da consulta
        """
        try:
            cmd = f'SELECT * FROM {table}'
            if not isinstance(limit, int): 
                raise ValueError('limit must be an integer')
            
            limit = f' LIMIT {limit}' if limit else ''
            if where and not like or like and not where:
                raise SyntaxError('if where is sent like also needs to be sent')
            
            elif not where and not like:
                cmd += limit
                
            elif where and like:
                where_cmd = f' WHERE {where} LIKE ?' + limit
                like = (f'%{like}%',)
                cmd += where_cmd
            
            self.cursor.execute(cmd, like)
            return self.cursor.fetchall()
        except:
            self.close_db()
        