from flask import Blueprint,redirect,url_for,request,flash,render_template,session
from.model import *
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user


auth = Blueprint('auth', __name__)

@auth.route('/signupvalidation', methods=['GET','POST'])
def signupvalidation():
    try:
        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            age = request.form['age']
            sex = request.form['sex']
            phone_no = request.form['contactnumber']
            email = request.form['email']
            password = request.form['password']
            user = UserDetails(first_name=first_name,
                           last_name=last_name,
                           age=age,
                           sex=sex,
                           phone_no=phone_no,
                           email=email,
                           password=generate_password_hash(password)
                               )
            if user:
                db.session.add(user)
                db.session.commit()
                flash(f'Created Successfully', category='Success')
                return redirect(url_for('views.login'))
        else:
            return redirect(url_for('views.signup'))
        return redirect(url_for('views.signup'))
    except Exception as e:
        flash(e,category='error')

@auth.route('/loginvalidation', methods=['GET', 'POST'])
def loginvalidation():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            userdetail = UserDetails.query.filter_by(email=email).first()
            if userdetail and check_password_hash(userdetail.password, password):
                login_user(userdetail)
                session['user'] = email
                flash('Login Successfully', category='success')
                storeitems = Purchase.query.filter_by(user_id=userdetail.id).all()
                return render_template('homepage.html', id=userdetail.id, email=userdetail.email, storeitems=storeitems)
            else:
                flash('Invalid Username or Password', category='error')
                return redirect(url_for('views.login'))
        else:
            if 'user' in session:
                email = session['user']
                userdetail = UserDetails.query.filter_by(email=email).first()
                storeitems = Purchase.query.filter_by(user_id=userdetail.id).all()
                flash('Refreshed Successfully', category='success')
                return render_template('homepage.html', id=userdetail.id, email=userdetail.email, storeitems=storeitems)
            else:
                return redirect(url_for('views.login'))
    except Exception as e:
        flash(str(e),category='error')
        return redirect(url_for('views.login'))

@auth.route('/adminloginvaldation', methods=['GET','POST'])
def aloginvalidation():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            userdetail = StoreUser.query.filter_by(email=email).first()
            if userdetail and (userdetail.password == password):
                login_user(userdetail)
                session['user'] = email
                flash('Login Successfully', category='success')
                storeitems = Product.query.all()
                return render_template('Admin_Dashboard.html', id=userdetail.id, email=userdetail.email, storeitems=storeitems)
            else:
                flash('Invalid Username or Password', category='error')
                return redirect(url_for('views.admin_login'))
        else:
            if 'user' in session:
                email = session['user']
                userdetail = StoreUser.query.filter_by(email=email).first()
                storeitems = Product.query.all()
                flash('Refreshed Successfully', category='success')
                return render_template('Admin_Dashboard.html', id=userdetail.id, email=userdetail.email, storeitems=storeitems)
            else:
                return redirect(url_for('views.admin_login'))
    except Exception as e:
        flash(str(e),category='error')
        return redirect(url_for('views.admin_login'))
    
@auth.route('/buyeditems', methods=['POST'])
def buyeditems():
    id = request.form.get('id')
    email = request.form.get('email')
    itemName = request.form.get('itemName')
    quantity = request.form.get('quantity')
    amount = request.form.get('amount')

    userbuyed = Purchase(
        email=email,
        user_id=id,
        itemName=itemName,
        quantity=quantity,
        rate=amount
    )

    db.session.add(userbuyed)
    db.session.commit()
    flash('Items added Successfully', category='success')
    return redirect(url_for('auth.loginvalidation'))

@auth.route('/productitems', methods=['POST'])
def productitems():
        product_name = request.form.get('ProductName')
        rate = request.form.get('Rate')
        stock = request.form.get('Stock')
        userbuyed = Product(
            product_name=product_name,
            rate=rate,
            stock=stock
        )
        db.session.add(userbuyed)
        db.session.commit()
        flash('Items added Successfully', category='success')
        return redirect(url_for('auth.aloginvalidation'))
    
@auth.route('/Purchaseditems', methods = ['POST'])
def purchaseditems():
    if request.method == 'POST':
        start_date = request.form.get('startdate')
        end_date = request.form.get('endate')
        purchased = Purchase.query.filter('date_of_purchase')