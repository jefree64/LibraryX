import sqlite3
import datetime
import csv
from models import *
from date import date_format


today = datetime.date.today()


def raw(file):
	with open(file) as file:
		x = csv.reader(file)
		return tuple(x)

	
	
class _db:
	con = sqlite3.connect('db.sqlite',check_same_thread = False)
	
	tables = {
		"admin" : admin,
		"book" : book,
		"staff" : staff,
		"student" : student,
		"lending" : lending
	}
	
	def query(self, query,records):
		result = {}
		try:
			with self.con as con:
				con.execute(query,records)
				con.commit()
				result["success"] = records
		except sqlite3.IntegrityError as e:
			result["error"] = str(e)
		except sqlite3.OperationalError as e:
			result["error"] = str(e)
		except :
			result["error"] = "Something Wrong"
		return result
		
	def addmany(db, table, records):
		cmd = {
			"staff" : "(?,?,?)",
			"student" : "(?,?,?,?,)",
			"book" : "(?,?,?,?,?)"
		} 
		try:
			with db.con as db:
				db.executemany(f"insert into {table} values {cmd[table]}",records)
				db.commit()
				return { "success" : "Records SuccessFully Added !"}
		except sqlite3.IntegrityError:
			return {
				"error" : "Records Are Already In"
			}
		except sqlite3.ProgrammingError:
			return {"error" : "This File Not Suitable"}
			
	def fetchone(self, table, id,id1 = None):
		ids = {
			"book" : f"id = '{id}'",
			"staff" : f"id = '{id}'",
			"student" : f"id = '{id}'",
			"lending" :  f"bid = '{id}' and lid = '{id1}'" ,
			"admin" : f"id = '{id}'"
		}
		query = f"select * from {table} where {ids[table]}"
		with self.con as con:
			cur = con.cursor()
			cur.execute(query)
			res = cur.fetchone()
			if res is None:
				return None
			return self.tables[table](res)
	
	def fetchall(self, table):
		query = "select * from {}".format(table)
		with self.con as con:
			cur = con.cursor()
			cur.execute(query)
			result = cur.fetchall()
			if result is None:
				return None
			return stack([ self.tables[table](rec) for rec in result ])
			
	def add(self, table, records):
		tables = {
		"book" : "insert into book values(?,?,?,?,?)",
		"staff" : "insert into staff values(?,?,?)",
		"student" : "insert into student values(?,?,?,?)",
		"lending" : "insert into lending (bid,bname,lid,lname,dol,dor,status) values(?,?,?,?,?,?,?)"
		}
		return self.query(tables[table],records)
		
		
	def delete(db, table, id1, id2 = None) :
		condition = {
			"lending" : f"bid = '{id1}' and lid = '{id2}'",
			"student" : f"id = '{id1}'"
		}
		x = db.fetchone(table, id1,id2)
		if x is None:
			return { "error" : "record not found" }
		if table == "lending":
			query = "delete from "+table+" where "+condition[table]
		else:
			query = "delete from {} where id = '{}'".format(table, id1)
		with db.con as con:
			con.execute(query)
			con.commit()
			return {"success" : "Deleted" }
			
	def deleteall(db,table):
		query = "delete from {}".format(table)
		with db.con as db:
			c = db.cursor()
			c.execute(query)
			db.commit()
			
	def update(db,table,id,x):
		queries = {
			"book" : f" set count = '{x}' where id = '{id}'"
		}
		with db.con as con:
			con.execute("update "+ table +queries[table])
			con.commit()

	
	def lending(db, Book,Lender):
		result = {}
		exist = db.is_lending(Book.id,Lender.id)
		if exist:
			result["error"] = ["already lended"]
			return result
		if int(Book.count) > 0:
			dol = str(today)
			dor = date_format(dol)
			new = (
			Book.id,Book.name,
			Lender.id,Lender.name,
			dol,dor,"onlending"
			)
			result = db.add("lending",new)
			if "error" in result:
				return result
		
			db.update(
			"book",Book.id,
			str(int(Book.count) - 1)
			)
			result["sucess"] = "Success Fully added"
		else:
			result["error"] = "Not available"
		return result
		
	def return_lending(db,L):
		query = f"update lending set status = 'returned' where id = {L.id}"
		with db.con as con:
			c = con.cursor()
			c.execute(query)
			con.commit()
		b = db.fetchone("book",L.bid)
		db.update(
			"book",
			b.id,
			str( int(b.count) + 1 )
		)
		return "Returned Successfully !"
			
	def view_lending(db, t, id):
		query = "select * from lending where {} = '{}' ".format( t, id )
		with db.con as con:
			cur = con.cursor()
			cur.execute(query)
			out = cur.fetchall()
			if out:
				return [
					db.tables["lending"](rec) for rec in out
				]
			
			
	def onlending(db):
		query = "select * from lending where status = 'onlending'"
		with db.con as con:
			c = con.cursor()
			c.execute(query)
			return [
				db.tables["lending"](row) \
				for row in c.fetchall()
			]
			
	def returned(db):
		query = "select * from lending where status = 'returned'"
		with db.con as con:
			c = con.cursor()
			c.execute(query)
			x = c.fetchall()
			if x:
				return [
				db.tables["lending"](rec) for rec in x
				]

	def is_lending(db,bid,lid):
		query = f"select * from lending where (lid = '{lid}' and bid = '{bid}') and status = 'onlending'"
		with db.con as con:
			c = con.cursor()
			c.execute(query)
			out = c.fetchone()
			if out is None:
				return None
			
			return db.tables["lending"](out)
			



 
 

if __name__ == "__main__":
	
	db = _db()
	
	students = db.fetchall("student")
	books = db.fetchall("book")
	lending = db.fetchall("lending")
	print(len(books))
