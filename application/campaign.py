from services.campaign import *
from flask import render_template
from flask_login.utils import *

from forms.filter import CampaignSearchForm
from services.campaign import *
from services.restaurant import *

@login_required
def getCampaigns():
    if session['role'] == 'student':
        form = CampaignSearchForm()
        campaigns = getAllCampaigns()
        popularCampaigns = getMostPopularCampaigns()
        return render_template("consumerViews/campaigns.html", popularcampaigns=popularCampaigns, campaigns=campaigns, form=form)
    else:
        return render_template("errorViews/403.html")


@login_required
def filterCampaigns():
    if session['role'] == 'student':
        form = CampaignSearchForm()
        popularCampaigns = getMostPopularCampaigns()
        campaigns = filterCampaign(request.form['menuname'], request.form['categories'])
        return render_template("consumerViews/campaigns.html",popularcampaigns=popularCampaigns, form=form, campaigns=campaigns)
    else:
        return render_template("errorViews/403.html")
