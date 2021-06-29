from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

database_file = "oracle://scott:tiger@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.248.121.76)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=3view.regress.rdbms.dev.us.oracle.com)))"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), nullable=False,primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)



@app.route("/",methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")
  
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
