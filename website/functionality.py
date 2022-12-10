from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
import sqlite3
from . import db
import json
from .DBmodel import Product
from sqlalchemy.sql import select
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    The page to add a task. If there is a POST request, the program will create the task, and save it in the Database. 
    """

    
    return render_template("home.html", user=current_user)
    


@views.route('/browse', methods=['GET', 'POST'])
def browse():
    "Render the restaurant browsing page"
    
    if request.method == 'POST':
        
        location = request.form.get('locat')
        if location == "Prishtina":
            return redirect(url_for('views.prishtina'))
        else:
            return redirect(url_for('views.home'))
            print(location, "This is location")
            
    else:
        return redirect(url_for('views.home'))


@views.route('/prishtina', methods=["GET", "POST"])
def prishtina():
    "Render the kanban board"
    
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from prishtina").fetchall()
    return render_template("prishtina.html", user=current_user, restaurants = rows)


@views.route('/sach_menu')
def sach_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'sach' OR restaurant = 'many'").fetchall()
    for row in rows:
        print(row[2], "This is row")
    return render_template("sach_menu.html", products = rows, user = current_user )

@views.route('/oldtree_menu')
def oldtree_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'oldtree'").fetchall()

    return render_template("oldtree_menu.html", products = rows, user = current_user)

@views.route('/shabani_menu')
def shabani_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'shabani'").fetchall()

    return render_template("shabani_menu.html", products = rows, user = current_user)


@views.route('/green_menu')
def green_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'green'").fetchall()

    return render_template("green_menu.html", products = rows, user = current_user)

@views.route('/missini_menu')
def missini_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'missini'").fetchall()

    return render_template("missini_menu.html", products = rows, user = current_user)

@views.route('/supreme_menu')
def supreme_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'supreme'").fetchall()

    return render_template("supreme_menu.html", products = rows, user = current_user)


@views.route('/sushi_menu')
def sushi_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'sushi'").fetchall()

    return render_template("sushi_menu.html", products = rows, user = current_user)

@views.route('/propper_menu')
def propper_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'proper'").fetchall()

    return render_template("propper_menu.html", products = rows, user = current_user)

@views.route('/sarajeva_menu')
def sarajeva_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'sarajeva'").fetchall()

    return render_template("sarajeva_menu.html", products = rows, user = current_user)


@views.route('/himalayan_menu')
def himalayan_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'himalayan'").fetchall()

    return render_template("himalayan_menu.html", products = rows, user = current_user)

@views.route('/memo_menu')
def memo_menu():
    conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
    cur = conn.cursor()
    rows = cur.execute("Select * from product where restaurant = 'memo'").fetchall()

    return render_template("memo_menu.html", products = rows, user = current_user)



@views.route('/checkout')
def checkout():
    return render_template("checkout.html", user = current_user)

@views.route('/add', methods = ['GET', 'POST'])
def add_product_to_cart():
    quantity = int(request.form['quantity'])
    code = request.form['code']
    if quantity and code and request.method == "POST":
        conn = sqlite3.connect("C:\\Users\\Albin Siriniqi\\Desktop\\Capstone\\website\database.db")
        cur = conn.cursor()
        row = cur.execute("Select * from product where id =  ?", (code,)).fetchone()
        itemArray = { str(row[0]): {'name' : row[1], 'code' : row[0], 'quantity' : quantity, 'price' : row[3], 'image' : row[2], 'total_price': quantity * row[3]}}
        print(itemArray, "th")
        all_total_price = 0
        all_total_quantiy = 0
        session.modified = True
        if 'cart_item' in session:
            
            
            if str(row[0]) in session['cart_item']:
                for key, value in session['cart_item'].items():
                    
                    if row[0] == int(key):
                        previous_quantity = session['cart_item'][key]['quantity']
                        total_quantity = previous_quantity + quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * row[3]
            else:
                session['cart_item'] = {**session['cart_item'], **itemArray}
            
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantiy += individual_quantity
                all_total_price += individual_price
        
        else:
            session['cart_item'] = itemArray
            all_total_quantiy +=  quantity
            all_total_price += quantity * row[3]
        
        session['all_total_quantity'] = all_total_quantiy
        session['all_total_price'] = all_total_price

        return redirect(url_for('views.checkout'))
    else:
        return 'Error while adding item to cart'
            
@views.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('views.checkout'))
    except Exception as e:
        print(e)


@views.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == str(code):
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + (individual_price * individual_quantity)
                break
        
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect(url_for('views.checkout'))
    except Exception as e:
        print(e)


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union(second_array)
    return False
