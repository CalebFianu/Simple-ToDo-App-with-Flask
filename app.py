from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class TodoApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %>' % self.id

@app.route("/", methods = ['POST','GET'])

def index():
    if request.method == 'POST':
        # return "It works!"
        task_content = request.form['content']
        new_task = TodoApp(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is a problem!" 
    else:
        tasks = TodoApp.query.order_by(TodoApp.date_created).all()
        return render_template('todofrontend/build/index.html', tasks=tasks)
#Delete here
@app.route('/delete/<int:id>')

def delete(id):
    task_delete = TodoApp.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is another problem'

#Update here
@app.route('/update/<int:id>', methods = ['POST','GET'])

def update(id):
    task_update = TodoApp.query.get_or_404(id)

    if request.method == 'POST':
        task_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task=task_update)

    

if __name__ == "__main__":
    app.run(debug=True)







