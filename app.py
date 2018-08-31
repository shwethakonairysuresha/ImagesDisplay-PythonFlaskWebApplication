import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/upload", methods=['GET','POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print (target)

    if not os.path.isdir(target):
        os.mkdir(target)
    mylist = []
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        mylist.append(file)
    print mylist

    imgs = [Image.open(i) for i in mylist]
    print(imgs)

    # Find the smallest image, and resize the other images to match it
    min_img_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    img_merge = np.hstack((np.asarray(i.resize(min_img_shape, Image.ANTIALIAS)) for i in imgs))

    # save the horizontally merged images
    img_merge = Image.fromarray(img_merge)
    img_merge.save('static/output.jpg')

    #image_path= 'output.jpg'
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)

    #full_filename = os.path.join('static', 'output.jpg')
    #path = dir_path + full_filename
    #print(full_filename)

    return render_template("complete.html", image_output='output.jpg')

if __name__ == '__main__':
    app.run(debug=True)