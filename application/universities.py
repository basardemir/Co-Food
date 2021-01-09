from flask import Flask, render_template
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login.utils import *
from forms.filter import RestaurantSearchForm
from services.university import *
from forms.university import *
from flask import Flask, render_template, request
from services.students import *

@login_required
def adminUniversities():
    if session['role'] == 'admin':
        universities = getAllUniversities()
        return render_template("adminViews/universities.html", universities=universities)
    else:
        return render_template("errorViews/403.html")

@login_required
def deleteUniversity(uniId):
    if session['role'] == 'admin':
        if(deleteUniversityById(uniId)):
            universities = getAllUniversities()
            return render_template("adminViews/universities.html", universities=universities)
        else:
            universities = getAllUniversities()
            return render_template("adminViews/universities.html", universities=universities, message="You cannot delete this university")
    else:
        return render_template("errorViews/403.html")

@login_required
def addUniversity():
    if session['role'] == 'admin':
        form = UniversityEditForm()
        return render_template("adminViews/addUniversity.html", form=form)
    else:
        return render_template("errorViews/403.html")

@login_required
def insertUniversity():
    form = UniversityEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            if (addUniversityByName(name) == True):
                universities = getAllUniversities()
                return render_template("adminViews/universities.html", universities=universities)
            else:
                form = UniversityEditForm()
                return render_template("adminViews/addUniversity.html", form=form, message="This name is already exist")
        else:
            return render_template("errorViews/403.html")


@login_required
def editUniversity(uniId):
    if session['role'] == 'admin':
        university = getUniversityById(uniId)
        if university:
            form = UniversityEditForm()
            students = getAllStudentsByUniId(uniId)
            return render_template("adminViews/editUniversity.html", form = form, university=university, students = students)
        else:
            universities = getAllUniversities()
            return render_template("adminViews/universities.html",universities=universities, message="This university does not exists")
    else:
        return render_template("errorViews/403.html")

@login_required
def saveUniversity(uniId):
    form = UniversityEditForm()
    if form.validate_on_submit():
        if session['role'] == 'admin':
            name = request.form['name']
            if(editUniversityById(uniId,name) == True):
                university = getUniversityById(uniId)
                if university:
                    form = UniversityEditForm()
                    students = getAllStudentsByUniId(uniId)
                    return render_template("adminViews/editUniversity.html", form = form, university=university, students = students)
                else:
                    universities = getAllUniversities()
                    return render_template("adminViews/universities.html",universities=universities, message="This university does not exists")
            else:
                university = getUniversityById(uniId)
                if university:
                    students = getAllStudentsByUniId(uniId)
                    form = UniversityEditForm()
                    return render_template("adminViews/editUniversity.html", form=form, university=university,message="This name already exists", students = students)
                else:
                    universities = getAllUniversities()
                    return render_template("adminViews/universities.html", universities=universities,
                                           message="This university does not exists")
        else:
            return render_template("errorViews/403.html")

