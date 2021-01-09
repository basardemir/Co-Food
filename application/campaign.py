from flask import Flask, render_template
from services.campaign import *
from flask import Flask, render_template
from services.restaurant import *
from flask_login.utils import *
from forms.filter import CampaignSearchForm

@login_required
def getCampaigns():
    if session['role'] == 'student':
        form = CampaignSearchForm()
        campaigns = getAllCampaigns()
        return render_template("consumerViews/campaigns.html", campaigns=campaigns, form=form)
    else:
        return render_template("errorViews/403.html")

@login_required
def filterCampaigns():
    if session['role'] == 'student':
        form = CampaignSearchForm()
        campaigns=filterCampaign(request.form['menuname'], request.form['categories'])
        return render_template("consumerViews/campaigns.html", form=form, campaigns=campaigns)
    else:
        return render_template("errorViews/403.html")