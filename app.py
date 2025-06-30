from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gmao.db'
db = SQLAlchemy(app)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    equipment = db.relationship('Equipment', backref=db.backref('tasks', lazy=True))

@app.route('/')
def index():
    tasks = Task.query.all()
    equipments = Equipment.query.all()
    return render_template('index.html', tasks=tasks, equipments=equipments)

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    name = request.form['name']
    description = request.form.get('description')
    eq = Equipment(name=name, description=description)
    db.session.add(eq)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_task', methods=['POST'])
def add_task():
    equipment_id = request.form['equipment_id']
    description = request.form['description']
    task = Task(equipment_id=equipment_id, description=description)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = request.form['status']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)
