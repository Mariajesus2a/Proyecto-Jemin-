from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# Ejemplos FROM, SAVE, GET_ALL, Obtener solo un dato,
# editar UPDATE, eliminar DELETE!!!


class Users:  # crear una clase llamada Table1
    def __init__(self, data):
        self.id = data["idt_user"]
        self.last_name = data["last_name"]
        self.first_name = data["first_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.is_admin = data["is_admin"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_user(user):
        is_valid = True  # asumimos que esto es true
        if len(user['firstName']) < 2:
            flash("first name must be at least 2 characters.")
            is_valid = False

        if len(user['lastName']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False

        # validación con regex para email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, user["email"]):
            flash("Email must be a valid email", "register")
            is_valid = False

        if len(user["password"]) < 6:
            flash("Password must be greater than 6 characteres", "register")
            is_valid = False

        if user["password"] != user["confirmPassword"]:
            flash("Password must match", "register")
            is_valid = False
        return is_valid

    @staticmethod  # método de validación de usuario de formulario de login
    def validate_login(user):
        is_valid = True
        # validación con regex para email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, user["email"]):
            flash("El imail no es válido", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("La contraseña debe tener más de 8 caracteres", "register")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO db_jemin.t_users(first_name, last_name, email, password) VALUES ( %(firstName)s, %(lastName)s, %(email)s, %(password)s);"
        result = connectToMySQL('db_jemin').query_db(query, data)
        user = {'user.id': result}
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM t_users WHERE email = %(email)s;"
        result = connectToMySQL("db_jemin").query_db(query, data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM db_jemin.t_users WHERE idt_user= %(id)s"
        result = connectToMySQL('db_jemin').query_db(query, data)
        print(result)
        return cls(result[0])
    # ahora usamos métodos de clase para consultar nuestra base de datos

    @classmethod
    def get_all_cartera(cls):
        query = "SELECT * FROM db_jemin.t_users ORDER BY first_name ASC ;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('db_jemin').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de friends
        tb_users = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friends con cls
        for u in results:
            tb_users.append(cls(u))
        return tb_users

    @classmethod
    def get_five_cartera(cls):
        query = "SELECT * FROM db_jemin.t_users ORDER BY first_name ASC limit 5 ;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('db_jemin').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de friends
        tb_users = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friends con cls
        for u in results:
            tb_users.append(cls(u))
        return tb_users

    @classmethod
    def get_last_user(cls):
        query = "SELECT * FROM db_jemin.t_users ORDER BY created_at  DESC limit 5 ;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('db_jemin').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de friends
        tb_users = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friends con cls
        for u in results:
            tb_users.append(cls(u))
        return tb_users

    # @classmethod
    # def find_one_user(cls):
    #     query = "SELECT * FROM db_jemin.t_users WHERE first_name LIKE  '%busqueda%' ;"
    #     # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
    #     results = connectToMySQL('db_jemin').query_db(query)
    #     # crear una lista vacía para agregar nuestras instancias de friends
    #     tb_users = []
    #     # Iterar sobre los resultados de la base de datos y crear instancias de friends con cls
    #     for u in results:
    #         tb_users.append(cls(u))
    #     return tb_users

    # @classmethod
    #     def save(cls, data):
    #         query = "INSERT INTO db_user.tb_users (first_name, last_name,email,created_at) VALUES (%(fname)s,%(lname)s,%(email)s,now());"
    #         # los firts o datos verdes, son de los nombre de las columnas de la base de datos
    #         # con comillas las verdes, van solo cuando se ponen el join
    #         # los nombres morados son los que recibo y estan en  datos_recibidos.html ( imput name= morado)
    #         # se saca el query de mysql
    #         # comes back as the new row id
    #         result = connectToMySQL('db_user').query_db(query, data)
    #         print(result)
    #         return result

    #     @classmethod
    #     def update(cls, data):
    #         query = "UPDATE tb_users SET first_name=%(fname)s, last_name=%(lname)s,email%(email)s,created_at= NOW() WHERE id= %(id)s;"
    #         return connectToMySQL('db_user').query_db(query, data)

    #     @classmethod
    #     def delete(cls, data):
    #         query = "DELETE FROM tb_users WHERE id= %(id)s ;"
    #         return connectToMySQL('db_user').query_db(query, data)
