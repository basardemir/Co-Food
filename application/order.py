from flask import Flask, render_template

def order():
    return render_template("consumerViews/order.html")