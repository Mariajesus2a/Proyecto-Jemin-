from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Docu:  # crear una clase llamada Table1
    def __init__(self, data):
        self.id = data["idt_doc"]
        self.documentos = data["documentos"]
        self.estatus = data["estatus"]
        self.t_user_idt_user = data["t_user_idt_user"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO db_jemin.t_doc (documentos,name, estatus, t_user_idt_user) VALUES (%(documentos)s,%(name)s, %(estatus)s, %(t_user_idt_user)s );"
        result = connectToMySQL('db_jemin').query_db(query, data)
        user = {'user.id': result}
        return user

    @classmethod
    def all_doc_users(cls):
        query = "SELECT * FROM db_jemin.t_doc JOIN db_jemin.t_users ON t_users.idt_user = t_doc.t_user_idt_user;"
        mysql = connectToMySQL("db_jemin")
        results = mysql.query_db(query)
        print(results)
        if len(results) > 0:
            all_doc_users = []
            for document in results:
                all_doc_users.append(cls(document))
            return all_doc_users
        else:
            return None

    @classmethod
    def get_doc_by_iduser(cls, data):
        query = "SELECT first_name, last_name, email, documentos,name, estatus FROM db_jemin.t_doc JOIN db_jemin.t_users ON t_users.idt_user = t_doc.t_user_idt_user WHERE idt_user = %(id_t_user)s"
        mysql = connectToMySQL("db_jemin")
        results = mysql.query_db(query, data)
        # print(results)
        if len(results) > 0:
            # all_doc_users = []
            # for docByUser in results:
            #     all_doc_users.append(cls(docByUser))
            return results
        else:
            return None
