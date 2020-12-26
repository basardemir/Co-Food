from flask import Flask, render_template
from services.campaign import *

def getCampaigns():
    campaigns = getAllCampaigns()
    return render_template("consumerViews/campaigns.html", campaigns=campaigns)