# -*- coding: utf-8 -*-
import os
from flask import Flask,render_template,jsonify,request,abort,Response,url_for,redirect,make_response
from bson import *
from bson.json_util import dumps
from bson.json_util import loads
from pymongo import *
import urllib2
import urllib
import hashlib
import unittest
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename


#APP.
app=Flask(__name__, static_url_path='')
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
EXTENSIONS_MACHINESFILES = set(['cdr', 'ai', 'stl', 'dxf'])
SESSION_EXPIRE=15
MONGODB_URI = 'mongodb://luigonsec:aks1991@ds033059.mongolab.com:33059/fabx'
try: 
    client = MongoClient(MONGODB_URI)
except:
    noConnected()

database  = client['fabx']
sessions  = database['sessions']
fabexs    = database['fabexs']
fabbers   = database['fabbers']
materials = database['materials']
machines  = database['machines']
counters  = database['counters']
comments  = database['comments']


def noConnected():
    return "No ha sido posible conectarse"

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/index.html')
def index():
    return render_template("index.html")
@app.route('/blog')
def blog():
    if verify_cookies():
        user=getUser(request.cookies.get('username'))
        return render_template("blog.html",user=user)
    else:
        return render_template("index.html")

@app.route('/blog/<int:oid>')
def fabexview(oid):
    if verify_cookies():
        sep="../"
        user=getUser(request.cookies.get('username'))
        return render_template("fabexview.html",sep=sep,user=user)
    else:
        return render_template("index.html")

@app.route('/facebook')
def face():
    return render_template("facebook.html")

@app.route('/fabx')
def fabx():
    if verify_cookies():
        user=getUser(request.cookies.get('username'))
        return render_template("fabx.html",user=user)
    else:
        return render_template("index.html")
@app.route('/qrsearch')
def qrsearch():
    if verify_cookies():
        user=getUser(request.cookies.get('username'))
        return render_template("qrsearch.html",user=user)
    else:
        return render_template("index.html")

@app.route('/myprofile')
def my_profile():
    # VERFICIAR LOS LIKES ANTES
    if verify_cookies():
        user=getUser(request.cookies.get('username'))
        return render_template("myprofile.html",user=user)
    else:
        return render_template("index.html")


@app.route('/machines')
def machinesHTML():
    if verify_cookies():
        user=getUser(request.cookies.get('username'))
        if (user['admin']) :
            return render_template("machines.html",user=user)
        else:
            return render_template("error400.html")
    else:
        return render_template("index.html")

@app.route('/signup.html')
def signup():
    return render_template("signup.html")


@app.route('/api/help.html')
def apiHelp():
    return render_template("help.html")

@app.route('/login', methods=['POST'])
def login():
    error = None
    try:        
        json_data=request.json
        username=json_data["username"]
        password=json_data["password"]
        if valid_login(username,password):
            datas=fabbers.find_one({"username" : username})
            print datas
            resp=make_response(render_template("blog.html",user=datas))
            name=datas['name']
            surname=datas['surname']
            password=datas['password']
            secure_cookie=getCookie(password)
            expire_date=datetime.now()+timedelta(seconds=30)
            save_cookie(secure_cookie,expire_date)
            resp.set_cookie("username" , username)
            resp.set_cookie("name" , name)
            resp.set_cookie("surname", surname)
            resp.set_cookie("session" , secure_cookie)
            return resp
        else:
            res={"reason" : "Invalid username/password"}
            return Response(dumps(res), mimetype='application/json'),404
    except KeyError:
        res={"reason" : "Fields username and password required"}
        return Response(dumps(res), mimetype='application/json'),400

def isLogIn(username):
    sessionID=request.cookies.get('session')
    if username != request.cookies.get('username'):
        return False
    password=fabbers.find_one({"username" : username},{"password" : 1})
    password=password['password']
    if sessionID == None or sessionID != getCookie(password):
        return False
    session=sessions.find_one({"_id" : sessionID})
    if session == None:
        return False
    if session['expire']<datetime.now():
        sessions.remove({"_id" : sessionID})
        return False
    sessions.update({"_id" : sessionID}, {"$set": {"expire" : datetime.now()+timedelta(minutes=SESSION_EXPIRE)}})   
    return True    

def getUser(username):
    return fabbers.find_one({"username" : username},{"_id":0})


def verify_cookies():
    sessionID=request.cookies.get('session')
    username=request.cookies.get('username')
    password=fabbers.find_one({"username" : username},{"password" : 1})
    password=password['password']
    if sessionID == None:
        return False
    if sessionID != getCookie(password):
        return False
    session=sessions.find({"_id" : sessionID})
    if session.count() != 1:
        return False
    session=sessions.find_one({"_id" : sessionID})
    if session['expire']<datetime.now():
        sessions.remove({"_id" : sessionID})
        return False
    sessions.update({"_id" : sessionID}, {"$set": {"expire" : datetime.now()+timedelta(minutes=SESSION_EXPIRE)}})   
    return True

def save_cookie(secure_cookie,expire_date):
    sessions.remove({"_id" :  secure_cookie})
    sessions.insert({"_id" : secure_cookie, "expire" : expire_date}) 

def getCookie(password):
    cookie=password
    for _ in range(2):
        cookie=sha1(cookie)
        for _ in range(4):
            cookie=sha256(cookie)
            for _ in range(8):
                cookie=sha512(cookie)
    return cookie

def md5(string):
    m=hashlib.md5()
    m.update(string)
    return str(m.hexdigest())
def sha1(string):
    m=hashlib.sha1()
    m.update(string)
    return str(m.hexdigest())

def sha256(string):
    m=hashlib.sha256()
    m.update(string)
    return str(m.hexdigest()) 

def sha512(string):
    m=hashlib.sha512()
    m.update(string)
    return str(m.hexdigest())        

def valid_login(username,password):
    if fabbers.find({"username" : username, "password" : password}).count() == 0:
        return False
    else:
        return True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS        

def allowed_source(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in EXTENSIONS_MACHINESFILES


@app.route('/thingiverse')
def thingiverse():
    return redirect('https://www.thingiverse.com/login/oauth/authorize?client_id=74e2d010826bf069ae56&redirec_uri=http://fabexpertizer.herokuapp.com/thingiverse/token')

@app.route('/thingiverse/token')
def token():
    code=r.args['code']
    url="https://www.thingiverse.com/login/oauth/access_token"
    r=urllib2.urlopen(url,urllib.urlencode({'code':code, 'client_id':'74e2d010826bf069ae56','client_secret':'b171e7bd3820914f402f4db5845ac757'})).read()
    access_token=r.args['access_token']
    token_type=r.args['token_type']



#RECURSOS

#METODOS GET
@app.route('/api/v1/fabbers', methods=['GET'])
def get_all_fabbers():
    response=fabbers.find({},{"_id" : 0})
    elements=list(fabbers.find({},{"_id" : 0}))
    if(len(elements)==0):
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    a=dumps(response)
    return Response(a,  mimetype='application/json')

@app.route('/api/v1/fabbers/<username>', methods=['GET'])
def get_fabber(username):
    response=fabbers.find({"username" : username})
    if response.count() >1:
        res={"reason" : "There is a problem with this user"}
        return Response(dumps(res), mimetype='application/json'),409    
    if response.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    response=fabbers.find_one({"username" : username},{"_id":0})    
    a=dumps(response)
    return Response(a,  mimetype='application/json'),200

@app.route('/api/v1/fabbers/<author>/fabexs', methods=['GET'])
def get_fabber_fabexs(author):
    response=fabexs.find({"author" : author})
    elements=list(response)
    if(len(elements)==0):
        res={"reason" : "The user was not found"}
        return Response(dumps(res), mimetype='application/json'),404
    response=fabexs.find({"author" : author})    
    a=dumps(response)
    return Response(a, mimetype='application/json'),200    

#METODOS POST
@app.route('/api/v1/fabbers/<someinfo>', methods=['POST'])
def post_fabber_failed(someinfo):
    res={"added" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'),400

@app.route('/api/v1/fabbers', methods=['POST'])
def post_fabber():
    json_data=request.json
    if fabbers.find({"email" : json_data["email"]}).count() > 0:
        res={"added" : False , "reason" : "The email introduced is already registered"}
        return Response(dumps(res), mimetype='application/json'),409    
    if fabbers.find({"username" : json_data["username"]}).count() > 0:
        res={"added" : False , "reason" : "The username introduced is already in use"}
        return Response(dumps(res), mimetype='application/json'),409  
    last=counters.find_one({"_id" : "fabber_oid"})
    fabber_oid=last["last"]
    nuevo={}
    nuevo['_id']=fabber_oid+1
    nuevo['name']=json_data['name']
    nuevo['surname']=json_data['surname']
    nuevo['username']=json_data['username']
    nuevo['email']=json_data['email']
    nuevo['password']=json_data['password']
    fabbers.insert(nuevo)
    counters.update({"_id" : "fabber_oid"},{"$set" : {"last" : fabber_oid+1}})
    res={"added" : True}
    return Response(dumps(res), mimetype='application/json'),201
    

  #METODOS DELETE

@app.route('/api/v1/fabbers/<username>', methods=['DELETE'])
def delete_fabber(username):
    res=fabbers.remove({'username' : username})
    if(res['n']>0):
        res={"deleted" : True}
        return Response(dumps(res), mimetype='application/json'),200
    else:
        res={'deleted' : False, 'reason' : 'Username does not exist'}
        return Response(dumps(res), mimetype='application/json'), 404

@app.route('/api/v1/fabbers', methods=['DELETE'])
def delete_all_fabbers():
    fabbers.remove()
    res={"deleted" : True}
    return Response(dumps(res), mimetype='application/json'),200

   #METODOS PUT PATCH

@app.route('/api/v1/fabbers', methods=['PUT','PATCH'])
def update_fabbers_error():
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400

@app.route('/api/v1/fabbers/<username>', methods=['PUT','PATCH'])
def update_fabber(username):
    json_data=request.json
    user=list(fabbers.find({'username': username}))
    if len(user) == 0:
        res={"error" : "Not Found", "reason" : "The username especified has not been found in the database." }
        return Response(dumps(res), mimetype='application/json'),404
    
    modificado=0
    try:
        name=json_data['name']
        current_name=fabbers.find({'username' : username},{"name" : 1})
        if(current_name["name"] == name):
            pass
        else:
            fabbers.update({'username': username}, {"$set": {"name": name}})
            modificado+=1
    except KeyError:
        pass
    
    try:
        surname=json_data['surname']
        current_surname=fabbers.find({'username' : username},{"surname" : 1})
        if(current_surname["surname"] == surname):
            pass
        else:
            fabbers.update({'username': username}, {"$set": {"surname": surname}})
            modificado+=1
    except KeyError:
        pass

    try:
        password=json_data['password']
        current_password=fabbers.find({'username' : username},{"password" : 1})
        if(current_password["password"] == password):
            pass
        else:       
            fabbers.update({'username': username}, {"$set": {"password": password}})
            modificado+=1
    except KeyError:
        pass

    if(modificado==0):
        res={'updated' : False, 'reason' : 'Bad especified properties'}
        return Response(dumps(res), mimetype='application/json'),400    
    else:
        res={'updated' : True}
        return Response(dumps(res), mimetype='application/json'), 200


#        MATERIALES

@app.route('/api/v1/materials', methods=['POST'])
def post_materials():
    json_data=request.json
    try:
        name=json_data["name"]
    except KeyError:
        res=dumps({"added" : False, "reason" : "Material's name required"})
        return Response(res, mimetype='application/json'),400
    if materials.find({"name" : name}).count() > 0:
        res=dumps({"added" : False, "reason" : "Material's name introduced already exists"})
        return Response(res, mimetype='application/json'),409
    try:
        machine=json_data["machine"]
    except KeyError:
        res=dumps({"added" : False, "reason" : "Machine's name required"})
        return Response(res, mimetype='application/json'),400
    if machines.find({"name" : machine}).count() == 0:
        res=dumps({"added" : False, "reason" : "Machine not found"})
        return Response(res, mimetype='application/json'),404
    material={}
    try:
        thicknesses=json_data["thicknesses"]
        material['thicknesses']=thicknesses
    except:
        pass
    last=counters.find_one({"_id" : "material_oid"})
    material_oid=last["last"]
    res={"added" : True}
    material['_id']=material_oid+1    
    material['name']=name
    material['machine']=machine
    materials.insert(material)
    counters.update({"_id" : "material_oid"},{"$set" : {"last" : material_oid+1}})
    return Response(dumps({'added' : True}), mimetype='application/json'),201

@app.route('/api/v1/materials/<some>',methods=['POST'])
def post_materials_error(some):
    return Response(dumps({'added' : False, 'reason' : 'This request is not supported. For more information visit the API documetation', 'url' : 'http://fabexpertizer.herokuapp.com'}), mimetype='application/json'),400    

@app.route('/api/v1/materials', methods=['GET'])
def get_all_materials():
    response=materials.find()
    a=dumps(response)
    return Response(a,  mimetype='application/json')

@app.route('/api/v1/materials/<name>', methods=['GET'])
def get_material(name):
    response=materials.find({"name" : name})
    if response.count() > 1:
        res={"reason" : "There is a problem with this user"}
        return Response(dumps(res), mimetype='application/json'),409    
    if response.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    response=materials.find_one({"name" : name},{"_id" : 0})    
    res=dumps(response)
    return Response(res,  mimetype='application/json'),200    

@app.route('/api/v1/materials/machines/<name>', methods=['GET'])
def get_material_machine(name):
    response=materials.find({"name" : name})
    if response.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    res=dumps(response)
    return Response(res,  mimetype='application/json'),200 
  
@app.route('/api/v1/materials', methods=['PUT','PATCH'])
def update_materials_error():
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400

@app.route('/api/v1/materials/<current_name>', methods=['PUT','PATCH'])
def update_material(current_name):
    json_data=request.json
    if materials.find({'name' : current_name}).count() == 0:
        res={"error" : "Not Found", "reason" : "The name especified has not been found in the database." }
        return Response(dumps(res), mimetype='application/json'),404
    
    modificado=0
    try:
        name=json_data['name']
        materials.update({'name': current_name}, {"$set": {"name": name}})
        modificado+=1
    except KeyError:
        pass
    
    try:
        thicknesses=json_data['thicknesses']
        materials.update({'name': current_name}, {"$set": {"thicknesses": thicknesses}})
        modificado+=1
    except KeyError:
        passi

    if(modificado==0):
        res={'updated' : False, 'reason' : 'Bad especified properties'}
        return Response(dumps(res), mimetype='application/json'),400    
    else:
        res={'updated' : True}
        return Response(dumps(res), mimetype='application/json'), 200

@app.route('/api/v1/materials/<name>', methods=['DELETE'])
def delete_material(name):
    res=materials.remove({'name' : name})
    if(res['n']>0):
        res={"deleted" : True}
        return Response(dumps(res), mimetype='application/json'),200
    else:
        res={"deleted" : False, "reason" : "Material's name does not exist"}
        return Response(dumps(res), mimetype='application/json'), 404

@app.route('/api/v1/materials', methods=['DELETE'])
def delete_all_material():
    materials.remove()
    res={"deleted" : True}
    return Response(dumps(res), mimetype='application/json'),201


#MACHINES
@app.route("/api/v1/machines", methods=['GET'])
def get_machines():
    maquinas=machines.find()
    return Response(dumps(maquinas), mimetype='application/json'),200

@app.route("/api/v1/machines/<nombre>", methods=['GET'])
def get_machine(nombre):
    maquinas=machines.find({"name" : nombre})
    if maquinas.count() == 0:
        res=dumps({"reason" : "No elements were found."})
        return Response(res, mimetype='application/json'),404
    maquinas=machines.find_one({"name" : nombre})
    return Response(dumps(maquinas),mimetype='application/json'),200

@app.route("/api/v1/machines" , methods=['POST'])
def post_machine():
    try:
        json_data=request.json
        nombre=json_data['name']
        modelo=json_data['model']
        description=json_data['description']
        properties=json_data['properties']
    except:
        return Response(dumps({"created" : False,"reason" : "Some properties were not introduced."}), mimetype='application/json'),400
    last=counters.find_one({"_id" : "machine_oid"})
    machine_oid=last["last"]
    nuevo={}
    nuevo['_id']=machine_oid+1
    nuevo["name"]=nombre
    nuevo["model"]=modelo
    nuevo["properties"]=properties    
    nuevo["description"]=description
    machines.insert(nuevo)
    counters.update({"_id" : "machine_oid"},{"$set" : {"last" : machine_oid+1}})
    return Response(dumps({"created" : True}), mimetype='application/json'),201

@app.route("/api/v1/machines/<something>", methods=['POST'])
def post_fail(something):
    return Response(dumps({'added' : False, 'reason' : 'This request is not supported. For more information visit the API documetation', 'url' : 'http://fabexpertizer.herokuapp.com'}), mimetype='application/json'),400    

@app.route("/api/v1/machines" , methods=['DELETE'])
def delete_machines():
    machines.remove()
    return Response(dumps({'removed' : True}), mimetype='application/json'),200

@app.route("/api/v1/machines/<name>", methods=['DELETE'])
def delete_machine(name):
    if machines.find({"name" : name}).count() < 1:
        return Response(dumps({'updated' : False}), mimetype='application/json'),404
    if machines.find({"name" : name}).count() > 1:
        return Response(dumps({'updated' ,'no'}), mimetype='application/json'),409
    machine.remove({"name" : name})
    return Response(dumps({'removed' : True}), mimetype='application/json'),200


@app.route("/api/v1/machines", methods=['PUT','PATCH'])
def update_fail():
    return Response(dumps({'added' : False, 'reason' : 'This request is not supported. For more information visit the API documetation', 'url' : 'http://fabexpertizer.herokuapp.com'}), mimetype='application/json'),400    

@app.route("/api/v1/machines/<name>", methods=['PUT','PATCH'])
def update_machine(name):
    json_data=request.json
    try:
        name_in=1
        new_name=json_data["name"]
    except:
        name_in=0
    try:
        description_in=1
        description=json_data["description"]
    except:
        description_in=0

    matches=machines.find({"name" : name})
   
    if matches.count() > 1:
        return Response(dumps({'updated':'no'}), mimetype='application/json'),409
    if matches.count() < 1:
        return Response(dumps({'updated':'no','reason':'The machine indicated were not found.'}),mimetype='application/json'),404
    if name_in + description_in == 0:
        return Response(dumps({'updated' : False, 'reason' : 'Some properties were not introduced'}),mimetype='application/json'),400
    if name_in:
        machines.updated({"name" : name},{"$set" : {"name" : new_name}})
    if description_in:
        machines.updated({"name" : name},{"$set" : {"description" : description}})
    return Response(dumps({'updated' : True}),mimetype='application/json'),200


######################################################################
#########################   RESOURCE FABEX   #########################
######################################################################

@app.route('/api/v1/fabexs', methods=['GET'])
def get_fabexs():
    if len(request.args) > 0:
        q=request.args.get("q")
        keywords=q.split(",")
        documents=[]
        filters=[]
        for word in keywords:
            nameq={"name" : {"$regex" : word}}
            authorq={"author" : {"$regex" : word}}
            machineq={"machine" : {"$regex" : word}}
            titleq={"title" : {"$regex" : word}}
            filters.append(nameq)
            filters.append(authorq)
            filters.append(machineq)
            filters.append(titleq)
        res=fabexs.find({"$or" : filters})      
    else:
        res=fabexs.find().sort("created" , -1)
    if res.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    res=dumps(res)
    return Response(res,  mimetype='application/json'),200



@app.route('/api/v1/fabexs/<int:oid>', methods=['GET'])
def get_fabex_oid(oid):
    res=fabexs.find({"_id" : oid})
    if res.count() > 1:
        res={"reason" : "There is a problem with this fabex"}
        return Response(dumps(res), mimetype='application/json'),409    
    if res.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    res=fabexs.find_one({"_id" : oid})    
    a=dumps(res)
    return Response(a,  mimetype='application/json'),200



@app.route('/api/v1/fabexs/<string>', methods=['GET'])
def get_fabex_string(username):
    res={"reason" : "The last URL element must be an integer."}
    return Response(dumps(res), mimetype='application/json'),400

@app.route('/api/v1/fabexs/<someinfo>', methods=['POST'])
def post_fabex_failed(someinfo):
    res={"added" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'),400

@app.route('/api/v1/fabexs', methods=['POST'])
def post_fabex():
    json_data=request.json
    nuevo={}
    try:
        title=json_data['title']
        machine=json_data['machine']
        author=json_data['author']
        nuevo['title']=title
        nuevo['machine']=machine
        nuevo['author']=author

    except:
        res={"added" : False, "reason" : "Some main property was not indicated"}
        return Response(dumps(res),mimetype='application/json'),400
    try:
        description=json_data['description']
        nuevo['description']=description
    except:
        pass
    try:
        blog=json_data['blog']
        nuevo['blog']=blog
    except:
        nuevo['blog']=False
    machine=machines.find({"name" : machine})
    if machine.count() == 0:
        res={"added" : False , "reason" : "Machine not found"}
        return Response(dumps(res), mimetype="application/json"),404
    if machine.count() > 1:
        res={"added" : False , "reason" : "Some wrong happens with the indicated machine"}
        return Response(dumps(res), mimetype="application/json"),409
    try:
        list_properties=json_data['properties']
        nuevo['properties']=list_properties
    except:
        res={"added" : False, "reason" : "Some main property was not indicated"}
        return Response(dumps(res),mimetype='application/json'),400

    try:
        left=json_data['left']
        nuevo['left']=left
    except:
        pass
    
    try:
        top=json_data['top']
        nuevo['top']=top
    except:
        pass
    
    try:
        front=json_data['front']
        nuevo['front']=front
    except:
        pass
    last=counters.find_one({"_id" : "fabex_oid"})
    fabex_oid=last["last"]
    nuevo['_id']=int(fabex_oid)+1
    nuevo['created']=datetime.now()
    fabexs.insert(nuevo)
    counters.update({"_id" : "fabex_oid"},{"$set" : {"last" : fabex_oid+1}})
    res=fabexs.find_one({"_id" : fabex_oid+1})
    return Response(dumps(res), mimetype='application/json'),201
    



@app.route('/api/v1/fabexs/<int:oid>', methods=['DELETE'])
def delete_fabex(oid):
    res=fabexs.remove({'_id' : oid})
    if(res['n']>0):
        res={"deleted" : True}
        return Response(dumps(res), mimetype='application/json'),200
    else:
        res={'deleted' : False, 'reason' : 'Username does not exist'}
        return Response(dumps(res), mimetype='application/json'), 404



@app.route('/api/v1/fabexs/<string>', methods=['DELETE'])
def delete_fabex_error(string):
    abort(404)

@app.route('/api/v1/fabexs', methods=['DELETE'])
def delete_all_fabexs():
    fabexs.remove()
    res={"removed" : True}
    return Response(dumps(res), mimetype='application/json'),201


@app.route('/api/v1/fabexs', methods=['PUT','PATCH'])
def update_fabexs_error():
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400



@app.route('/api/v1/fabexs/<int:oid>', methods=['PUT','PATCH'])
def update_fabex(oid):
    json_data=request.json
    user=list(fabexs.find({'_id': oid}))
    if len(user) == 0:
        res={"error" : "Not Found", "reason" : "The oid especified has not been found in the database." }
        return Response(dumps(res), mimetype='application/json'),404
    
    modificado=0
    try:
        title=json_data['title']
        fabexs.update({'_id': oid}, {"$set": {"title": title}})
        modificado+=1
    except KeyError:
        pass
    
    try:
        description=json_data['description']
        fabexs.update({'_id': oid}, {"$set": {"description": description}})
        modificado+=1
    except KeyError:
        pass

    if(modificado==0):
        res={'updated' : False, 'reason' : 'Bad especified properties'}
        return Response(dumps(res), mimetype='application/json'),400    
    else:
        res={'updated' : True}
        return Response(dumps(res), mimetype='application/json'), 200
    

@app.route('/api/v1/fabexs/like/<username>/<int:oid>', methods=['PUT','PATCH'])
def add_like(username,oid):
    if not isLogIn(username):
        return Response(dumps({"updated" : False}), mimetype='application/json'),401
    fabber=fabbers.find_one({"username" : username})
    fabex=fabexs.find_one({"_id" : oid})
    if fabber == None or fabex == None:
        return Response(dumps({"reason" : "Not found"}) , mimetype='application/json'),404
    fabbers.update({"username" : username},{"$push" : {"likes" : oid}})
    fabexs.update({"_id" : oid},{"$push" : {"likes" : username}})
    return Response(dumps({"updated" : True}), mimetype='application/json'),200

@app.route('/api/v1/fabexs/dislike/<username>/<int:oid>', methods=['PUT','PATCH'])
def remove_like(username,oid):
    if not isLogIn(username):
        return Response(dumps({"updated" : False}), mimetype='application/json'),401
    fabber=fabbers.find_one({"username" : username})
    fabex=fabexs.find_one({"_id" : oid})
    if fabber == None or fabex == None:
        return Response(dumps({"reason" : "Not found"}) , mimetype='application/json'),404
    fabbers.update({"username" : username},{"$pull" : {"likes" : oid}})
    fabexs.update({"_id" : oid},{"$pull" : {"likes" : username}})
    return Response(dumps({"updated" : True}), mimetype='application/json'),200

#####################################################################
######################### RESOURCE COMMENTS #########################
#####################################################################

@app.route('/api/v1/comments/<username>/<int:oid>',methods=['POST'])
def add_comment(username,oid):
    if not isLogIn(username):
        return Response(dumps({"created" : False, "reason" : "Not logged in"}), mimetype='application/json'),401
    fabber=fabbers.find_one({"username" : username})
    fabex=fabexs.find_one({"_id" : oid})
    if not fabber or not fabex:
        return Response(dumps({"created" : False, "reason" : "Fabber o Fabex not found"}) , mimetype='application/json'),404
    now=datetime.now()
    json_data=request.json
    try:
        comment=json_data['comment']
    except:
        res={'created' : False, 'reason' : 'Bad especified properties'}
        return Response(dumps(res), mimetype='application/json'),400

    last=counters.find_one({"_id" : "comments_oid"})['last']
    counters.update({"_id" : "comments_oid"},{"$set" : {"last" : last + 1}})
    comments.insert({"_id" : last, "username" : username, "fabex" : oid, "date" : now, "comment" : comment })
    return Response(dumps({"created" : True}), mimetype='application/json'),201  

@app.route('/api/v1/comments/<username>', methods=['GET'])
def get_comment_by_user(username):
    comment_list=comments.find({"username" : username})
    return Response(dumps(comment_list) , mimetype="application/json"),200

@app.route('/api/v1/comments/<int:oid>', methods=['GET'])
def get_comment_by_fabex(oid):
    comment_list=comments.find({"fabex" : oid})
    return Response(dumps(comment_list) , mimetype="application/json"),200

@app.route('/api/v1/comments', methods=['GET'])
def get_comments():
    comment_list=comments.find()
    return Response(dumps(comment_list) , mimetype="application/json"),200
#####################################################################
######################### RESOURCE SOURCE #########################
#####################################################################

'''
@app.route('/api/v1/images/<int:oid>/front', methods=['PUT','PATCH'])
def upload_file_front(oid):
    try:
        if request.method == 'PUT' or request.method == 'PATCH':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = str(oid)+".jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+"fabex_img/front", filename))
                url_file="fabex_img/front/"+filename
                fabexs.update({"_id" : oid}, {"$set" : {"front" : url_file}})
                return Response(dumps({"created" : True}), mimetype="application/json"),201
            else:
                return Response(dumps({"created" : False}), mimetype="application/json"),400
    except Exception as e:
        return str(e)
@app.route('/api/v1/images/<int:oid>/left', methods=['PUT','PATCH'])
def upload_file_left(oid):
    try:
        if request.method == 'PUT' or request.method == 'PATCH':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = str(oid)+".jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+"fabex_img/left/", filename))
                url_file="fabex_img/left/"+filename
                fabexs.update({"_id" : oid}, {"$set" : {"left" : url_file}})
                return Response(dumps({"created" : True}), mimetype="application/json"),201
            else:
                return Response(dumps({"created" : False}), mimetype="application/json"),400
    except Exception as e:
        return str(e)

@app.route('/api/v1/images/<int:oid>/top', methods=['PUT','PATCH'])
def upload_file_top(oid):
    try:
        if request.method == 'PUT' or request.method == 'PATCH':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = str(oid)+".jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+"fabex_img/top/", filename))
                url_file="fabex_img/top/"+filename
                fabexs.update({"_id" : oid}, {"$set" : {"top" : url_file}})
                return Response(dumps({"created" : True}), mimetype="application/json"),201
            else:
                return Response(dumps({"created" : False}), mimetype="application/json"),400
    except Exception as e:
        return str(e)
'''
@app.route('/api/v1/source/<int:oid>', methods=['PUT','PATCH'])
def upload_file_source(oid):
    cont=0
    try:
        if request.method == 'PUT' or request.method == 'PATCH':
            file = request.files['file']
            if file:
                parts=file.filename.split(".")
                ext=parts[-1]
                name=fabexs.find_one({"_id" : oid})
                title=str(name['title'])
                titleCamel=''.join(x for x in title.title() if not x.isspace())
                filename="{}-{}.{}".format(titleCamel,oid,ext)
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+"sources/", filename))
                url_file="sources/"+filename
                fabexs.update({"_id" : oid}, {"$set" : {"source" : url_file}})
                return Response(dumps({"created" : True}), mimetype="application/json"),201
            else:
                return Response(dumps({"created" : False}), mimetype="application/json"),400
    except Exception as e:
        return "Ha petado: "+str(filename)


class ApiTest(unittest.TestCase):
    def test_good_login(self):
        self.assertEqual(True, valid_login("luigonsec","password"))
    def test_bad_login(self):
        self.assertEqual(False,valid_login("noexiste","noexiste"))
    def test_verify_cookies(self):
        self.assertEqual(True,verify_cookies());
if __name__ == '__main__':
    unittest.main()    
