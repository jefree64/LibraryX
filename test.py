from flask import *
from db import _db, lending,today,date_format, raw

app = Flask(__name__)
app.secret_key = "definition9806"
app.config["files"] = "static/files/"


db = _db()



def admin():
	if "admin" in session:
		return True
	return False



@app.route("/")
def main():
	if admin():
		return render_template("book/index.html",books = db.fetchall("book"))
	return redirect("/login")

@app.route("/login",methods = ["GET","POST"])
def login():
	error = None
	if request.method == "POST":
		id = request.form.get('id')
		password = request.form.get("password")
		auth = db.fetchone("admin",id)
		if auth:
			if auth.password == password:
				session["admin"] = auth.json()
				return redirect("/")
			else:
				flash("Password was Wrong !")
		else:
			flash("Admin Doesn't Exist !.")
	return render_template("login.html",error = error)

 


@app.route("/add_book",
methods = ["POST"]
)
def add_book():
	if admin():
		id = request.form["id"]
		name = request.form["name"]
		auth = request.form["author"]
		pub = request.form["publication"]
		co = request.form["count"]
		rex = (
			id,name,auth,pub,co
		)
		flash(db.add("book",rex))
		return redirect("/")
	return redirect("/login") 

@app.route(
	"/import_book",
	methods = ["POST", "GET"]
)
def import_book():
	result = None
	if admin():
		if request.method == "POST":
			file = request.files["file"]
			x = app.config["files"] + file.filename
			file.save(x)
			records = raw(x)
			result = db.addmany("book",records)
			flash(result)
		return render_template("book/upload.html",b = "/")
	return redirect("/login")
		

@app.route("/del_book",
methods = [ "GET", "POST" ]
)
def del_book():
	if request.method != "POST":
		return render_template("book/delete.html")
	id = request.form["id"]
	x = db.view_lending("bid",id)
	if x is None:
		flash(db.delete("book",id))
	else:
		flash({
			"error" : "Book Is Onlending"
		})
	return redirect("/del_book")





@app.route("/staff")
def staff():
	if admin():
		return render_template(
		"staff/staff.html",
		staffs = db.fetchall("staff"))
	return redirect("/login")

@app.route(
	"/addstaff",
	methods = ["POST"]
)
def addstaff():
	if admin():
		id = request.form["id"]
		name = request.form["name"]
		mobile = request.form["mobile"]
		x = db.add("staff",[id,name,mobile])
		flash(x)
		return redirect("/staff")
	return redirect("/login")



@app.route(
	"/del_staff", 
	methods = ["POST","GET"]
)
def delstaff():
	if admin():
		if request.method == "POST":
			id = request.form["id"]
			x = db.delete("staff",id)
			flash(x)
			return redirect("/del_staff")
		return render_template("staff/delete.html")
	return redirect("/login")


@app.route(
"/import_staff",
methods = [ "GET", "POST" ]
)
def import_staff():
	if admin():
		if request.method != "POST":
			return render_template('staff/upload.html', b = "/staff")
		rec = request.files["file"]
		x = app.config["files"] + rec.filename
		rec.save(x)
		rec = raw(x)
		out = db.addmany("staff",rec)
		flash(out)
		return redirect("/import_staff")
	return redirect('/login')



@app.route("/student")
def student():
	if admin():
		return render_template("/student/student.html", students = db.fetchall("student"))
		

@app.route("/add_student",
methods = ["POST"]
)
def add_student():
	id = request.form["id"]
	name = request.form["name"]
	year = request.form.get("year")
	mobile=request.form.get("mobile")
	flash(db.add(
	"student",
	(id,name,year,mobile)
	))
	return redirect("/student")


@app.route("/del_stud",methods = ["POST", "GET"])
def delstud():
	if admin():
		if request.method == "POST":
			id = request.form["id"]
			result = db.delete("student", id)
			flash(result)
			return redirect("/del_stud")
		return render_template("student/delete.html")
	return redirect("/login") 

@app.route('/import_student')
def imp_stud():
	if admin():
		if request.method == "GET":
			return render_template('student/upload.html')
	return redirect('/login')

 

@app.route("/lending",methods = ["POST","GET"])
def lending():
	if "admin" in session:
		result = {}
		if request.method == "POST":
			bid = request.form["bid"]
			lid = request.form["uid"]
			ufield = request.form["ufield"]
			book = db.fetchone("book",bid)
			lender = db.fetchone(ufield,lid)
			if book and lender:
				result = db.lending(book,lender)
			elif lender is None:
				result["error"] = "Lender Does'nt Exist ...!"
			elif book is None:
				result["error"] = "book Does'nt Exist ...!"
			else:
				result["error"] = "Something Went Wrong"
		return render_template(
		"Lending/index.html",
		len = db.onlending(), 
		result = result
		)
	return redirect("/login")

@app.route("/view_lending",methods = ["POST"])
def view_lending():
	if admin():
		if request.method == "POST":
			id = request.form["id"]
			field = request.form["field"]
			records = db.view_lending("lid",id)
			lender = db.fetchone(field,id)
			return render_template(
				"Lending/view.html",
				lendings = records,
				lender = lender
		)
	return redirect("/login")


 
@app.route(
"/return_lending",
methods = ["POST","GET"]
)
def return_lending():
	if admin():
		if request.method == "POST":
			lid = request.form["lid"]
			bid = request.form["bid"]
			len = db.is_lending(bid,lid)
			if len:
				result = db.return_lending(len)
				flash({"success" : result})
			else:
				flash({"error" : "Lending Not Found "})
				return redirect("/return_lending")
		return render_template("Lending/return.html")
	return redirect('/login')



@app.route("/returned")
def returned():
	if admin():
		rec = db.returned()
		return render_template(
			"Lending/returned.html",
			lendings = rec
		)
	return redirect("/login")











@app.route("/logout")
def logout():
	if admin():
		del session["admin"]
		return redirect("/")
	return redirect("/login")










if __name__ == "__main__":
    app.run("192.168.235.7",5000,debug=True)
