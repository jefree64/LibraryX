class admin:
	def __init__(a,records):
		a.id,a.name,a.password = records
	
	def json(a):
		data = {
			"id" : a.id,
			"name" : a.name,
			"password" : a.password
		}
		return data

##############

class book:
	def __init__(b,records):
		b.id,b.name,b.author,b.publication,b.count = records
		
	def __repr__(b):
		return f"|{b.id},{b.name},{b.count}|"
		
#############

class student:
	def __init__(s,records):
		s.id,s.name,s.year,s.mobile = records
		
	def __repr__(s):
		return f"{s.id},{s.name},{s.year}"

####$#########

class staff:
	def __init__(s,records):
		s.id,s.name,s.mobile = records

class lending:
	def __init__(l,records):
		l.id,l.bid,l.bname,l.lid,l.lname,l.dol,l.dor,l.status = records
	def tolist(l):
		return (l.bid,l.bname,l.lid,l.lname,l.dol,l.dor)
	
	def __repr__(l):
		return f"{l.id},{l.lname},{l.bname},{l.status}"
		
		
class stack:
	def __init__( self, args ):
		self.value =  args
	def len( self ):
		return len(self.value)
	def all(self):
		return self.value