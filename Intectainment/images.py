import os, urllib.request, shutil
from Intectainment.app import app
from Intectainment.datamodels import Channel, User, db
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif", "bmp", "svg", "ico"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def create_subfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def deleteImage(user: User):
    if user.icon_extension:
        source_path = os.path.join(app.config["UPLOAD_FOLDER"], "usr/", str(user.id) + user.icon_extension)
        user.icon_extension = None
        if os.path.exists(source_path):
            os.remove(source_path)
        db.session.add(user)
        db.session.commit()
        user.reload()

def softImageDelete(user: User):
    if user.icon_extension:
        source_path = os.path.join(app.config["UPLOAD_FOLDER"], "usr/", str(user.id) + "." + user.icon_extension)
        if os.path.exists(source_path):
            os.remove(source_path)

def softImageDelete(channel: Channel):
    if channel.icon_extension:
        source_path = os.path.join(app.config["UPLOAD_FOLDER"], "c/", str(channel.id) + "." + channel.icon_extension)
        if os.path.exists(source_path):
            os.remove(source_path)

def move_images(userid, postid):
    source_path = os.path.join(app.config["UPLOAD_FOLDER"], "usr/tmp", str(userid))
    if os.path.exists(source_path):
        destination_path = app.config["UPLOAD_FOLDER"]
        shutil.move(source_path, destination_path)
        os.rename(os.path.join(app.config["UPLOAD_FOLDER"], str(userid)), os.path.join(app.config["UPLOAD_FOLDER"], str(postid)))
        source_path = os.path.join(app.config["UPLOAD_FOLDER"], str(postid))
        destination_path = os.path.join(app.config["UPLOAD_FOLDER"], "p", str(postid))
        shutil.move(source_path, destination_path)

def upload_image(name="", folder="c", subfolder="", type=""):
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No Image is selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if name != "":
            filename = name + "." + get_extension(file.filename)
        create_subfolder(os.path.join(app.config["UPLOAD_FOLDER"], folder, subfolder))
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], folder, subfolder, filename))

        profile = None

        if folder == "c":
            channel = Channel.query.filter_by(id=int(name)).first()
            softImageDelete(channel)
            channel.icon_extension = get_extension(file.filename)
            db.session.add(channel)
            db.session.commit()
        elif folder == "usr":
            profile = True
            user = User.query.filter_by(id=int(name)).first()
            softImageDelete(user)
            user.icon_extension = get_extension(file.filename)
            db.session.add(user)
            db.session.commit()
            user.reload()

        path = None
        if type:
            path = url_for("display_image_posts", type=type, post_id=subfolder, filename=filename)
        else:
            path = url_for("display_image_", type=folder, filename=filename)

        return render_template("img/upload.html", path=path, type=type, profile=profile)

    else:
        flash("Zulässige Dateiendungen sind: png, jpg, jpeg, gif, bmp, svg, ico")
        return redirect(request.url)

def display_image(folder, filename):
    return redirect(url_for("static", filename="img/" + folder + "/" + filename), code=301)