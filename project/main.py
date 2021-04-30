import os
from flask import Blueprint, render_template, Flask, flash, request,redirect,send_file, session, send_from_directory
from . import db
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

import glob

import spacy
from textblob import TextBlob
from gensim.summarization import summarize

from flask import current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Removing Files
        # Pfiles = glob.glob('uploads/*')
        # for f in Pfiles:
        #     os.remove(f)

        # Pfiles2 = glob.glob('uploads2/*')
        # for f in Pfiles2:
        #     os.remove(f)
        req = request.form
        # check if the post request has the file part
        if req['form-name'] == 'form1':
            text_area = req['txtarea']
            percent = int(req['percent'])
            percent = percent/100
            print(percent)
            sum_text = summarize(text_area, percent)
            return render_template('profile.html', in_text=text_area, sum_text=sum_text)
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            # path = 'static/upload/'

            file.save(os.path.join(current_app.config['FOLDER'], filename))

            text = " ".join((line for line in open(os.path.join(current_app.config['FOLDER'], filename), encoding='utf-8')))
            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            percent = int(req['percent'])
            percent = percent/100
            text2 = summarize(text, percent)
            print("after summary.....")

            print(filename)
            with open(os.path.join(current_app.config['FOLDER2'], filename), 'w') as f:
                f.write(text2)

            print("saved file successfully")

            return redirect('/downloadfile/'+ filename)
    return render_template('profile.html', name=current_user.name, in_text="Text area for input ...")


@main.route("/downloadfile/<filename>", methods = ['GET'])
@login_required
def download_file(filename):
    return render_template('download.html',value=filename)

@main.route("/return-files/<filename>")
@login_required
def return_files_tut(filename):
    # file_path = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
    if os.path.isfile(os.path.join(current_app.config['FOLDER2'], filename)):
        print("yes file is present")
    print("file for sent is ::: ")
    path = 'static/download'
    return send_from_directory(path, filename=filename, as_attachment=True, attachment_filename="Sum_"+filename, cache_timeout=-1)



