from pymongo import *
from datetime import *
import random
from security_utils import *
import base64

class Model(object):


	##### CONSTRUCTOR #####
	def __init__(self):
		#self.__url = "mongodb://luigonsec:aks1991@ds033059.mongolab.com:33059/fabx"
		#self._bd   = MongoClient(self.__url)['fabx']

		self.__url = "mongodb://superuser:fabber@ds063879.mongolab.com:63879/fabexpertizer"
		self._bd   = MongoClient(self.__url)['fabexpertizer']


	def get_collection(self,nombre):
		return self._bd[nombre]	





class Session(Model):
	
	
	def __init__(self):
		super(Session,self).__init__()
		self.__model=self.get_collection("sessions")
		self.__expire=15
	def login(self,username):
		self.__model.remove({"_id" : username})
		secure_cookie=sha512(username+str(random.random()))
		expire=datetime.now()+timedelta(minutes=self.__expire)
		datas                         ={}
		datas["_id"]                  =username
		datas["fabexpertizersession"] =secure_cookie
		datas["expire"]               =expire
		self.__model.insert(datas)
		return secure_cookie

	def get_session(self,username):
		session = self.__model.find_one({"_id" : username})
		if session:
			return session["fabexpertizersession"]
		else:
			return None
	def verify_cookies(self,cookies):
		sessionID=cookies.get('fabexpertizersession')
		username=cookies.get('username')
		if not sessionID:
		    return False
		if sessionID != self.get_session(username):
		    return False
		session=self.__model.find_one({"_id" : username})
		if not session:
		    return False
		if session['expire']<datetime.now():
		    self.__model.remove({"_id" : username})
		    return False
		secure_cookie=sha512(username+str(random.random()))
		self.__model.update({"_id" : username}, {"$set": {"fabexpertizersession" : secure_cookie , "expire" : datetime.now()+timedelta(minutes=self.__expire)}})   
		return secure_cookie

	def is_login(self,username,cookies):
		sessionID=cookies.get('fabexpertizersession')
		if username != cookies.get('username'):
		    return False
		if not sessionID:
			return False
		if sessionID != self.get_session(username):
		    return False
		session=self.__model.find_one({"_id" : username})
		if not session:
		    return False
		if session['expire']<datetime.now():
		    self.__model.remove({"_id" : username})
		    return False
		return True   

class Belt(Model):

	def __init__(self):
		super(Belt,self).__init__()
		self.__model=self.get_collection("belts")

	def get_belt(self,points):
		belt = self.__model.find_one({"min" : {"$lte" : points}, "max" : {"$gte" : points}})
		return belt

class Fabber(Model):

	##### CONSTRUCTOR #####
	def __init__(self):
		super(Fabber,self).__init__()
		self.__model=self.get_collection('fabbers')

	def add_follow(self,username,followed):
		if not self.get_fabber(username) or not self.get_fabber(followed):
			return False
		self.__model.update({"username" : username},{"$push" : {"followings" : followed  }})
		self.__model.update({"username" : followed},{"$push" : {"followers"  :	username }})
		return True

	def add_fabex(self,username,oid):
		self.__model.update({"username" : username},{"$push" : {"fabexs" : oid}})

	def add_fablab(self,username,fablab):
		self.__model.update({"username" : username},{"$push" : {"fablabs" : fablab }})
		return True

	def add_comment(self,username,oid):
		self.__model.update({"username" : username},{"$push" : {"comments" : oid}})

	def add_points(self,username,amount):
		self.__model.update({"username" : username},{"$inc" : {"points" : amount}})
		return True

	def add_request(self,username,fablab):
		self.__model.update({"username" : username},{"$push" : {"requests" : fablab}})
		return True	
	
	def add_photo(self,username,source):
		self.__model.update({"username" : username}, {"$set" : {"photo" : source}})

	def add_unfollow(self,username,unfollowed):
		if not self.get_fabber(username) or not self.get_fabber(unfollowed):
			return False
		self.__model.update({"username" : username  },{"$pull" : {"followings" : unfollowed }})
		self.__model.update({"username" : unfollowed},{"$pull" : {"followers"  : username   }})
		return True
	
	def add_like(self,username,oid):
		if self.__model.find_one({"username" : username, "$in" : {"likes" : [oid]}}):
			return False
		self.__model.update({"username" : username},{"$push" : {"likes" : oid}})
		return True

	def create_fabber(self,name,surname,username,email,password):
		try:
			identificador =Counter("fabber_oid")
			siguiente     =identificador.get_next()
			identificador.update_next()
			datas               = {}
			datas["_id"]        = siguiente
			datas["name"]       = name
			datas["surname"]    = surname
			datas["username"]   = username
			datas["email"]      = email
			datas["password"]   = password
			datas["photo"]      = "img/no-profile-photo.jpg"
			datas["admin"]      = False
			datas["superuser"]  = False
			datas["points"]		= 0
			datas["fablabs"]    = []
			datas["requests"]	= []
			datas["likes"]      = []
			datas["followers"]  = []
			datas["followings"] = []
			datas["comments"]   = []
			datas["fabexs"]     = []
			datas["date"]       = datetime.now()
			self.__model.insert(datas)
			return True
		except:
			return False

	def delete_like(self,username,oid):
		if not self.__model.find({"username" : username, "$in" : {"likes" : [oid]}}):
			return False
		self.__model.update({"username" : username},{"$pull" : {"likes" : oid}})
		return True
	
	def delete(self,username):
		res=self.__model.remove({"username" : username})
		return True if res['n'] > 0 else False
	
	def delete_all(self):
		self.__model.remove()
		return True

	def delete_fabex(self,username,oid):
		self.__model.update({"username" : username} , {"$pull" : {"fabexs" : oid }})

	def delete_request(self,username,fablab):
		self.__model.update({"username" : username},{"$pull" : {"requests" : fablab}})
		return True	

	def delete_comment(self,username,oid):
		self.__model.update({"username" : username},{"$pull" : {"comments" : oid}})

	def delete_all_comments(self):
		self.__model.update({},{"$set" : {"comments" : [] }})
		return True

	def exists_email(self,email):
		res=self.__model.find_one({"email" : email})
		return True if res else False

	def exists_username(self,username):
		res=self.__model.find_one({"username" : username})
		return True if res else False

	def exists_request(self,username,fablab):
		res=self.__model.find_one({"username" : username, "requests" : {"$in" : [fablab]}})
		return True if res else False

	def get_fabbers(self,sort="username",order = ASCENDING):
		fabbers=self.__model.find({},{"_id" : 0, "password" : 0 }).sort([(sort,order)])
		return fabbers

	def get_fablabs(self,username):
		fablab=Fablab()
		fablabs=fablab.get_fabber_fablabs(username)
		return fablabs

	def get_fabber(self,username):
		fabber=self.__model.find_one({"username" : username})
		return fabber

	def get_fabber_belt(self,username):
		points=self.__model.find_one({"username" : username})["points"]
		belt=Belt()
		res = belt.get_belt(points);
		return res;

		
	def admin_fablab(self,fabber,fablab):
		try:
			self.__model.update({"username" : fabber},{"$set" : {"admin" : True}, "$push" : {"fablabs" : fablab}})
			return True
		except:
			return False
	def is_superuser(self,username):
		fabber=self.get_fabber(username)
		return fabber['superuser']

	def is_admin(self,username):
		fabber=self.get_fabber(username)
		return fabber['admin']

	def leave_fablab(self,username,fablab):
		self.__model.update({"username" : username},{"$pull" : {"fablabs" : fablab}})
		return True

	def set_fabber(self,username,field,value):
		self.__model.update({"username" : username},{"$set" : {field : value}})

	def valid_login(self,username,password):
	    if self.__model.find({"username" : username, "password" : password}).count() == 0:
	        return False
	    else:
	        return True



class Fablab(Model):

	def __init__(self):
		super(Fablab,self).__init__()
		self.__model=self.get_collection("fablabs")
	
	def add_admin(self,fablab,fabber):
		res=self.__model.find_one({"fablab" : fablab, "members" : {"$in" : [fabber]}})
		operations={}
		if not res:
			operations["members"] =  fabber
		
		res=self.__model.find_one({"fablab" : fablab, "admins" : {"$in" : [fabber]}})
		if not res: 
			operations["admins"] = fabber
			self.__model.update({"fablab" : fablab} , {"$push" : operations })
			return True
		else:
			return False

	def add_fablab(self,name,fablab,address,description,phone,email):
		try:
			identificador =Counter("fablab_oid")
			siguiente     =identificador.get_next()
			identificador.update_next()
			data                = {}
			data["_id"]			= siguiente
			data["name"]        = address
			data["fablab"]		= fablab
			data["description"] = description
			data["photo"]       = "img/no-fablab-photo.jpg"
			data["phone"]       = phone
			data["email"]       = email
			data["created"] 	= datetime.now()
			data["admins"]		= []
			data["members"]		= []
			data["requests"]    = []
			self.__model.insert(data)
			return True
		except:
			return False

	def add_member(self,fablab,username):
		self.__model.update({"fablab" : fablab} , {"$push" : {"members" : username}})
		fabber=Fabber()
		fabber.add_fablab(username,fablab)
		return True

	def has_member(self,fablab,username):
		res = self.__model.find({"fablab" :  fablab},{"$in" : {"members" : username}})
		return True if res else False

	def delete_member(self,fablab,username):
		self.__model.update({"fablab" : fablab} , {"$pull" : {"members" : username}})
		fabber=Fabber()
		fabber.leave_fablab(username,fablab)
		return True
	
	def add_photo(self,fablab,source):
		self.__model.update({"fablab" : fablab}, {"$set" : {"photo" : source}})
		return True

	def add_points(self,fablab,points):
		self.__model.update({"fablab" : fablab},{"$inc" : {"points" : points}})
		return True

	def add_request(self,fablab,username):
		self.__model.update({"fablab" : fablab}, {"$push" : {"requests" : username}})
		return True

	def delete_request(self,fablab,username):
		self.__model.update({"fablab" : fablab}, {"$pull" : {"requests" : username}})
		return True
		
	def exists_fablab(self,fablab):
		res=self.__model.find_one({"fablab" : fablab})
		return True if res else False
	
	def exists_request(self,fablab,username):
		res=self.__model.find_one({"fablab" : fablab, "requests" : {"$in" : [username]}})
		return True if res else False	
	
	def get_fablab(self,fablab):
		res=self.__model.find_one({"fablab" : fablab})
		return res if res else False

	def get_fabber_fablabs(self,username):
		res=self.__model.find({"members" : {"$in" : [username]}},{"fablab" : 1, "name" : 1, "photo" :1 , "admins" : 1})
		return res
	def get_fablab_by_admin(self,username):
		res=self.__model.find_one({"admins" : {"$in" : [username]}})
		return res if res else False

	def get_fablabs(self):
		return self.__model.find()

class Fabex(Model):

	def __init__(self):
		super(Fabex,self).__init__()
		self.__model=self.get_collection('fabexs')
	
	def get_fabex_author(self,author):
		fabexs=self.__model.find({"author" : author})
		return fabexs
	def get_username(self,oid):
		fabex=self.__model.find_one({"_id" : oid})
		if fabex:
			return fabex["author"]
		else:
			return	False

	def get_fabexs(self,keywords):
		if keywords:
			filters=[]
			for word in keywords:
				nameq    ={"name" : {"$regex" : word}}
				authorq  ={"author" : {"$regex" : word}}
				machineq ={"machine" : {"$regex" : word}}
				titleq   ={"title" : {"$regex" : word}}
				filters.append(nameq)
				filters.append(authorq)
				filters.append(machineq)
				filters.append(titleq)
			fabexs=self.__model.find({"$or" : filters})
		else:
			fabexs=self.__model.find()
		return fabexs

	def oid_exists(self,oid):
		res=self.__model.find_one({"_id" : oid})
		return True if res else False

	def add_like(self,oid,username):
		if self.__model.find_one({"_id" : oid, "$in" : {"likes" : [username]}}):
			return False
		self.__model.update({"_id" : oid},{"$push" : {"likes" : username}, "$inc" : {"totalLikes" : 1}})
		return True

	def delete(self,oid):
		author=self.get_username(oid)
		if author:
			self.__model.remove({"_id" : oid})
			return author
		else:
			return False

	def delete_all(self):
		self.__model.remove()
		return True

	def delete_like(self,oid,username):
		if not self.__model.find({"_id" : oid, "$in" : {"likes" : [username]}}):
			return False
		self.__model.update({"_id" : oid},{"$pull" : {"likes" : username} , "$inc" : {"totalLikes" : -1}})
		return True

	def delete_username(self,username):
		self.model.remove({"author" : username})
		return True

	def add_source(self,oid,source):
		self.__model.update({"_id" : oid}, {"$set" : {"source" : source}})

	def get_author(self,oid):
		fabex = self.__model.find_one({"_id" : oid})
		return fabex["author"] 

	def get_fabex_oid(self,oid):
		fabex=self.__model.find_one({"_id" : oid})
		return fabex
	
	def set_fabex(self,oid,field,value):
		self.__model.update({"_id" : oid},{"$set" : {field : value}})


	
	def oid_exists(self,oid):
		res=self.__model.find_one({"_id" : oid})
		return True if res else False



	def get_fabex_username(self,username):
		fabex=self,__model.find_one({"username" : username})
		return fabex

	def create_fabex(self,title,machine,fablab,author,properties,description,blog):
		try:
			identificador          = Counter("fabex_oid")
			siguiente              = identificador.get_next()
			identificador.update_next()
			fabber=Fabber()
			belt = fabber.get_fabber_belt(author)
			datas                  = {}
			datas["_id"]           = siguiente
			datas["title"]         = title
			datas["machine"]       = machine
			datas["fablab"]        = fablab
			datas["author"]        = author
			datas["properties"]    = properties
			datas["blog"]          = blog
			datas["likes"]         = []
			datas["totalLikes"]    = 0

			datas["belt"] = belt["belt"]
			if description:
				datas["description"]=description
			datas["created"]=datetime.now()
			self.__model.insert(datas)
			return siguiente
		except:
			return False		

	def addPhoto(self,_id,path,position,data):
		data     =data.replace("data:image/png;base64","")
		data     =data.replace(" ","+")
		data     =base64.b64decode(data)
		filename ="{}{}/{}.png".format(path,position,_id)
		f        = open(filename , 'w')
		f.write(data)
		f.close()
		url_file ="fabex_img/{}/{}.png".format(position,_id) 
		self.__model.update({"_id" : _id},{"$set" : {position : url_file }}) 


class Machine(Model):

	def __init__(self):
		super(Machine,self).__init__()
		self.__model=self.get_collection("machines")
	
	def name_exists(self,name):
		res=self.__model.find_one({"name" : name})
		return True if res else False
	
	def get_machines(self):
		machines=self.__model.find()
		return machines

	def set_machine(self,name,field,value):
		self.__model.update({"name" : name},{"$set" : {field : value}})


	def get_machine(self,name):
		machine=self.__model.find_one({"name" : name})
		return machine

	def delete(self,name):
		res=self.__model.remove({"name" : name})
		return True if res['n'] > 0 else False
	
	def delete_all(self):
		self.__model.remove()
		return True

	def create_machine(self,name,model,description,properties):
		try:
			identificador        =Counter("machine_oid")
			siguiente            =identificador.get_next()
			identificador.update_next()
			datas                ={}
			datas["_id"]         =siguiente
			datas["name"]        =name
			datas["model"]       =model
			datas["description"] =description
			datas["properties"]  =properties
			self.__model.insert(datas)
			return True
		except:
			return False

class Material(Model):

	def __init__(self):
		super(Material,self).__init__()
		self.__model=self.get_collection("materials")
	
	def get_materials(self):
		material=self.__model.find()
		return material

	def get_material(self,name):
		material=self.__model.find_one({"name" : name})
		return material

	def get_material_for_machine(self,machine):
		material=self.__model.find({"machine" : machine},{"machine" : 0})
		return material

	def set_material(self,name,field,value):
		self.__model.update({"name" : name},{"$set" : {field : value}})


	def name_exists(self,name):
		res=self.__model.find_one({"name" : name})
		return True if res else False

	def create_material(self,name,machine,thicknesses):
		try:
			identificador    =Counter("material_oid")
			siguiente        =identificador.get_next()
			identificador.update_next()
			datas            ={}
			datas["name"]    =name
			datas["machine"] =machine
			if thicknesses:
				datas["thicknesses"]=thicknesses
			self.__model.insert(datas)
			return True
		except:
			return False

	def delete(self,name):
		res=self.__model.remove({"name" : name})
		return True if res['n'] > 0 else False
	
	def delete_all(self):
		self.__model.remove()
		return True


class Comment(Model):
	def __init__(self):
		super(Comment,self).__init__()
		self.__model=self.get_collection("comments")
	
	def get_comments(self):
		comments=self.__model.find()
		return comments

	def get_comment_username(self,username):
		comments=self.__model.find({"username" : username})
		return comments

	def get_comment_fabex(self,fabex):
		comments=self.__model.find({"fabex" : fabex})
		return comments

	def get_author(self,oid):
		comment=self.__model.find_one({"_id" : oid})
		if comment:
			return comment["username"]
		else:
			return False

	def get_fabex_by_comment(self,oid):
		fabexoid = self.__model.find_one({"_id" : oid})["fabex"]
		return fabexoid if fabexoid else False

	def delete_fabex(self,fabex):
		self.__model.remove({"fabex" : fabex})
		return True

	def delete_username(self,username):
		self.__model.remove({"username" : username})
		return True

	def delete(self,oid):
		self.__model.remove({"_id" : oid})
		return True

	def delete_all(self):
		self.__model.remove()
		return True

	def create_comment(self,username,fabex,comment):
		identificador =Counter("comment_oid")
		siguiente     =identificador.get_next()
		identificador.update_next()
		datas             ={}
		datas["_id"]      =siguiente
		datas["username"] =username
		datas["fabex"]    =fabex
		datas["comment"]  =comment
		datas["date"]     =datetime.now()
		self.__model.insert(datas)
		return siguiente


class Counter(Model):

	##### CONSTRUCTOR #####
	def __init__(self,nombre):
		super(Counter,self).__init__()
		self.__model  =self.get_collection('counters')
		self.__nombre =nombre

	def get_next(self):
		last=self.__model.find_one({"_id" : self.__nombre})
		if not last:
			self.create_identifier(self.__nombre)
			return self.get_next()
		return last['last']

	def update_next(self):
		last=self.get_next()
		self.__model.update({"_id" : self.__nombre},{"$set" : {"last" : last+1 }})
	

	def create_identifier(self,name):
		self.__model.insert({"_id" : name, "last" : 1000})