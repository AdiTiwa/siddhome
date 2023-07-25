import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import app, render_template, Flask, request, flash
import os
import datetime

cred = credentials.Certificate('./firebase.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'home-1b4e9.appspot.com'})
db = firestore.client()

def create_document(collection, document_data):
    doc_ref = db.collection(collection).document()
    doc_ref.set(document_data)
    return doc_ref

def update_document(collection, document_id, document_data):
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(document_data)
    return doc_ref

def upload_file(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    return blob.public_url

app = Flask(__name__)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        tags = request.form['tags']
        imgurl= request.form['imgurl']
        content = request.form['content']

        if not (title or subtitle or tags or imgurl or content):
            flash("you know better idiot")
        else:
            create_document('posts', {"title": title, "subtitle": subtitle, "date": datetime.datetime.now(), "tags": tags.split(), "img": imgurl, "text": content})


    return render_template('create.html')

@app.route('/create/album', methods=('GET', 'POST'))
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']

        if not (title or subtitle or content):
            flash("you know better idiot")
        else:
            create_document('albums', {'date': datetime.datetime.now(), "images": content.split(), "name": title, "description": subtitle})

    return render_template('create_album.html')

@app.route('/update', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        idd = request.form['id']
        timestamp = request.form.get('timestamp')
        title = request.form['title']
        subtitle = request.form['subtitle']
        tags = request.form['tags']
        imgurl= request.form['imgurl']
        content = request.form['content']

        if not idd:
            flash("you know better idiot (why no id bruh)")
        else:
            data = {}

            if title:
                data["title"] = title
            if subtitle:
                data["subtitle"] = subtitle
            if tags:
                data["tags"] = tags.split()
            if imgurl:
                data["img"] = imgurl
            if content:
                data["text"] = content
            if title:
                data["title"] = title
            if timestamp:
                data["date"] = datetime.datetime.now()

            update_document('posts', idd, data)


    return render_template('update.html')


@app.route('/update/album', methods=('GET', 'POST'))
def update_album():
    if request.method == 'POST':
        idd = request.form['id']
        timestamp = request.form.get('timestamp')
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']

        if not idd:
            flash("you know better idiot (why no id bruh)")
        else:
            data = {}

            if title:
                data["title"] = title
            if subtitle:
                data["subtitle"] = subtitle
            if content:
                data["images"] = content.split()
            if timestamp:
                data["date"] = datetime.datetime.now()

            update_document('albums', idd, data)


    return render_template('update_album.html')

@app.route('/')
def index():
    return render_template('index.html')

  
@app.route('/upload')  
def upload():  
    return render_template("upload.html")  
  
@app.route('/uploaded', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        filePath = upload_file(f.filename)
        os.remove(f.filename)
        return render_template("uploaded.html", path = filePath)  
  
if __name__ == '__main__':  
    app.run(debug=True)

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True # allow for template reloads to make it easier
    app.run(debug=True, threaded=True, port=port)