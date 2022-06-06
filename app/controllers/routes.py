from xml.etree.ElementPath import find
from flask import send_from_directory
from app import app
from app.models.user import Users
from app.models.docum import Docu
from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/inicio')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not Users.validate_user(request.form):
        # redirigir a la ruta donde se renderiza el formulario de burger
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "firstName": request.form['firstName'],
        "lastName": request.form['lastName'],
        "email": request.form['email'],
        "password": pw_hash
    }

    Users.save(data)
    flash("Registro exitoso, ya puedes iniciar sesion.")
#   El DATA modifica el diccionario y la Key se deben remplazar en  el query ( parte morada)
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = {"email": request.form["email"]}
    user_in_db = Users.get_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # si obtenemos False después de verificar la contraseña
        flash("Invalid Email/Password")
        return redirect('/')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    if user_in_db.is_admin == 1:
        return redirect("/dashboard")
    # ¡¡¡Nunca renderices en una post!!!
    return redirect("/usuario/doc")


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/usuario/doc')
def usuario_inicio():
    if not 'user_id' in session:
        return redirect('/')

    return render_template('userIn.html')

# subir documento


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# descargar doc


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# ruta de save doc
@app.route('/usuario/status', methods=['GET', 'POST'])
def usuario_status():
    if not 'user_id' in session:
        return redirect('/')
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            document_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(document_url)
            print(session['user_id'])

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)

        data = {
            "documentos": document_url,
            "name": filename,
            "estatus": 1,
            "t_user_idt_user": session['user_id']
        }

        Docu.save(data)

        flash("¡Documento guardado con exito!")
        return redirect('/usuario/status')

    return render_template('status.html')


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data = {"id": session['user_id']}
    user_in_db = Users.get_one(data)

    if user_in_db.is_admin != 1:
        return redirect("/inicio")

    getFive = Users.get_five_cartera()

    return render_template('dashboard.html', getFive=getFive)

# rutas cartera


@app.route('/dashboard/cartera')
def cartera():
    if not 'user_id' in session:
        return redirect('/')
    data = {"id": session['user_id']}
    user_in_db = Users.get_one(data)

    if user_in_db.is_admin != 1:
        return redirect("/inicio")

    cartera = Users.get_all_cartera()

    return render_template('cartera.html', cartera=cartera)


@app.route('/dashboard/userDoc')
def userDoc():
    if not 'user_id' in session:
        return redirect('/')
    data = {"id": session['user_id']}
    user_in_db = Users.get_one(data)

    if user_in_db.is_admin != 1:
        return redirect("/inicio")

    getLastUsers = Users.get_last_user()
    return render_template('userDoc.html', getLastUsers=getLastUsers)


@app.route('/dashboard/showUser/<id>')
def showUser(id):
    if not 'user_id' in session:
        return redirect('/')
    data = {"id": session['user_id']}
    user_in_db = Users.get_one(data)

    if user_in_db.is_admin != 1:
        return redirect("/inicio")
    data = {
        "id_t_user": id
    }
    getUser = Docu.get_doc_by_iduser(data)
    print(getUser)
    if getUser == None:
        flash("No tiene Documentos!")
        return render_template('showUser.html')

    else:
        return render_template('showUser.html', documents=getUser)


# @app.route('/dashboard/cartera', methods=['GET'])
# def findOne():
#     if not 'user_id' in session:
#         return redirect('/')
#     data = {"id": session['user_id']}
#     user_in_db = Users.get_one(data)

#     if user_in_db.is_admin != 1:
#         return redirect("/inicio")

#     data = {
#         "id_t_user": request.args.get('id')
#     }

#     findOne = Users.find_one_user()

#     return render_template('cartera.html', findOne=findOne)
