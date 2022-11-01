from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    The page to add a task. If there is a POST request, the program will create the task, and save it in the Database. 
    """
 
    
    return render_template("home.html", user=current_user)



@views.route('/browse', methods=["GET", "POST"])
def browse():
    "Render the restaurant browsing page"
    return render_template("browse.html", user=current_user)




