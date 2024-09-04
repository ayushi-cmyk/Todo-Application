from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password123@localhost:3306/mytodo"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class myTodo(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.num}{self.task}"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form['task']
        if task.strip():
            mytodo = myTodo(task=task.strip())
            db.session.add(mytodo)
            db.session.commit()
    allTodo = myTodo.query.all()
    return render_template('mytodo.html', allTodo=allTodo)

@app.route('/remove/<int:num>')
def remove(num):
    mytodo = myTodo.query.filter_by(num=num).first()
    db.session.delete(mytodo)
    db.session.commit()
    return redirect("/")

@app.route('/new/<int:num>', methods=['GET', 'POST'])
def update(num):
    if request.method == 'POST':
        task = request.form['task']
        mytodo = myTodo.query.filter_by(num=num).first()
        mytodo.task = task
        db.session.add(mytodo)
        db.session.commit()
        return redirect("/")
    mytodo = myTodo.query.filter_by(num=num).first()
    return render_template('mytodo_update.html',mytodo=mytodo)


if __name__ == "__main__":
    app.run(debug=True)