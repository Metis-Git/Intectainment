from flask import render_template, send_from_directory, request, redirect, url_for, session, Blueprint
import os

from Intectainment.app import app
from Intectainment.database.models import User


@app.before_request
def before_request():
	User.resetTimeout()
	pass


@app.route("/")
def mainPage():
	return render_template("main/start.html")

@app.route("/home")
def home():
	if not User.isLoggedIn():
		return redirect(url_for("login"))
	else:
		return render_template("main/home.html")



### Access Points ###
accessPoints: Blueprint = Blueprint("accessPoints", __name__, url_prefix="/inteface")
@accessPoints.route("/user/login", methods = ["POST"])
def login():
	"""login access point"""
	if User.isLoggedIn():
		return redirect(url_for("home"))

	if request.method == "POST":
		if "username" and "password" in request.form:
			if User.logIn(request.form["username"], request.form["password"]):
				#success
				return redirect(request.form.get("redirect") or url_for("home"))
			else:
				#failed login
				return redirect("?badLogin=1")
		else:
			#form nicht ausgefüllt
			return redirect("?badLogin=1")


@accessPoints.route("/user/logout", methods = ["POST"])
def logout():
	"""logout access point"""
	User.logOut()
	return redirect(url_for("home"))

app.register_blueprint(accessPoints)



##### Favicon #####
@app.route("/favicon.ico")
def getIcon():
    return send_from_directory(os.path.join(app.root_path, 'webpages/static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

##### Errors #####
@app.errorhandler(404)
def page_not_found(e):
	return render_template("errors/error_404.html"), 404
	
@app.errorhandler(500)
def server_error(e):
	return render_template("errors/error_500.html"), 500