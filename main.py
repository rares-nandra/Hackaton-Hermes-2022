from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response, send_from_directory, send_file, jsonify
from modulos import mongodb
from modulos import geo
from modulos import search
import os
app = Flask(__name__)
db = mongodb.mongodb()
pletea = geo.pletea()
se = search.Search()

app.config['SECRET_KEY'] = 'Am bagat un xanny in my lean' 


@app.route('/statice/<path:path>')
def send_report(path):
    return send_from_directory('statice', path)

@app.route("/")
def ikljfk():
    return redirect(url_for("auth"))

@app.route("/home")
def home():
    if not "diseases" in db.data(request.cookies.get("user")):
        return redirect(url_for("edit"))
    elif db.verificareUser(request.cookies.get("user"), request.cookies.get("parola")):

        fav = ""

        if "html" in db.data(request.cookies.get("user")):
            fav = db.data(request.cookies.get("user"))["html"]
            
        return render_template("index.html", edit=db.data(request.cookies.get("user")), search=("diseases" in db.data(request.cookies.get("user"))), saved_destinations=fav)
    else:
        return redirect(url_for("auth"))

@app.route("/favorite", methods=["POST"])
def favorite():
    if request.method == "POST":
        data = request.get_json()
        db.favorite(data,request.cookies.get("user"))
        return redirect(url_for("home"))
        
#@app.route("/limba-info", methods=["POST"])
#def limba-info():

@app.route("/search", methods=["POST"])
def searcfh():
    if(db.verificareUser(request.cookies.get("user"), request.cookies.get("parola"))):
        if("diseases" in db.data(request.cookies.get("user"))):
            data = request.get_json()
            print(data, "hhh")
            return jsonify(se.s(request.cookies.get("user"), data["vacation-type"], data["covid"], data["distance"]))
        else:
            return "nu ai dat edit"


@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/signup", methods=['POST'])
def add_signup():
    res = make_response(redirect('/auth'))
    ok = db.add({
        "nume": request.form["nume"],
        "user": request.form["user"],
        "parola": request.form["parola"]
    })
    if(ok):
        res.set_cookie("user", request.form['nume'])
        res.set_cookie("parola", request.form["parola"])
        return res

@app.route("/login", methods=["POST"])
def login():
    res = make_response(redirect('/home'))
    if(db.verificareUser(request.form["user"], request.form["parola"])):
        res.set_cookie("user", request.form['user'])
        res.set_cookie("parola", request.form["parola"])
        return res
    
    return redirect(url_for("auth"))

@app.route("/edit")
def edit():
    if(db.verificareUser(request.cookies.get("user"), request.cookies.get("parola"))):
        return render_template("personalinfo.html", edit=db.data(request.cookies.get("user")))
    else:
        return redirect(url_for("auth")) 

@app.route("/carduri")
def card():
    if(db.verificareUser(request.cookies.get("user"), request.cookies.get("parola"))):
        filename = db.fileName(request.cookies.get("user"))
        return send_file("carduri/" + filename)

@app.route("/edit-info", methods=['POST'])
def editinfo():
    user = request.cookies.get("user")
    if db.verificareUser(user, request.cookies.get("parola")):
        poza = request.files["poza"]
        type=""
        if poza.filename.endswith("png"):
            type = ".png"
        elif poza.filename.endswith("jpg"):
            type = ".jpg"
        elif poza.filename.endswith("jpeg"):
            type = ".jpeg"
        elif poza.filename.endswith("bmp"):
            type = ".bmp"

        nume_poza = user + type
        poza.save(os.path.join("carduri", nume_poza))

        diseases = []
        
        try:

            if "Blindness" in request.form:
                diseases.append("Blindness")
            
            if "Deafness" in request.form:
                diseases.append("Deafness")

            if "Locomotory" in request.form:
                diseases.append("Locomotory")

            if "Asthma" in request.form:
                diseases.append("Asthma")

            if "Allergies" in request.form:
                diseases.append("Allergies")
        except:
            pass

        data = {
            "filename": nume_poza,
            "blood": request.form["blood"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "diseases": diseases
        }

        db.update(data, user)


        return redirect(url_for("home"))
    else:
        return redirect(url_for("auth"))


# @app.route("/locatiii", methods=['POST'])
# def editinfo():



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")