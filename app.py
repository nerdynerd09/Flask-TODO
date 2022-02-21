from datetime import datetime
from flask import Flask, redirect,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

# Setting up flask app
app = Flask(__name__)

# Setting up Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from app import db
# db.create_all()
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if(request.method=='POST'):
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    # return "<p><h1>Hello, World!</h1></p>"
    return render_template("index.html", alltodos=alltodo)

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "this is show page"


@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if(request.method=='POST'):
        updateTodo = Todo.query.filter_by(sno=sno).first()    
        title = request.form['title']
        desc = request.form['desc']
        updateTodo.title = title
        updateTodo.desc = desc
        db.session.add(updateTodo)
        db.session.commit()
        return  redirect("/")

    updateTodo = Todo.query.filter_by(sno=sno).first()    
    return render_template('update.html',todo=updateTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    delTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delTodo)
    db.session.commit()
    return  redirect("/")

if __name__=="__main__":
    app.run(debug=True,port=8000)  #Always set `debug=False` when updating it on live server