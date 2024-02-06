from flask import Flask, render_template,request, redirect , url_for
# from flask_sqlalchemy import SQLAlchemy
# from model.model  import Todo
from datetime import datetime   
from db.db import db
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import current_user, LoginManager
check_password_hash
from flask import session

# db_setup = setup_sqlalchemy()
# db = db_setup.db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///table.db"
app.secret_key = 'anyrandomstring'

# initialization
db.init_app(app)
# db = SQLAlchemy(app)

#loginmanager code
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

app.app_context().push()

from model.model  import Todo,User

with app.app_context():
    inspector = db.inspect(db.engine)
    if not inspector.has_table(Todo.__tablename__):
        db.create_all()
    if not inspector.has_table(User.__tablename__):
        db.create_all()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///table.db"
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# app.app_context().push()



# class Todo(db.Model):
#     sno = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(200),nullable=False)
#     desc = db.Column(db.String(500),nullable=False)
#     date_created = db.Column(db.DateTime, default=lambda: datetime.utcnow())
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

#     # my_datetime = datetime.now()
#     # lowercase_string = str(my_datetime).lower()

#     def __repr__(self) -> str:
#         return f"{self.sno} - {self.title}"


# with app.app_context():
#     inspector = db.inspect(db.engine)
#     if not inspector.has_table(Todo.__tablename__):
#         db.create_all()


@app.route('/',methods=['GET','POST'])
def helloworld():
    if request.method=='GET':
        # title = request.form['title']
        # desc = request.form['desc']
        # todo=Todo(title=title,desc=desc)
        # db.session.add(todo)
        # db.session.commit()  
        # allTodo = Todo.query.all()
        # allTodo_str_dates = [{'title': todo.title, 'desc': todo.desc, 'date_created': str(todo.date_created)} for todo in allTodo]
        # return render_template('index.html', allTodo=allTodo_str_dates) 
    #     return redirect(url_for('helloworld')) 

    # if request.method == "GET":
    #     allTodo = Todo.query.all()
    #     print("-------------------------------------",allTodo)
    #     allTodo_str_dates = [{'sno':todo.sno,'title': todo.title, 'desc': todo.desc, 'date_created': str(todo.date_created)} for todo in allTodo]
        return render_template('login.html')

@app.route('/show')
def product():
    #table_name.query
    allTodo= Todo.query.all()
    print(allTodo)
    return 'this is my product'

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    #table_name.query
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/index") 

    todo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html' , todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    #table_name.query
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # return redirect(url_for('helloworld')) 
    return redirect("/index")

@app.route('/index',methods=['GET','POST'])
def index():
         if request.method=='POST':
            title = request.form['title']
            desc = request.form['desc']
            todo=Todo(title=title,desc=desc,user_sno=session['user_id'])
            db.session.add(todo)
            db.session.commit()  
            return redirect(url_for('index'))
         
         if request.method == "GET":
            allTodo = Todo.query.filter_by(user_sno=session['user_id']).all()
            print("-------------------------------------",allTodo)
            allTodo_str_dates = [{'sno':todo.sno,'title': todo.title, 'desc': todo.desc, 'date_created': str(todo.date_created)} for todo in allTodo]
            return render_template('index.html' , allTodo=allTodo_str_dates )
    


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            return "Username already exists. Please choose a different one."
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # Create a new user instance
        new_user = User(username=username, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # conn = sqlite.connect(table)
        # cursor = conn.cursor()

        # cursor.execute('INSERT INTO user (username,password) VALUES (?,?)', (username, hashed_password))

        # conn.commit()
        # conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # print(username)
        # print(password)

        user = User.query.filter_by(username=username).first()
        # user = User.query.filter_by(password=password).first()

        # todo=Todo.query.filter_by(username=username, password=password).first()
        # conn = sqlite3.connect(table)
        # cursor = conn.cursor()

        # cursor.execute('SELECT * FROM user WHERE username = ?',(username,))
        # user = cursor.fetchone()

        # conn.close()

        # print(user)

        
        if user and check_password_hash(user.password, password):
            # print("hiee")
            # return "Login successful!"
            session['user_id'] = user.sno
            return redirect(url_for('index'))
        else:
            return "Login failed Check your username and password."
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session['user_id'] = 0
    return redirect(url_for('helloworld'))

    

# @app.route('/style')
# def style():
#     allStyle = Todo.query.all()
#     print(allStyle)
#     return 'this is the style page'

# @app.route('/rest')
# def rest():
#     allrest = Todo.query.all()
#     print(allrest)
#     return 'Take the rest'



@app.route('/items')
def item():
    return 'todo this is items list'

@app.route('/lists')
def lists():
    return 'this is my lists'


if __name__ == "__main__":
    app.run(debug=True,port = 8000)


