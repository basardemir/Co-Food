from flask import Flask, render_template

def wait_room():
    return render_template("consumerViews/wait_room.html")
