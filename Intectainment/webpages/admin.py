from Intectainment.app import db
from Intectainment.webpages.webpages import gui
from Intectainment.database.models import User

from flask import Blueprint, render_template, request, redirect, url_for


admin: Blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/")
def main():
    return render_template("admin/main.html")

@admin.route("/user", methods= ["GET", "POST"])
def userconfig():
    if(request.method == "GET"):
        return render_template("admin/userConfig.html")
    elif(request.method == "POST"):
        post = request.form

        if post.get("createUser"):
            # all fields are filled
            if post.get("username") and post.get("email") and post.get("password"):

                #if username is not taken
                if User.query.filter_by(username=post.get("username")).first() is None:
                    user = User()
                    user.username = post.get("username")
                    user.email = post.get("email")
                    user.changePassword(post.get("password"))

                    db.session.add(user)
                    fail = False
                    try:
                        db.session.commit()
                    except:
                        fail = True
                    if not fail:
                        return render_template("admin/userConfig.html", createUser="success", userName=post.get("username"))
                    else:
                        return render_template("admin/userConfig.html", createUser="fail", error="SQL Fehler")
                    pass
                else:
                    #username taken
                    return render_template("admin/userConfig.html", createUser="fail", error="Benutzername existiert schon")
                    pass
                pass
            else:
                #nicht ausgefüllt
                pass
            pass
        elif post.get("queryUser"):
            users = User.query

            if post.get("queryname"):
                users = users.filter_by(username=post.get("queryname"))

            return render_template("admin/userConfig.html", users = users.all())
            #continue
            pass

        return redirect(url_for("admin.userconfig"))
    pass




gui.register_blueprint(admin)