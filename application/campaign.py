from services.campaign import *
from flask import render_template
from flask_login.utils import *

from forms.filter import CampaignSearchForm
from services.campaign import *


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
        campaigns = filterCampaign(request.form['menuname'], request.form['categories'])
        return render_template("consumerViews/campaigns.html", form=form, campaigns=campaigns)
    else:
        return render_template("errorViews/403.html")
