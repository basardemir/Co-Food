from services.campaign import *
from flask import render_template
from flask_login.utils import *

from forms.filter import CampaignSearchForm
from services.campaign import *
from services.category import getAllCategoriesForm
from services.restaurant import *
from services.students import getStudentDetail


@login_required
def getCampaigns():
    if session['role'] == 'student':
        form = CampaignSearchForm()
        form.categories.choices=getAllCategoriesForm()
        student = getStudentDetail(session['id'])
        university = student['universityid']
        campaigns = getAllCampaignsWithUniversity(university)
        popularCampaigns = getMostPopularCampaigns()
        return render_template("consumerViews/campaigns.html", popularcampaigns=popularCampaigns, campaigns=campaigns, form=form)
    else:
        return render_template("errorViews/403.html")


@login_required
def filterCampaigns():
    form = CampaignSearchForm()
    if session['role'] == 'student':
        if form.validate_on_submit():
            student = getStudentDetail(session['id'])
            university = student['universityid']
            popularCampaigns = getMostPopularCampaigns()
            campaigns = filterCampaign(request.form['menuname'], request.form['categories'],university)
            form.categories.choices = getAllCategoriesForm()
            return render_template("consumerViews/campaigns.html",popularcampaigns=popularCampaigns, form=form, campaigns=campaigns)
        else:
            student = getStudentDetail(session['id'])
            university = student['universityid']
            campaigns = getAllCampaignsWithUniversity(university)
            popularCampaigns = getMostPopularCampaigns()
            form.categories.choices = getAllCategoriesForm()
            return render_template("consumerViews/campaigns.html", popularcampaigns=popularCampaigns, form=form,
                                   campaigns=campaigns)
    else:
        return render_template("errorViews/403.html")
