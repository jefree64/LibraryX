from flask import *
from db import *
from os import path

app = Flask(__name__)
app.secret_key = "wallahi64"
app.config["DATASETS"] = "static/files"



# Admin
@app.route('/',methods = ["GET","POST"])
def index():
	"""
	if 'admin' in session:
		return render_template('index.html',name = session["admin"][1],book = book())
	return redirect("/login")"""
	return render_template("book/add.html",books = Book.view())
	
# Admin - Login
@app.route('/login',methods = ["POST","GET"])
def login():
	error = None
	if request.method == "POST":
		id = request.form["adminid"]
		password = request.form["password"]
		auth = admin().is_user(id)
		if auth:
			if auth[2] == password:
				session["admin"] = auth
				return redirect("/")
			error = "Password Dis_matched"
		else :
			error = "Admin Id Dis_Matched"
	return render_template("login.html",error = error)

# Students..
# Student view
@app.route('/student')
def student():
	if "admin" in session:
		return render_template("student/student.html", students = Student().view())
	return redirect('/login')
# student Add
@app.route('/add_student',methods = ["GET","POST"])
def add_students():
	if "admin" in session:
		if request.method == "POST":
			id = request.form["id"]
			name = request.form["name"]
			year = request.form["year"]
			mobile = request.form["mobile"]
			Studnt.add(id,name,year,mobile)
			return redirect("/student")
		return render_template("/student/add.html")
	return redirect('/login')
# delete student
@app.route("/delstud",methods = ["POST"])
def delstud():
	id = request.form.get("id")
	query = "delete from student where id = '{}'".format(id)
	Studnt.cursor(query)
	return redirect("/student")

# student upload csv
@app.route("/upload_student", methods = ["POST", "GET"])
def upload_student():
	error = None
	if request.method == "POST":
		file = request.files["file"]
		file.save(path.join(app.config["DATASETS"],file.filename))
		error = Studnt.upload(path.join(app.config["DATASETS"],file.filename))
		if error is None :
			return redirect('/student')
	return render_template('student/upload.html',er = error)
	

@app.route("/lendbystud",method = ["POST"])
def  lendbystud():
	pass



# Staff main
@app.route("/staffs")
def staffs():
	if "admin" in session:
		return render_template("staff/staff.html")
	return redirect("/login")


# LENDING..
# Lending - add
@app.route("/lending", methods = ["GET","POST"])
def lending():
	if "admin" in session:
		error = None
		if request.method == "POST":
			uid = request.form.get("uid")
			bid = request.form.get("bid")
			user = request.form.get("ufield")
			exist = len.is_lending(uid,bid)
			if exist is False:
				add = len.add(bid, user, uid)
				if add == "002":
					error = "Book Not Found"
				elif add == "001":
					error = "User Not Found"
				elif add == "003":
					error = "Book Lending Out"
			else:
				error = "User Already Lended the Same Book"
		return render_template("lending/index.html",error = error,len = len.view())
	return redirect('/login')





# BOOK..
# add Book
@app.route("/add_book", methods = ["POST"])
def add_book():
			id, name, auth, pub, count \
			=\
			request.form["id"],\
			request.form["name"],\
			request.form["author"],\
			request.form["publication"],\
			request.form["count"]
			
			if Book.add(id,name,auth,pub,count) is None:
				return redirect("/")
# Upload Book.
@app.route("/upload_book", methods = ["POST", "GET"])
def upload_book():
	error = None
	if request.method == "POST":
		file = request.files["file"]
		file.save(path.join(app.config["DATASETS"],file.filename))
		Book.upload(path.join(app.config["DATASETS"],file.filename))
		return redirect('/')
	return render_template('book/upload.html',er = error)
# delete 
@app.route("/del_book", methods = ["POST","GET"])
def del_book():
	if request.method == "POST":
		id = request.form.get("id")
		query = "delete from book where id = '{}'".format(id)
		Book.cursor(query)
		return redirect("/")



# Logout..
@app.route("/logout")
def logout():
	if "admin" in session:
		del session["admin"]
		return redirect("/") 
	return redirect("/")




@app.route("/SuperUserArchMan",methods = ["POST","GET"])
def SuperUserArchMan():
	if request.method == "POST":
		id = request.form["id"]
		name = request.form["name"]
		password = request.form["pass"]
		admin().add(id,name,password)
		return redirect("/")
	return render_template("add_admin.html")
	
	
if __name__ == "__main__":
	app.run()