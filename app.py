from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C://Users//vampirepapi//Desktop//nowhere//Internship//flask//todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow )

    def __repr__(self) -> str:
    	return f"{self.Sno} - {self.title}"



@app.route('/', methods =['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		title = request.form['title']
		desc = request.form['desc']
		todos = todo(title = title, desc = desc)
		db.session.add(todos)
		db.session.commit()

	alltodo = todo.query.all()
	return render_template('index.html', alltodo = alltodo)
   
@app.route('/delete/<int:Sno>')
def delete(Sno):
	todos = todo.query.filter_by(Sno=Sno).first()
	db.session.delete(todos)
	db.session.commit()
	return redirect("/")

@app.route('/update/<int:Sno>', methods =['GET', 'POST'])
def update(Sno):
	if request.method == 'POST':
		title = request.form['title']
		desc = request.form['desc']
		todoe = todo.query.filter_by(Sno=Sno).first()
		todoe.title = title
		todoe.desc = desc
		db.session.add(todoe)
		db.session.commit()
		return redirect("/")
	todoe = todo.query.filter_by(Sno=Sno).first()
	return render_template('update.html', todoe = todoe)

if __name__ == "__main__":
	app.run(debug=True,)
