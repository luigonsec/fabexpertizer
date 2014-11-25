# -*- coding: utf-8 -*-
import os
from flask import Flask,render_template,jsonify,request,abort,Response,url_for,redirect,session,make_response
from bson import *
from bson.json_util import dumps
from bson.json_util import loads
from pymongo import *
import urllib2
import urllib
import unittest
from datetime import datetime, timedelta
from models import *



#APP.
app                         =Flask(__name__, static_url_path='')
UPLOAD_FOLDER               = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug                   = True
ALLOWED_EXTENSIONS          = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
EXTENSIONS_MACHINESFILES    = set(['cdr', 'ai', 'stl', 'dxf'])
app.secret_key = '\x9e\xbb\xa8\xc1\xa29y\x91\xe7\x1c\x17\xa3tX\x93\xfe\x82\xdc\xd3]\xcf\xd1\xbc\xf5'


@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/index.html')
def index():
    return render_template("index.html")
@app.route('/blog')
def blog():
    if session["logged"]:
        user = get_username(session["username"])
        return render_template("blog.html",user=user,login=True)
    else:
        return redirect("/")

@app.route('/blog/<int:oid>')
def fabexview(oid):

    if session["logged"]:
        sep  ="../"
        user =get_username(session["username"])
        return render_template("fabexview.html",sep=sep,user=user,login=True)

    else:
        return redirect("/")

@app.route('/facebook')
def face():
    return render_template("facebook.html")

@app.route('/fabx')
def fabx():
    if session["logged"]:
        user = get_username(session["username"])
        return render_template("fabx.html",user=user,login=True)
    else:
        return redirect("/")
@app.route('/qrsearch')
def qrsearch():
    if session["logged"]:
        user = get_username(session["username"])
        return render_template("qrsearch.html",user=user,login=True)
    else:
        return redirect("/")

@app.route('/fablabs')
def fablabs():
    if session["logged"]:
        user = get_username(session['username'])
        return render_template("fablabs.html",user=user,login=True)
    else:
        return redirect("/")

@app.route('/myprofile')
def my_profile():
    if session["logged"]:
        user = get_username(session['username'])
        return render_template("myprofile.html",user=user,login=True)
    else:
        return redirect("/")


@app.route('/machines')
def machinesHTML():
    fabber=Fabber()
    if session["logged"]:
        if fabber.is_admin(session["username"]):
            user=get_username(session['username'])
            return render_template("machines.html",user=user,login=True)
        else:
            return render_template("error400.html")
    else:
        return redirect("/")

@app.route('/adminfablab')
def admin_fablab():
    if session["logged"]:
        fabber=Fabber()
        if (fabber.is_admin(session["username"])):
            user=get_username(session['username'])
            fablab=Fablab()
            f = fablab.get_fablab_by_admin(user['username'])
            return render_template("adminfablab.html",user=user,login=True,fablab=f)

        else:
            return render_template("error400.html")

    else:
        return redirect("/")   
@app.route('/managefabbers')
def manage_fabbers():
    if session["logged"]:
        fabber=Fabber()
        if (fabber.is_admin(session["username"])) :
            user=get_username(session["username"])
            return render_template("managefabber.html",user=user,login=True)
        else:
            return render_template("error400.html")
    else:
        return redirect("/")

@app.route('/managefablabs')
def manage_fablabs():
    if session["logged"]:
        fabber=Fabber()
        if (fabber.is_superuser(session["username"])) :
            user=get_username(session["username"])
            return render_template("managefablabs.html",user=user,login=True)
        else:
            return render_template("error400.html")
    else:
        return redirect("/")

@app.route('/fabbers')
def fabbers():
    if session["logged"]:
        user=get_username(session["username"])
        return render_template("fabbers.html",user=user,login=True)
    else:
        return redirect("/")

@app.route('/fabbers/<fabber>')
def visit_profile(fabber):
    if session["logged"] and session["username"] == fabber:
        return redirect("/myprofile")
    else:
        if session["logged"]:
            user=get_username(session["username"])
            return render_template("profile.html",user=user,sep="../",login=True)
        else:
            return redirect("/")     


@app.route('/signup.html')
def signup():
    return render_template("signup.html")


@app.route('/api/help.html')
def apiHelp():
    return render_template("help.html")

@app.route('/login', methods=['POST'])
def login():
    fabber=Fabber()
    try:        
        json     =request.json
        username =json["username"]
        password =json["password"]
        if fabber.valid_login(username,password):
            datas         =fabber.get_fabber(username)
            resp          =make_response(render_template("blog.html",user=datas))
            session["logged"] = True
            session["username"] = username
            session["admin"] = fabber.is_admin(username);
            session["superuser"] = fabber.is_superuser(username)
            return resp
        else:
            res={"reason" : "Invalid username/password"}
            return Response(dumps(res), mimetype='application/json'),404
    except KeyError:
        res={"reason" : "Fields username and password required"}
        return Response(dumps(res), mimetype='application/json'),400

@app.route("/api/v1/session/<param>",methods=["GET"])
def get_data_session(param):
    if session["logged"]:
        return Response(dumps({"param" : session[param]}),mimetype="application/json"),200
    else:
        return Response(dumps({"param" : None }),mimetype="application/json"),200


def get_username(username):
    fabber=Fabber();
    return fabber.get_fabber(username)

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

##########################################################
#################### RESOURCE FABLAB #####################
##########################################################

@app.route("/api/v1/fabbers/<username>/fablabs" , methods=["GET"])
def get_fabber_fablabs(username):
    fabber=Fabber()
    fab=Fablab()
    if session["logged"]:
        if not fabber.exists_username(username):
            return Response(dumps({"ok" : False}), mimetype="application/json"),404
        fablabs=fabber.get_fablabs(username)
        return Response(dumps(fablabs),mimetype="application/json"),200
    else:
        return Response(dumps({"ok":False}),mimetype="application/json"),403


@app.route("/api/v1/fabbers/<username>/requests/<fablab>" , methods=["PUT","PATCH"])
def join_fablab(username,fablab):
    fabber=Fabber()
    fab=Fablab()
    if session["logged"] and session["username"] == username:
        if not fabber.exists_username(username) or not fab.exists_fablab(fablab):
            return Response(dumps({"created" : False}), mimetype="application/json"),404
        fabber.add_request(username,fablab)
        fab.add_request(fablab,username)
        return Response(dumps({"created":True}),mimetype="application/json"),201
    else:
        return Response(dumps({"created":False}),mimetype="application/json"),403

@app.route("/api/v1/fabbers/<username>/requests/<fablab>", methods=["DELETE"])
def cancel_request(username,fablab):
    fabber=Fabber()
    fab=Fablab()
    if session["logged"] and session["username"] == username:
        if not fabber.exists_username(username) or not fab.exists_fablab(fablab):
            return Response( dumps({"deleted": False}), mimetype="application/json"),404
        if not fabber.exists_request(username,fablab) or not fab.exists_request(fablab,username):
            return Response( dumps({"deleted": False}), mimetype="application/json"),404
        fabber.delete_request(username,fablab)
        fab.delete_request(fablab,username)
        return Response(dumps({"deleted" : True}), mimetype="application/json"),200
    else:
        return Response(dumps({"created":False}),mimetype="application/json"),403
@app.route("/api/v1/fabbers/<username>/leave/<fablabname>",methods=["PUT"])
def leave_fablab(username,fablabname):
    fablab = Fablab()
    if session["logged"] and session["username"] == username:
        if fablab.has_member(fablabname,username):
            fablab.delete_member(fablabname,username)
            fabber.add_points(username,-50)
            fablab.add_points(fablabname,-25)
            return Response(dumps({"ok" : True}),mimetype="application/json"),200
        return Response(dumps({"reason" : "Not member"}),mimetype="application/json"),404
    return Response(dumps({"reason" : "Not login"}),mimetype="application/json"),403

@app.route("/api/v1/fablabs" , methods=['GET'])
def get_fablabs():
    fablabs=Fablab().get_fablabs()
    return Response(dumps(fablabs),mimetype="application/json"),200

@app.route("/api/v1/fablabs/<fablab>", methods=["GET"])
def get_fablab(fablab):
    fab=Fablab().get_fablab(fablab)
    if fab:
        return Response(dumps(fab), mimetype="application/json"),200
    else:
        return Response(mimetype="application/json"),404


@app.route("/api/v1/fablabs/<admin>/members", methods=["GET"])
def get_fablab_members(admin):

    fablab=Fablab()
    fab = fablab.get_fablab_by_admin(admin)
    fab = fablab.get_fablab(fab["fablab"])["members"]
    if fab:
        return Response(dumps(fab), mimetype="application/json"),200
    else:
        return Response(mimetype="application/json"),404

@app.route("/api/v1/fablab/accept/<fabbername>" , methods=["PUT"])
def accept_fablab(fabbername):
    fabber = Fabber()
    fablab = Fablab()
    if session["logged"] and fabber.is_admin(session["username"]):
        fablabname = fablab.get_fablab_by_admin(session["username"])["fablab"]
        if not fablabname:
            return Response(dumps({"reason" : "Not admin"}),mimetype="application/json"),403
        else:
            if fablab.delete_request(fablabname,fabbername):
                if fablab.add_member(fablabname,fabbername):
                    fabber.add_points(fabbername,50)
                    fablab.add_points(fablabname,25)
                    return Response(dumps({"ok" : True }),mimetype="application/json"),200
    else:
        return Response(dumps({"reason" : "Not admin"}),mimetype="application/json"),403

@app.route("/api/v1/fablab/cancel/<fabbername>" , methods=["PUT"])
def cancel_request2(fabbername):
    fabber = Fabber()
    fablab = Fablab()
    if session["logged"] and fabber.is_admin(session["username"]):
        fablabname = fablab.get_fablab_by_admin(session["username"])["fablab"]
        if not fablabname:
            return Response(dumps({"reason" : "Not admin"}),mimetype="application/json"),403
        else:
            fablab.delete_request(fablabname,fabbername)
            return Response(dumps({"ok" : True }),mimetype="application/json"),200
    else:
        return Response(dumps({"reason" : "Not admin"}),mimetype="application/json"),403


@app.route("/api/v1/fablabs" , methods=["POST"])
def post_fablab():
    json=request.json
    error=0
    fab=Fablab()
    fabber=Fabber()
    if session["logged"] and fabber.is_superuser(session["username"]):
        try:
            name=json["name"]
        except:
            error+=1
        exists=False
        try:
            fablab=json["fablab"]
            if fab.exists_fablab(fablab):
                exists=True
        except:
            error+=1
        
        try:
            address=json["address"]
        except:
            address=None
        
        try:
            description=json["description"]
        except:
            description=None
        
        try:
            phone=json["phone"]
        except:
            phone=None
        
        try:
            email=json["email"]
        except:
            error+=1

        if error:
            return Response(dumps({"created" : False}) , mimetype="application/json"),400

        if exists:
            return Response(dumps({"created": False}), mimetype="application/json"),409

        res = Fablab().add_fablab(name,fablab,address,description,phone,email)
        if res:
            return Response(dumps({"created" : True }), mimetype="application/json"),201
        else:
            return Response(dumps({"created" : False}),mimetype="application/json"),400
    else:
        return Response(dumps({"created" : False}),mimetype="application/json"),403
##########################################################
#################### RESOURCE FABBERS ####################
##########################################################
    
    # name
    # surname
    # username
    # email
    # password
    # date
 

@app.route('/api/v1/fabbers', methods=['GET'])
def get_all_fabbers():
    if request.args.get("sort"):
        sort=request.args.get("sort")
        if request.args.get("order"):
            order = -1 if request.args.get("order") == "DESC" else 1
        else:
            order = 1
    else:
        sort  = "username"
        order = ASCENDING
    response=Fabber().get_fabbers(sort,order);
    if(response.count() == 0):
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    

    return Response(dumps(response),  mimetype='application/json')

@app.route('/api/v1/fabbers/<username>', methods=['GET'])
def get_fabber(username):
    response=Fabber().get_fabber(username);
    if not response:
        res={"reason" : username}
        return Response(dumps(res), mimetype='application/json'),404
    return Response(dumps(response),  mimetype='application/json'),200

@app.route('/api/v1/fabbers/<author>/fabexs', methods=['GET'])
def get_fabber_fabexs(author):
    response=Fabex().get_fabex_author(author)
    if(response.count() == 0):
        res={"reason" : "The user was not found"}
        return Response(dumps(res), mimetype='application/json'),404
    return Response(dumps(response), mimetype='application/json'),200    

#METODOS POST
@app.route('/api/v1/fabbers/<someinfo>', methods=['POST'])
def post_fabber_failed(someinfo):
    res={"added" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'),400

@app.route('/api/v1/fabbers', methods=['POST'])
def post_fabber():
    fabber =Fabber()
    try:
        json     =request.json
        name     =json['name'].title()
        surname  =json['surname'].title()
        username =json['username'].lower()
        email    =json['email'].lower()
        password =json['password']
    except:
        res={"created" : False}
        return Response(dumps(res), mimetype='application/json'),400
    
    if fabber.exists_email(json['email']):
        res={"added" : False , "reason" : "The email introduced is already registered"}
        return Response(dumps(res), mimetype='application/json'),409    
    
    if fabber.exists_username(json['username']):
        res={"added" : False , "reason" : "The username introduced is already in use"}
        return Response(dumps(res), mimetype='application/json'),409  

    fabber.create_fabber(name,surname,username,email,password)
    res={"added" : True}
    return Response(dumps(res), mimetype='application/json'),201
    

@app.route('/api/v1/fabbers/<username>', methods=['DELETE'])
def delete_fabber(username):
    fabber=Fabber()
    if session["logged"] and (session["username"] == username or fabber.is_superuser(session["username"])):
        if fabber.delete(username):
            res={"deleted" : True}
            return Response(dumps(res), mimetype='application/json'),200
        else:
            res={'deleted' : False, 'reason' : 'Username does not exist'}
            return Response(dumps(res), mimetype='application/json'), 404
    else:
        res={"deleted" : False}
        return Response(dumps(res), mimetype='application/json'),403

@app.route('/api/v1/fabbers', methods=['DELETE'])
def delete_all_fabbers():
    fabber=Fabber()
    if session["logged"] and fabber.is_superuser(session["username"]):
        fabber.delete_all()
        res={"deleted" : True}
        return Response(dumps(res), mimetype='application/json'),200
    else:
        res = {"deleted" : False}
        return Response(dumps(res),mimetype="application/json"),403

   #METODOS PUT PATCH
@app.route('/api/v1/fabbers/<username>/grant/<fablabname>' , methods=['PUT','PATCH'])
def grant_privileges(username,fablabname):
    fabber=Fabber()
    if session["logged"] and fabber.is_superuser(session["username"]):
        if fabber.is_admin(username):
            return Response(dumps({"reason" : "User {0} is already admin".format(username)}), mimetype="application/json"),400
        fablab=Fablab()
        if fabber.exists_username(username) and fablab.exists_fablab(fablabname):
            granted = fablab.add_admin(fablabname,username)
            if not granted:
                return Response(dumps({"reason" : "User {0} is already admin".format(username)}), mimetype="application/json"),400
            else:
                added = fabber.admin_fablab(username,fablabname)
                if not added:
                    return Response(dumps({"reason" : "Can't be added"}),mimetype="application/json"),400
            fabber.add_points(username,25000)
            return Response({dumps({"granted" :  True})},mimetype="application/json"),200

        else:
            res={"error" : "Not Found", "reason" : "The username or the fablab especified has not been found in the database." }
            return Response(dumps(res), mimetype='application/json'),404 
    else:
        res={"granted" : False}
        return Response(dumps(res), mimetype='application/json'),403    

@app.route('/api/v1/fabbers', methods=['PUT','PATCH'])
def update_fabbers_error():
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400

@app.route('/api/v1/fabbers/<username>', methods=['PUT','PATCH'])
def update_fabber(username):
    json   =request.json
    fabber =Fabber()
    sender=session["username"]
    if session["logged"] and (fabber.is_superuser(session["username"]) or session["username"] == username):
        if not fabber.exists_username(username):
            res={"error" : "Not Found", "reason" : "The username especified has not been found in the database." }
            return Response(dumps(res), mimetype='application/json'),404
        
        modifications=0
        try:
            password=json['password']
            if fabber.valid_login(username,password) or fabber.is_superuser(sender) :
                try:
                    new_password  =json['new_password']
                    fabber.set_fabber(username,"password",new_password)
                    modifications +=1
                except:
                    pass
            else:
                return Response(dumps({"updated" : False, "reason" : "Invalid password"}), mimetype="application/json"),400
        except KeyError:
            pass

        try:
            name          =json['name'].title()
            fabber.set_fabber(username,"name",name)
            modifications +=1
        except KeyError:
            pass
        
        try:
            surname       =json['surname'].title()
            fabber.set_fabber(username,"surname",surname)
            modifications +=1
        except KeyError:
            pass

        if not modifications:
            res={'updated' : False, 'reason' : 'Bad especified properties'}
            return Response(dumps(res), mimetype='application/json'),400    
        else:
            res={'updated' : True}
            return Response(dumps(res), mimetype='application/json'), 200
    else:
        res={"updated" : False}
        return Response(dumps(res), mimetype='application/json'), 403

@app.route("/api/v1/fabbers/<username>/belt",methods=["GET"])
def get_fabber_belt(username):
    fabber=Fabber()
    if fabber.exists_username(username):
        belt = fabber.get_fabber_belt(username);
        return Response(dumps(belt),mimetype="application/json"),200
    else:
        return Response(dumps({"reason" : "Not found"}),mimetype="application/json"),404
@app.route("/api/v1/fabber/<username>/follow/<followed>" , methods=['PUT','PATCH'])
def add_follow(username,followed):
    fabber=Fabber()
    if session["logged"] and session["username"] == username:    
        success=fabber.add_follow(username,followed);
        if not success:
            return Response(dumps({"updated" : False, "reason" : "Not Found"}), mimetype="application/json"),404
        fabber.add_points(followed,30)
        fabber.add_points(username,10)
        return Response(dumps({"updated" : True}), mimetype="application/json"),200
    else:
        return Response(dumps({"updated" : False}), mimetype="application/json"),403

@app.route("/api/v1/fabber/<username>/unfollow/<unfollowed>" , methods=['PUT','PATCH'])
def add_unfollow(username,unfollowed):
    fabber=Fabber()
    if session["logged"] and session["username"] == username:     
        success=fabber().add_unfollow(username,unfollowed);    
        if not success:
            return Response(dumps({"updated" : False, "reason" : "Not Found"}), mimetype="application/json"),404
        fabber.add_points(unfollwed,-30)
        fabber.add_points(username,-10)
        return Response(dumps({"updated" : True}), mimetype="application/json"),200
    else:
        return Response(dumps({"updated" : False}), mimetype="application/json"),403

##########################################################
################## RESOURCE MATERIALS ####################
##########################################################
    
    # name
    # thicknesses
    # machine

@app.route('/api/v1/materials', methods=['POST'])
def post_materials():
    json     =request.json
    material =Material()
    machine  =Machine()

    try:
        name=json["name"]
    except KeyError:
        res=dumps({"added" : False, "reason" : "Material's name required"})
        return Response(res, mimetype='application/json'),400
    if material.name_exists(name):
        res=dumps({"added" : False, "reason" : "Material's name introduced already exists"})
        return Response(res, mimetype='application/json'),409
    try:
        machine_name=json["machine"]
    except KeyError:
        res=dumps({"added" : False, "reason" : "Machine's name required"})
        return Response(res, mimetype='application/json'),400
    if not machine.name_exists(machine_name):
        res=dumps({"added" : False, "reason" : "Machine not found"})
        return Response(res, mimetype='application/json'),404
    try:
        thicknesses=json["thicknesses"]
    except:
        thicknesses=None
    material.create_material(name,machine_name,thicknesses)
    return Response(dumps({'added' : True}), mimetype='application/json'),201

@app.route('/api/v1/materials/<some>',methods=['POST'])
def post_materials_error(some):
    return Response(dumps({'added' : False, 'reason' : 'This request is not supported. For more information visit the API documetation', 'url' : 'http://fabexpertizer.herokuapp.com'}), mimetype='application/json'),400    

@app.route('/api/v1/materials', methods=['GET'])
def get_all_materials():
    material =Material()
    response =material.get_materials()
    a=dumps(response)
    return Response(a,  mimetype='application/json'),200

@app.route('/api/v1/materials/<name>', methods=['GET'])
def get_material(name):
    material=Material().get_material(name)
    if not material:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    return Response(dumps(material),  mimetype='application/json'),200    

@app.route('/api/v1/materials/machines/<name>', methods=['GET'])
def get_material_machine(name):
    material=Material().get_material_for_machine(name)
    if material.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    return Response(dumps(material),  mimetype='application/json'),200 
  
@app.route('/api/v1/materials', methods=['PUT','PATCH'])
def update_materials_error():
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400

@app.route('/api/v1/materials/<current_name>', methods=['PUT','PATCH'])
def update_material(current_name):
    json=request.json
    material=Material()
    if not material.name_exists(current_name):
        res={"error" : "Not Found", "reason" : "The name especified has not been found in the database." }
        return Response(dumps(res), mimetype='application/json'),404
    
    modifications=0
    try:
        name=json['name']
        material.set_material(current_name,"name",name)
        modifications+=1
    except KeyError:
        pass
    
    try:
        thicknesses=json['thicknesses']
        material.set_material(current_name,"thicknesses",thicknesses)
        modifications+=1
    except KeyError:
        pass

    if not modifications:
        res={'updated' : False, 'reason' : 'Bad especified properties'}
        return Response(dumps(res), mimetype='application/json'),400    
    else:
        res={'updated' : True}
        return Response(dumps(res), mimetype='application/json'), 200

@app.route('/api/v1/materials/<name>', methods=['DELETE'])
def delete_material(name):
    material=Material()
    
    if material.delete(name):
        res={"deleted" : True}
        return Response(dumps(res), mimetype='application/json'),200
    else:
        res={"deleted" : False, "reason" : "Material's name does not exist"}
        return Response(dumps(res), mimetype='application/json'), 404

@app.route('/api/v1/materials', methods=['DELETE'])
def delete_all_material():
    material=Material()
    material.delete_all()
    res={"deleted" : True}
    return Response(dumps(res), mimetype='application/json'),201


##########################################################
################## RESOURCE MACHINES #####################
##########################################################
    
    # name
    # properties
    # model
    # description



@app.route("/api/v1/machines", methods=['GET'])
def get_machines():
    machine=Machine().get_machines()
    return Response(dumps(machine), mimetype='application/json'),200

@app.route("/api/v1/machines/<name>", methods=['GET'])
def get_machine(name):
    machine=Machine().get_machine(name)
    if not machine:
        res=dumps({"reason" : "No elements were found."})
        return Response(res, mimetype='application/json'),404
    return Response(dumps(machine),mimetype='application/json'),200

@app.route("/api/v1/machines" , methods=['POST'])
def post_machine():
    machine=Machine()
    try:
        json        =request.json
        name        =json['name']
        model       =json['model']
        description =json['description']
        properties  =json['properties']
    except:
        return Response(dumps({"created" : False,"reason" : "Some properties were not introduced."}), mimetype='application/json'),400
    if machine.name_exists(name):
        res=dumps({"added" : False, "reason" : "Material's name introduced already exists"})
        return Response(res, mimetype='application/json'),409


    machine.create_machine(name,model,description,properties)
    return Response(dumps({"created" : True}), mimetype='application/json'),201

@app.route("/api/v1/machines/<something>", methods=['POST'])
def bad_post_machine(something):
    return Response(dumps({'added' : False, 'reason' : 'This request is not supported. For more information visit the API documetation', 'url' : 'http://fabexpertizer.herokuapp.com'}), mimetype='application/json'),400    

@app.route("/api/v1/machines" , methods=['DELETE'])
def delete_machines():
    machine=Machine()
    machine.delete_all()
    return Response(dumps({'deleted' : True}), mimetype='application/json'),200

@app.route("/api/v1/machines/<name>", methods=['DELETE'])
def delete_machine(name):
    machine=Machine()
    if not machine.delete(name):
        return Response(dumps({'deleted' : False}), mimetype='application/json'),404
    return Response(dumps({'deleted' : True}), mimetype='application/json'),200


@app.route("/api/v1/machines", methods=['PUT','PATCH'])
def bad_update_machine():
    return Response(dumps({'added' : False, 'reason' : 'This request is not supported. For more information visit the API documetation', 'url' : 'http://fabexpertizer.herokuapp.com'}), mimetype='application/json'),400    

@app.route("/api/v1/machines/<current_name>", methods=['PUT','PATCH'])
def update_machine(current_name):
    json=request.json
    machine=Machine()
    if not machine.name_exists(current_name):
        res={"error" : "Not Found", "reason" : "The name especified has not been found in the database." }
        return Response(dumps(res), mimetype='application/json'),404
    
    modifications=0
    try:
        name=json['name']
        machine.set_machine(current_name,"name",name)
        modifications+=1
    except KeyError:
        pass

    try:
        description=json['description']
        machine.set_machine(current_name,"description",description)
        modifications+=1
    except KeyError:
        pass
    
    try:
        properties=json['properties']
        machine.set_machine(current_name,"properties",properties)
        modifications+=1
    except KeyError:
        pass
    
    try:
        thicknesses=json['thicknesses']
        machine.set_machine(current_name,"thicknesses",thicknesses)
        modifications+=1
    except KeyError:
        pass

    if not modifications:
        res={'updated' : False, 'reason' : 'Bad especified properties'}
        return Response(dumps(res), mimetype='application/json'),400    
    else:
        res={'updated' : True}
        return Response(dumps(res), mimetype='application/json'), 200


##########################################################
#################### RESOURCE FABEXS #####################
##########################################################
    
    # blog
    # author
    # title
    # description
    # created
    # top
    # front
    # left
    # source

@app.route('/api/v1/fabexs', methods=['GET'])
def get_fabexs():
    fabex=Fabex()
    if len(request.args) > 0:
        keywords=request.args.get("q").split(",")
        fabexs=fabex.get_fabexs(keywords)       
    else:
        fabexs=fabex.get_fabexs(None)
    if fabexs.count() == 0:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    return Response(dumps(fabexs),  mimetype='application/json'),200



@app.route('/api/v1/fabexs/<int:oid>', methods=['GET'])
def get_fabex_oid(oid):
    fabex=Fabex().get_fabex_oid(oid)
    if not fabex:
        res={"reason" : "No elements were found"}
        return Response(dumps(res), mimetype='application/json'),404
    return Response(dumps(fabex),  mimetype='application/json'),200



@app.route('/api/v1/fabexs/<username>', methods=['GET'])
def get_fabex_string(username):
    res={"reason" : "The last URL element must be an integer."}
    return Response(dumps(res), mimetype='application/json'),400

@app.route('/api/v1/fabexs/<someinfo>', methods=['POST'])
def post_fabex_failed(someinfo):
    res={"added" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'),400

@app.route('/api/v1/fabexs', methods=['POST'])
def post_fabex():
    json=request.json
    machine=Machine()
    fabex=Fabex()
    fabber=Fabber()
    path=app.config['UPLOAD_FOLDER']+"fabex_img/";
    try:
        title=json['title']
        fablab=json['fablab']
        machine_name=json['machine']
        author=json['author']

    except:
        res={"added" : False, "reason" : "Some main property was not indicated"}
        return Response(dumps(res),mimetype='application/json'),400
    if session["logged"] and session["username"] ==  author:
        if not machine.name_exists(machine_name):
            res={"added" : False , "reason" : "Machine not found"}
            return Response(dumps(res), mimetype="application/json"),404

        try:
            properties=json['properties']
        except:
            res={"added" : False, "reason" : "Some main property was not indicated"}
            return Response(dumps(res),mimetype='application/json'),400
        try:
            description=json['description']
        except:
            description=None
        try:
            blog=json['blog']
        except:
            blog=False
        _id=fabex.create_fabex(title,machine_name,fablab,author,properties,description,blog)
        
        try:
            left=json['left']
            fabex.addPhoto(_id,path,"left",left)
        except:
            pass
        try:
            top=json['top']
            fabex.addPhoto(_id,path,"top",top)
        except:
            pass
        try:
            front=json['front']
            fabex.addPhoto(_id,path,"front",front)
        except:
            pass
            
        res={"created" : True, "_id" : _id}
        fabber.add_fabex(author,_id)
        fabber.add_points(author,50)
        return Response(dumps(res), mimetype='application/json'),201
    else:
        res={"added" : False}
        return Response(dumps(res),mimetype="application/json"),403
        

@app.route('/api/v1/fabexs/<int:oid>', methods=['DELETE'])
def delete_fabex(oid):
    fabex=Fabex()
    if session["logged"] and fabex.get_author(oid) == session["username"]:
        author=fabex.delete(oid)
        if not author:
            return Response(dumps({'deleted' : False}), mimetype='application/json'),404
        fabber=Fabber()
        fabber.delete_fabex(author,oid)
        Comment().delete_fabex(oid)
        fabber.add_points(author,-50)
        return Response(dumps({'deleted' : True}), mimetype='application/json'),200
    return Response(dumps({'deleted' : False}), mimetype='application/json'),403

@app.route('/api/v1/fabexs/<string>', methods=['DELETE'])
def delete_fabex_error(string):
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400

@app.route('/api/v1/fabexs', methods=['DELETE'])
def delete_all_fabexs():
    fabber =Fabber()
    if session["logged"] and fabber.is_superuser(session["username"]):
        fabex=Fabex()
        fabex.delete_all()
        return Response(dumps({'deleted' : True}), mimetype='application/json'),200
    else:
        return Response(dumps({'deleted' : False}),mimetype="application/json"),403


@app.route('/api/v1/fabexs', methods=['PUT','PATCH'])
def update_fabexs_error():
    res={"updated" : False, "reason" : "This request is not supported. For more information visit the API documetation", "url" : "http://fabexpertizer.herokuapp.com"}
    return Response(dumps(res), mimetype='application/json'), 400



@app.route('/api/v1/fabexs/<int:oid>', methods=['PUT','PATCH'])
def update_fabex(oid):
    json=request.json
    fabex=Fabex()
    if not fabex.oid_exists(oid):
        res={"error" : "Not Found", "reason" : "The oid especified has not been found in the database." }
        return Response(dumps(res), mimetype='application/json'),404
    
    modificado=0
    try:
        title=json['title']
        fabex.set_fabex(oid,"title",title)
        modificado+=1
    except KeyError:
        pass
    
    try:
        blog=json['blog']
        fabex.set_fabex(oid,"blog",blog)
        modificado+=1
    except KeyError:
        pass

    try:
        description=json['description']
        fabex.set_fabex(oid,"description",description)
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
    if session["logged"] and username==session["username"]:
        fabex=Fabex()
        fabber=Fabber()
        if not fabex.oid_exists(oid) or not fabber.exists_username(username): 
            return Response(dumps({"reason" : "Not found"}) , mimetype='application/json'),404
        step1=fabber.add_like(username,oid)
        step2=fabex.add_like(oid,username)

        if step2 and step1:
            author=fabex.get_author(oid)
            fabber.add_points(author,30)
            fabber.add_points(username,5)
            return Response(dumps({"updated" : True}), mimetype='application/json'),200
        return Response(dumps({"updated" : False}), mimetype='application/json'),400
    else:
        return Response(dumps({"updated" : False}), mimetype='application/json'),403
@app.route('/api/v1/fabexs/dislike/<username>/<int:oid>', methods=['PUT','PATCH'])
def remove_like(username,oid):
    if session["logged"] and username==session["username"]:
        fabex=Fabex()
        fabber=Fabber()
        if not fabex.oid_exists(oid) or not fabber.exists_username(username): 
            return Response(dumps({"reason" : "Not found"}) , mimetype='application/json'),404
        
        step1=fabber.delete_like(username,oid)
        step2=fabex.delete_like(oid,username)
        if step2 and step1:
            author=fabex.get_author(oid)
            fabber.add_points(author,-30)
            fabber.add_points(username,-5)
            return Response(dumps({"updated" : True}), mimetype='application/json'),200
        return Response(dumps({"updated" : False}), mimetype='application/json'),400
    else:
        return Response(dumps({"updated" : False}), mimetype='application/json'),403


#####################################################################
######################### RESOURCE COMMENTS #########################
#####################################################################

    # username
    # fabex
    # comment



@app.route('/api/v1/comments/<username>/<int:oid>',methods=['POST'])
def add_comment(username,oid):
    json=request.json
    if session["logged"] and username==session["username"]:
        fabex=Fabex()
        fabber=Fabber()
        comment=Comment()
        if not fabex.oid_exists(oid) or not fabber.exists_username(username): 
            return Response(dumps({"created" : False, "reason" : "Fabber o Fabex not found"}) , mimetype='application/json'),404
        try:
            comentario=json['comment']
        except:
            res={'created' : False, 'reason' : 'Bad especified properties'}
            return Response(dumps(res), mimetype='application/json'),400

        _id=comment.create_comment(username,oid,comentario)
        fabber.add_comment(username,_id)
        author=fabex.get_author(oid)
        if author != username:
            fabber.add_points(author,30)
            fabber.add_points(username,5)
        return Response(dumps({"created" : True}), mimetype='application/json'),201  
    else:
        return Response(dumps({"updated" : False}), mimetype='application/json'),403
       

@app.route('/api/v1/comments/<username>', methods=['GET'])
def get_comment_by_user(username):
    comment_list=Comment().get_comment_username(username)
    return Response(dumps(comment_list) , mimetype="application/json"),200

@app.route('/api/v1/comments/<int:oid>', methods=['GET'])
def get_comment_by_fabex(oid):
    comment_list=Comment().get_comment_fabex(oid)
    return Response(dumps(comment_list) , mimetype="application/json"),200

@app.route('/api/v1/comments', methods=['GET'])
def get_comments():
    comment_list=Comment().get_comments()
    return Response(dumps(comment_list) , mimetype="application/json"),200

@app.route("/api/v1/comments", methods=["DELETE"])
def delete_comments():
    Comment().delete_all()
    Fabber().delete_all_comments()
    return Response(dumps({"deleted" : True}),mimetype="application/json"),200

@app.route("/api/v1/comments/<int:oid>" , methods=["DELETE"])
def delete_comment(oid):
    fabex=Fabex()
    comment=Comment()
    if session["username"] == author:
        Comment.delete(oid)
        Fabber().delete_comment(oid)    
        author=comment.get_author(oid)
        fabexoid=comment.get_fabex_by_comment(oid)
        authorF=fabex.get_author(fabexoid)
        if author != authorF:
            fabber.add_points(authorF,-30)
            fabber.add_points(author,-5)
        return Response(dumps({"deleted" : True}), mimetype="application/json"),200
    else:
        return Response(dumps({"deleted" : False, "reason" : "Not Found"}), mimetype="application/json"),404

#####################################################################
######################### RESOURCE SOURCE #########################
#####################################################################

@app.route('/api/v1/photo/<username>',methods=["PUT","PATCH"])
def upload_fablab_photo(username):
    fabber=Fabber()
    file = request.files['file']
    if file and allowed_file(file.filename):
        ext      =file.filename.split(".")[-1]
        filename =username+"."+ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+"profile-photos/",filename))
        url_file ="profile-photos/"+filename
        fabber.add_photo(username,url_file)
        return Response(dumps({"updated": True}), mimetype="application/json"),201
    else:
        return Response(dumps({"updated" : False, "reason" : "Bad type file"}), mimetype="application/json"),400

@app.route('/api/v1/fablab/photo/<name>',methods=["PUT","PATCH"])
def upload_photo(name):
    fablab=Fablab()
    file = request.files['file']
    if file and allowed_file(file.filename):
        ext      =file.filename.split(".")[-1]
        filename =name+"."+ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+"fablab-photos/",filename))
        url_file ="fablab-photos/"+filename
        fablab.add_photo(name,url_file)
        return Response(dumps({"updated": True}), mimetype="application/json"),201
    else:
        return Response(dumps({"updated" : False, "reason" : "Bad type file"}), mimetype="application/json"),400


@app.route('/api/v1/source/<int:oid>', methods=['PUT','PATCH'])
def upload_file_source(oid):
    cont=0
    fabex=Fabex()
    if request.method == 'PUT' or request.method == 'PATCH':
        file = request.files['file']
        if file:
            parts      =file.filename.split(".")
            ext        =parts[-1]
            name       =fabex.get_fabex_oid(oid)
            title      =str(name['title'])
            titleCamel =''.join(x for x in title.title() if not x.isspace())
            filename   ="{}-{}.{}".format(titleCamel,oid,ext)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+"sources/", filename))
            url_file   ="sources/"+filename
            fabex.add_source(oid,url_file)
            return Response(dumps({"updated" : True}), mimetype="application/json"),201
        else:
            return Response(dumps({"updated" : False}), mimetype="application/json"),400


if __name__ == "__main__":
    app.run()