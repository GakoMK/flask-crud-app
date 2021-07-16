import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

# app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = "p9Bv<3Eid9%$i01"

db = SQLAlchemy(app)



@app.route('/', methods=["GET", "POST"])
def home():
    books = Book.query.all()
    return render_template("books_list.html", books=books)
    

@app.route('/new', methods=["GET", "POST"])
def newBook():
    if request.form:
        title = request.form.get("title")
        author = request.form.get("author")
        if not request.form['title'] or not request.form['author']:
            flash('Please enter all the fields', 'error')
        else:
            newBook = Book(title = title, author = author)
            db.session.add(newBook)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('home'))
    return render_template('new.html') 


@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.form:
        id = request.form['id']
        toDeleteObj = Book.query.filter(Book.id == id).first()   
        db.session.delete(toDeleteObj)
        db.session.commit()
        flash('Record was successfully deleted')
        return redirect(url_for('home'))
    


@app.route('/edit/', methods=["GET", "POST"])
def edit():
    id = request.args['id'] #<a class="btn btn-primary" href="/edit/?id={{book.id}}">Edit</a>
    print(id)
    editBook = Book.query.filter(Book.id == int(id)).first()
    if request.method == "GET":
        return render_template('edit.html', books=editBook)      

@app.route('/update', methods=["GET", "POST"])
def update():
    if request.form:
        id = request.form.get("id")
        title = request.form.get("title")
        author = request.form.get("author")
        if not request.form['title'] or not request.form['author']:
            flash('Please enter all the fields', 'error')
        else:
            print('id: '+str(id))
            print('title: '+title)
            print('author: '+author)
            editBook = Book.query.filter(Book.id == id).first()
            editBook.title = title
            editBook.author = author
            db.session.commit()
            flash('Record was successfully updated')   
            return redirect(url_for('home')) 
    return redirect(url_for('home'))


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self): # object as a string
        return "<Title: {}>".format(self.title)



if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    app.run(host='0.0.0.0', debug=True)   
    