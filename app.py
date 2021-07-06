# from flask import Flask, render_template
from flask import (
    Flask,
    config,
    render_template,
    redirect,
    url_for,
    request,
    jsonify,
    send_from_directory,
    session,
)

# import os
# import uuid
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_migrate import Migrate, current
from datetime import datetime, date
import random
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "transport!"

# For PostgreSQL
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "postgresql://nandan:nandan2537@@localhost:5432/transport"

db = SQLAlchemy(app)
app.secret_key = "Secret Key"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)

# app = Flask(__name__)
# app.config["SECRET_KEY"] = "tradianautotrade!"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////home/nandan/Desktop/FLASKCODE/collage_transport7/collage_transport/database.db"

# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "sqlite:////../var/www/FlaskApp/AutoTrade/database.db"

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"
# migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Date, nullable=True, default=date.today())
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(600))
    passwordshow = db.Column(db.String(100))
    name = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(50), nullable=True, default="None")
    is_superuser = db.Column(db.String(50), nullable=True, default="None")
    is_user = db.Column(db.String(50), nullable=True, default="None")
    is_active = db.Column(db.String(50), nullable=True, default="True")
    approval = db.Column(db.String(50), nullable=True, default="True")

    def __init__(
        self,
        email,
        password,
        passwordshow,
        name,
        phone,
        is_superuser,
        is_user,
        is_active,
        approval,
    ):

        self.email = email
        self.password = password
        self.passwordshow = passwordshow
        self.name = name
        self.phone = phone
        self.is_superuser = is_superuser
        self.is_user = is_user
        self.is_active = is_active
        self.approval = approval


class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    pan = db.Column(db.String(100), nullable=False)
    gistin = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(250), nullable=False, default="None")
    city = db.Column(db.String(80), nullable=False, default="None")
    pin = db.Column(db.String(50), nullable=False, default="None")
    state = db.Column(db.String(50), nullable=False, default="None")
    country = db.Column(db.String(50), nullable=False, default="None")

    def __init__(self, pan, gistin, address, city, pin, state, country, email):
        self.pan = pan
        self.gistin = gistin
        self.address = address
        self.city = city
        self.pin = pin
        self.state = state
        self.country = country
        self.email = email


class CustomerUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_registered = db.Column(db.Date, nullable=True, default=date.today())
    customer_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    mobile = db.Column(db.String(50), nullable=True)
    gstin = db.Column(db.String(50), nullable=True)
    pan = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    pin = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    def __init__(
        self,
        customer_name,
        email,
        mobile,
        gstin,
        pan,
        address,
        city,
        pin,
        state,
        country,
    ):
        self.customer_name = customer_name
        self.email = email
        self.mobile = mobile
        self.gstin = gstin
        self.pan = pan
        self.address = address
        self.city = city
        self.pin = pin
        self.state = state
        self.country = country


class SupplierUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    mobile = db.Column(db.String(50), nullable=True)
    gstin = db.Column(db.String(50), nullable=True)
    pan = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    pin = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    def __init__(
        self,
        supplier_name,
        email,
        mobile,
        gstin,
        pan,
        address,
        city,
        pin,
        state,
        country,
    ):
        self.supplier_name = supplier_name
        self.email = email
        self.mobile = mobile
        self.gstin = gstin
        self.pan = pan
        self.address = address
        self.city = city
        self.pin = pin
        self.state = state
        self.country = country


class VehicleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(50), nullable=True)
    vehicle_name = db.Column(db.String(50), nullable=True)
    select_type = db.Column(db.String(50), nullable=True)
    dimension = db.Column(db.String(50), nullable=True)
    weight = db.Column(db.String(50), nullable=True)
    ground_clearence = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    manufacture_year = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    registration_no = db.Column(db.String(80), nullable=True)
    engine_no = db.Column(db.String(50), nullable=True)
    chassis_no = db.Column(db.String(50), nullable=True)

    def __init__(
        self,
        supplier_name,
        vehicle_name,
        select_type,
        dimension,
        weight,
        ground_clearence,
        model,
        manufacture_year,
        color,
        registration_no,
        engine_no,
        chassis_no,
    ):
        self.supplier_name = supplier_name
        self.vehicle_name = vehicle_name
        self.select_type = select_type
        self.dimension = dimension
        self.weight = weight
        self.ground_clearence = ground_clearence
        self.model = model
        self.manufacture_year = manufacture_year
        self.color = color
        self.registration_no = registration_no
        self.engine_no = engine_no
        self.chassis_no = chassis_no


class AcidUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loadingdate = db.Column(db.String(50), nullable=True)
    ttno = db.Column(db.String(50), nullable=True)
    product = db.Column(db.String(50), nullable=True)
    loadedat = db.Column(db.String(50), nullable=True)
    destination = db.Column(db.String(50), nullable=True)
    lrno = db.Column(db.String(50), nullable=True)
    invoice = db.Column(db.String(50), nullable=True)
    loadqty = db.Column(db.String(50), nullable=True)
    shortage = db.Column(db.String(50), nullable=True)
    unloadingdate = db.Column(db.String(50), nullable=True)
    unloadingqty = db.Column(db.String(80), nullable=True)
    helperunload = db.Column(db.String(50), nullable=True)
    hsdqty = db.Column(db.String(50), nullable=True)
    advcash = db.Column(db.String(50), nullable=True)
    totaladv = db.Column(db.String(50), nullable=True)
    billingrate = db.Column(db.String(50), nullable=True)
    totalamount = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)

    def __init__(
        self,
        loadingdate,
        ttno,
        product,
        loadedat,
        destination,
        lrno,
        invoice,
        loadqty,
        shortage,
        unloadingdate,
        unloadingqty,
        helperunload,
        hsdqty,
        advcash,
        totaladv,
        billingrate,
        totalamount,
        status,
    ):
        self.loadingdate = loadingdate
        self.ttno = ttno
        self.product = product
        self.loadedat = loadedat
        self.destination = destination
        self.lrno = lrno
        self.invoice = invoice
        self.loadqty = loadqty
        self.shortage = shortage
        self.unloadingdate = unloadingdate
        self.unloadingqty = unloadingqty
        self.helperunload = helperunload
        self.hsdqty = hsdqty
        self.advcash = advcash
        self.totaladv = totaladv
        self.billingrate = billingrate
        self.totalamount = totalamount
        self.status = status
        
        
        
class NrlUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loadingdate = db.Column(db.String(50), nullable=True)
    ttno = db.Column(db.String(50), nullable=True)
    shipmentno = db.Column(db.String(50), nullable=True)
    qty = db.Column(db.String(50), nullable=True)
    shortage = db.Column(db.String(50), nullable=True)
    unloadingdate = db.Column(db.String(50), nullable=True)
    unloadingqty = db.Column(db.String(50), nullable=True)
    rate = db.Column(db.String(50), nullable=True)
    destination = db.Column(db.String(50), nullable=True)
    toll = db.Column(db.String(50), nullable=True)
    totalamount = db.Column(db.String(50), nullable=True)
    shortageamount = db.Column(db.String(50), nullable=True)
    product = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)

    def __init__(
        self,
        loadingdate,
        ttno,
        shipmentno,
        qty,
        shortage,
        unloadingdate,
        unloadingqty,
        rate,
        destination,
        toll,
        totalamount,
        shortageamount,
        product,
        status,
    ):
        self.loadingdate = loadingdate
        self.ttno = ttno
        self.shipmentno = shipmentno
        self.qty = qty
        self.shortage = shortage
        self.unloadingdate = unloadingdate
        self.unloadingqty = unloadingqty
        self.rate = rate
        self.destination = destination
        self.toll = toll
        self.totalamount = totalamount
        self.shortageamount = shortageamount
        self.product = product
        self.status = status
        

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    pan = db.Column(db.String(50), nullable=True)
    gstin = db.Column(db.String(50), nullable=True)
    invno = db.Column(db.String(50), nullable=True)
    invdate = db.Column(db.String(50), nullable=True)
    jobdate = db.Column(db.String(50), nullable=True)
    date_of_complition = db.Column(db.String(50), nullable=True)
    ordno = db.Column(db.String(50), nullable=True)
    orderdate = db.Column(db.String(50), nullable=True)
    gst = db.Column(db.String(50), nullable=True)
    total = db.Column(db.String(50), nullable=True)
    result = db.Column(db.String(50), nullable=True)
    description_1 = db.Column(db.String(50), nullable=True)
    description_2 = db.Column(db.String(50), nullable=True)
    description_3 = db.Column(db.String(50), nullable=True)
    description_4 = db.Column(db.String(50), nullable=True)
    description_5 = db.Column(db.String(50), nullable=True)
    description_6 = db.Column(db.String(50), nullable=True)
    description_7 = db.Column(db.String(50), nullable=True)
    description_8 = db.Column(db.String(50), nullable=True)
    description_9 = db.Column(db.String(50), nullable=True)
    description_10 = db.Column(db.String(50), nullable=True)
    hsn_sac_1 = db.Column(db.String(50), nullable=True)
    hsn_sac_2 = db.Column(db.String(50), nullable=True)
    hsn_sac_3 = db.Column(db.String(50), nullable=True)
    hsn_sac_4 = db.Column(db.String(50), nullable=True)
    hsn_sac_5 = db.Column(db.String(50), nullable=True)
    hsn_sac_6 = db.Column(db.String(50), nullable=True)
    hsn_sac_7 = db.Column(db.String(50), nullable=True)
    hsn_sac_8 = db.Column(db.String(50), nullable=True)
    hsn_sac_9 = db.Column(db.String(50), nullable=True)
    hsn_sac_10 = db.Column(db.String(50), nullable=True)
    qty_1 = db.Column(db.String(50), nullable=True)
    qty_2 = db.Column(db.String(50), nullable=True)
    qty_3 = db.Column(db.String(50), nullable=True)
    qty_4 = db.Column(db.String(50), nullable=True)
    qty_5 = db.Column(db.String(50), nullable=True)
    qty_6 = db.Column(db.String(50), nullable=True)
    qty_7 = db.Column(db.String(50), nullable=True)
    qty_8 = db.Column(db.String(50), nullable=True)
    qty_9 = db.Column(db.String(50), nullable=True)
    qty_10 = db.Column(db.String(50), nullable=True)
    rate_1 = db.Column(db.String(50), nullable=True)
    rate_2 = db.Column(db.String(50), nullable=True)
    rate_3 = db.Column(db.String(50), nullable=True)
    rate_4 = db.Column(db.String(50), nullable=True)
    rate_5 = db.Column(db.String(50), nullable=True)
    rate_6 = db.Column(db.String(50), nullable=True)
    rate_7 = db.Column(db.String(50), nullable=True)
    rate_8 = db.Column(db.String(50), nullable=True)
    rate_9 = db.Column(db.String(50), nullable=True)
    rate_10 = db.Column(db.String(50), nullable=True)
    amount_1 = db.Column(db.String(50), nullable=True)
    amount_2 = db.Column(db.String(50), nullable=True)
    amount_3 = db.Column(db.String(50), nullable=True)
    amount_4 = db.Column(db.String(50), nullable=True)
    amount_5 = db.Column(db.String(50), nullable=True)
    amount_6 = db.Column(db.String(50), nullable=True)
    amount_7 = db.Column(db.String(50), nullable=True)
    amount_8 = db.Column(db.String(50), nullable=True)
    amount_9 = db.Column(db.String(50), nullable=True)
    amount_10 = db.Column(db.String(50), nullable=True)

    def __init__(
        self,
        customer_name,
        address,
        pan,
        gstin,
        invno,
        invdate,
        jobdate,
        date_of_complition,
        ordno,
        orderdate,
        gst,
        total,
        result,
        description_1,
        description_2,
        description_3,
        description_4,
        description_5,
        description_6,
        description_7,
        description_8,
        description_9,
        description_10,
        hsn_sac_1,
        hsn_sac_2,
        hsn_sac_3,
        hsn_sac_4,
        hsn_sac_5,
        hsn_sac_6,
        hsn_sac_7,
        hsn_sac_8,
        hsn_sac_9,
        hsn_sac_10,
        qty_1,
        qty_2,
        qty_3,
        qty_4,
        qty_5,
        qty_6,
        qty_7,
        qty_8,
        qty_9,
        qty_10,
        rate_1,
        rate_2,
        rate_3,
        rate_4,
        rate_5,
        rate_6,
        rate_7,
        rate_8,
        rate_9,
        rate_10,
        amount_1,
        amount_2,
        amount_3,
        amount_4,
        amount_5,
        amount_6,
        amount_7,
        amount_8,
        amount_9,
        amount_10,
    ):
        self.customer_name = customer_name
        self.address = address
        self.pan = pan
        self.gstin = gstin
        self.invno = invno
        self.invdate = invdate
        self.jobdate = jobdate
        self.date_of_complition = date_of_complition
        self.ordno = ordno
        self.orderdate = orderdate
        self.gst = gst
        self.total = total
        self.result = result
        self.description_1 = description_1
        self.description_2 = description_2
        self.description_3 = description_3
        self.description_4 = description_4
        self.description_5 = description_5
        self.description_6 = description_6
        self.description_7 = description_7
        self.description_8 = description_8
        self.description_9 = description_9
        self.description_10 = description_10
        self.hsn_sac_1 = hsn_sac_1
        self.hsn_sac_2 = hsn_sac_2
        self.hsn_sac_3 = hsn_sac_3
        self.hsn_sac_4 = hsn_sac_4
        self.hsn_sac_5 = hsn_sac_5
        self.hsn_sac_6 = hsn_sac_6
        self.hsn_sac_7 = hsn_sac_7
        self.hsn_sac_8 = hsn_sac_8
        self.hsn_sac_9 = hsn_sac_9
        self.hsn_sac_10 = hsn_sac_10
        self.qty_1 = qty_1
        self.qty_2 = qty_2
        self.qty_3 = qty_3
        self.qty_4 = qty_4
        self.qty_5 = qty_5
        self.qty_6 = qty_6
        self.qty_7 = qty_7
        self.qty_8 = qty_8
        self.qty_9 = qty_9
        self.qty_10 = qty_10
        self.rate_1 = rate_1
        self.rate_2 = rate_2
        self.rate_3 = rate_3
        self.rate_4 = rate_4
        self.rate_5 = rate_5
        self.rate_6 = rate_6
        self.rate_7 = rate_7
        self.rate_8 = rate_8
        self.rate_9 = rate_9
        self.rate_10 = rate_10
        self.amount_1 = amount_1
        self.amount_2 = amount_2
        self.amount_3 = amount_3
        self.amount_4 = amount_4
        self.amount_5 = amount_5
        self.amount_6 = amount_6
        self.amount_7 = amount_7
        self.amount_8 = amount_8
        self.amount_9 = amount_9
        self.amount_10 = amount_10


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @login_manager.user_loader
# def load_company(user_id):
#     return Company.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("backend/login/login2.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.values.get("email")).first()
        if user:
            if check_password_hash(user.password, request.values.get("password")):
                login_user(user)
                db.session.commit()
                return jsonify(
                    success=True, msg="You have successfully logged in", url="superuser"
                )
            else:
                return jsonify(success=False, msg="Incorrect password")
        else:
            company = Company.query.filter_by(email=request.values.get("email")).first()
            if company:
                if check_password_hash(
                    company.password, request.values.get("password")
                ):
                    login_user(company)
                    db.session.commit()
                    return jsonify(
                        success=True,
                        msg="You have successfully logged in",
                        url="dashboard",
                    )
                else:
                    return jsonify(success=False, msg="Incorrect password")
            return jsonify(success=False, msg="Invalid email or password")
    return render_template("backend/login/login2.html")


# @app.route("/forgot/", methods=["GET", "POST"])
# def forgot():
#     if request.method == "POST":
#         user = User.query.filter_by(email=request.values.get("email")).first()
#         if user:
#             a_string = str(request.values.get("password"))
#             length = len(a_string)
#             if length == 6:
#                 if request.values.get("password") == request.values.get("confirmpassword"):
#                     hashed_password = generate_password_hash(
#                         request.values.get("password")
#                     )
#                     forgotuser = User.query.filter_by(email = request.values.get("email")).first()
#                     forgotuser.password = request.values.get("password")
#                     forgotuser.passwordshow = hashed_password
#                     db.session.commit()
#                     return jsonify(
#                         success=True, msg="You Password have successfully Changed", url="login"
#                     )
#                 else:
#                     return jsonify(success=False, msg="Password does not match")
#             else:
#                 return jsonify(
#                     success=False, msg="Please Enter Minimum Six Character"
#                 )
#         else:
#             return jsonify(success=False, msg="Invalid email")
#     return render_template("frontend/forgotpassword.html")


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard/")
@login_required
def dashboard():
    return render_template("backend/index.html")


@app.route("/superuser/", methods=["GET", "POST"])
@login_required
def superuser():
    if request.args.get("action") == "add":
        if request.method == "POST":

            email = request.form["email"]
            passwordshow = request.form["password"]
            a_string = str(request.form["password"])
            length = len(a_string)
            user_by_email = User.query.filter_by(email=email).first()
            if user_by_email:
                return jsonify(
                    success=False,
                    msg="This User Id already RegistRegisterderd",
                    url="register",
                )
            else:
                if length >= 4:
                    if request.form["password"] == request.form["password"]:
                        hashed_password = generate_password_hash(
                            request.form["password"]
                        )
                        password = hashed_password

                        user = User(
                            name=request.form.get("name"),
                            email=request.form.get("email"),
                            password=generate_password_hash(
                                request.form.get("password")
                            ),
                            passwordshow=request.form.get("password"),
                            phone=request.form.get("phone"),
                            is_user="1",
                            is_superuser="0",
                            is_active="1",
                            approval="1",
                        )
                        company = Company(
                            email=request.form.get("email"),
                            pan="",
                            gistin="",
                            address="",
                            city="",
                            pin="",
                            state="",
                            country="",
                        )
                        db.session.add(user)
                        db.session.add(company)
                        db.session.commit()
                        return redirect(url_for("superuser"))
                    else:
                        return jsonify(success=False, msg="Password does not match")
                else:
                    return jsonify(
                        success=False, msg="Please Enter Minimum Four Character"
                    )

    if request.args.get("action") == "edit":
        if request.args.get("id"):
            user = User.query.filter_by(id=request.args.get("id")).first()
            user.name = request.form.get("name")
            user.email = request.form.get("email")
            user.phone = request.form.get("phone")
            user.password = generate_password_hash(request.form["password"])
            user.passwordshow = request.form.get("password")
            db.session.commit()
            return redirect(url_for("superuser"))

    if request.args.get("action") == "delete":
        if request.args.get("id"):
            user = User.query.filter_by(id=request.args.get("id")).first()
            id = int(request.args.get("id")) - 1
            company = Company.query.filter_by(id=id).first()
            db.session.delete(user)
            db.session.delete(company)
            db.session.commit()
            return redirect(url_for("superuser"))

        return render_template("backend/superuser.html", user=user)
    if request.args.get("action") == "dashboard":
        if request.args.get("id"):
            company = Company.query.filter_by(id=request.args.get("id"))
            return render_template("backend/index.html", company=company)
    user = User.query.filter_by(is_user="1")
    return render_template("backend/superuser.html", user=user)


# ------------------update---------------------------

# @app.route('/superuser/<int:id>/update',methods = ['GET','POST'])
# def update(id):
#     user = User.query.filter_by(user=id).first()
#     if request.method == 'POST':
#         if user:
#             db.session.delete(user)
#             db.session.commit()

#             name = request.form['name']
#             email = request.form['email']
#             phone = request.form['phone']
#             password = request.form['password']

#             db.session.add(user)
#             db.session.commit()
#             return redirect(f'/superuser/{id}')
#         return f"User with id = {id} Does nit exist"

#     return render_template('update.html', user = user)


# ------------------------------------------------------------------------


@app.route("/customers/", methods=["POST", "GET"])
@login_required
def customers():
    if request.args.get("action") == "add":
        if request.method == "POST":
            # print(request.form["state"])
            # print(request.form.get("country"))
            customer = CustomerUser(
                customer_name=request.form.get("customer_name"),
                email=request.form.get("email"),
                mobile=request.form.get("mobile"),
                gstin=request.form.get("gstin"),
                pan=request.form.get("pan"),
                address=request.form.get("address"),
                city=request.form.get("city"),
                pin=request.form.get("pin"),
                state=request.form["state"],
                country=request.form.get("country"),
            )
            db.session.add(customer)
            db.session.commit()
            # return jsonify(success=True, url="pharmacy")
            return redirect(url_for("customers"))

    if request.args.get("action") == "edit":
        # print("hellooooooooooooooooooo")
        if request.args.get("id"):
            # print("goodggggggggggggggg")
            customer = CustomerUser.query.filter_by(id=request.args.get("id")).first()
            customer.customer_name = request.form.get("customer_name")
            customer.email = request.form.get("email")
            customer.mobile = request.form.get("mobile")
            customer.gstin = request.form.get("gstin")
            customer.pan = request.form.get("pan")
            customer.address = request.form.get("address")
            customer.city = request.form.get("city")
            customer.pin = request.form.get("pin")
            customer.state = request.form.get("state")
            customer.country = request.form.get("country")
            db.session.commit()
            return redirect(url_for("customers"))

    if request.args.get("action") == "delete":
        if request.args.get("id"):
            customer = CustomerUser.query.filter_by(id=request.args.get("id")).first()
            db.session.delete(customer)
            db.session.commit()
            return redirect(url_for("customers"))
        return render_template("backend/customer/customers.html", customer=customer)

    customer = CustomerUser.query.all()
    return render_template("backend/customer/customers.html", customer=customer)


@app.route("/suppliers/", methods=["POST", "GET"])
@login_required
def suppliers():
    if request.args.get("action") == "add":
        if request.method == "POST":
            # print(request.form["state"])
            # print(request.form.get("country"))
            supplier = SupplierUser(
                supplier_name=request.form.get("supplier_name"),
                email=request.form.get("email"),
                mobile=request.form.get("mobile"),
                gstin=request.form.get("gstin"),
                pan=request.form.get("pan"),
                address=request.form.get("address"),
                city=request.form.get("city"),
                pin=request.form.get("pin"),
                state=request.form["state"],
                country=request.form.get("country"),
            )
            db.session.add(supplier)
            db.session.commit()
            return redirect(url_for("suppliers"))

    if request.args.get("action") == "edit":
        # print("hellooooooooooooooooooo")
        if request.args.get("id"):
            # print("goodggggggggggggggg")
            supplier = SupplierUser.query.filter_by(id=request.args.get("id")).first()
            supplier.supplier_name = request.form.get("supplier_name")
            supplier.email = request.form.get("email")
            supplier.mobile = request.form.get("mobile")
            supplier.gstin = request.form.get("gstin")
            supplier.pan = request.form.get("pan")
            supplier.address = request.form.get("address")
            supplier.city = request.form.get("city")
            supplier.pin = request.form.get("pin")
            supplier.state = request.form.get("state")
            supplier.country = request.form.get("country")
            db.session.commit()
            return redirect(url_for("suppliers"))

    if request.args.get("action") == "delete":
        if request.args.get("id"):
            supplier = SupplierUser.query.filter_by(id=request.args.get("id")).first()
            db.session.delete(supplier)
            db.session.commit()
            return redirect(url_for("suppliers"))
        return render_template("backend/supplier/suppliers.html", supplier=supplier)

    supplier = SupplierUser.query.all()
    return render_template("backend/supplier/suppliers.html", supplier=supplier)


@app.route("/vehicles/", methods=["POST", "GET"])
@login_required
def vehicles():
    if request.args.get("action") == "add":
        if request.method == "POST":
            # print(request.form["state"])
            # print(request.form.get("country"))
            vehicle = VehicleUser(
                supplier_name=request.form.get("supplier_name"),
                vehicle_name=request.form.get("vehicle_name"),
                select_type=request.form.get("select_type"),
                dimension=request.form.get("dimension"),
                weight=request.form.get("weight"),
                ground_clearence=request.form.get("ground_clearence"),
                model=request.form.get("model"),
                manufacture_year=request.form.get("manufacture_year"),
                color=request.form["color"],
                registration_no=request.form.get("registration_no"),
                engine_no=request.form.get("engine_no"),
                chassis_no=request.form.get("chassis_no"),
            )
            db.session.add(vehicle)
            db.session.commit()
            return redirect(url_for("vehicles"))

    if request.args.get("action") == "edit":
        # print("hellooooooooooooooooooo")
        if request.args.get("id"):
            # print("goodggggggggggggggg")
            vehicle = VehicleUser.query.filter_by(id=request.args.get("id")).first()
            vehicle.supplier_name = request.form.get("supplier_name")
            vehicle.vehicle_name = request.form.get("vehicle_name")
            vehicle.select_type = request.form.get("select_type")
            vehicle.dimension = request.form.get("dimension")
            vehicle.weight = request.form.get("weight")
            vehicle.ground_clearence = request.form.get("ground_clearence")
            vehicle.model = request.form.get("model")
            vehicle.manufacture_year = request.form.get("manufacture_year")
            vehicle.color = request.form.get("color")
            vehicle.registration_no = request.form.get("registration_no")
            vehicle.engine_no = request.form.get("engine_no")
            vehicle.chassis_no = request.form.get("chassis_no")
            db.session.commit()
            return redirect(url_for("vehicles"))

    if request.args.get("action") == "delete":
        if request.args.get("id"):
            vehicle = VehicleUser.query.filter_by(id=request.args.get("id")).first()
            db.session.delete(vehicle)
            db.session.commit()
            return redirect(url_for("vehicles"))

    supplier = SupplierUser.query.all()
    vehicle = VehicleUser.query.all()
    return render_template(
        "backend/vehicle/vehicles.html", vehicle=vehicle, supplier=supplier
    )


@app.route("/billing/", methods=["POST", "GET"])
@login_required
def billing():
    if request.args.get("action") == "add":
        if request.method == "POST":
            bill = Billing(
                customer_name=request.form.get("customer_name"),
                address=request.form.get("address"),
                pan=request.form.get("pan"),
                gstin=request.form.get("gstin"),
                invno=request.form.get("invno"),
                invdate=request.form.get("invdate"),
                jobdate=request.form.get("jobdate"),
                date_of_complition=request.form.get("date_of_complition"),
                ordno=request.form.get("ordno"),
                orderdate=request.form.get("orderdate"),
                gst=request.form.get("gst"),
                total=request.form.get("total"),
                result=request.form.get("result"),
                description_1=request.form.get("description_1"),
                description_2=request.form.get("description_2"),
                description_3=request.form.get("description_3"),
                description_4=request.form.get("description_4"),
                description_5=request.form.get("description_5"),
                description_6=request.form.get("description_6"),
                description_7=request.form.get("description_7"),
                description_8=request.form.get("description_8"),
                description_9=request.form.get("description_9"),
                description_10=request.form.get("description_10"),
                hsn_sac_1=request.form.get("hsn_sac_1"),
                hsn_sac_2=request.form.get("hsn_sac_2"),
                hsn_sac_3=request.form.get("hsn_sac_3"),
                hsn_sac_4=request.form.get("hsn_sac_4"),
                hsn_sac_5=request.form.get("hsn_sac_5"),
                hsn_sac_6=request.form.get("hsn_sac_6"),
                hsn_sac_7=request.form.get("hsn_sac_7"),
                hsn_sac_8=request.form.get("hsn_sac_8"),
                hsn_sac_9=request.form.get("hsn_sac_9"),
                hsn_sac_10=request.form.get("hsn_sac_10"),
                qty_1=request.form.get("qty_1"),
                qty_2=request.form.get("qty_2"),
                qty_3=request.form.get("qty_3"),
                qty_4=request.form.get("qty_4"),
                qty_5=request.form.get("qty_5"),
                qty_6=request.form.get("qty_6"),
                qty_7=request.form.get("qty_7"),
                qty_8=request.form.get("qty_8"),
                qty_9=request.form.get("qty_9"),
                qty_10=request.form.get("qty_10"),
                rate_1=request.form.get("rate_1"),
                rate_2=request.form.get("rate_2"),
                rate_3=request.form.get("rate_3"),
                rate_4=request.form.get("rate_4"),
                rate_5=request.form.get("rate_5"),
                rate_6=request.form.get("rate_6"),
                rate_7=request.form.get("rate_7"),
                rate_8=request.form.get("rate_8"),
                rate_9=request.form.get("rate_9"),
                rate_10=request.form.get("rate_10"),
                amount_1=request.form.get("amount_1"),
                amount_2=request.form.get("amount_2"),
                amount_3=request.form.get("amount_3"),
                amount_4=request.form.get("amount_4"),
                amount_5=request.form.get("amount_5"),
                amount_6=request.form.get("amount_6"),
                amount_7=request.form.get("amount_7"),
                amount_8=request.form.get("amount_8"),
                amount_9=request.form.get("amount_9"),
                amount_10=request.form.get("amount_10"),
            )
            db.session.add(bill)
            db.session.commit()
            # return render_template("backend/bill/billing.html")
            return redirect(url_for("billing"))
        customer = CustomerUser.query.all()
        return render_template("backend/bill/createbill.html",customer=customer)
    
    if request.args.get("action") == "delete":
        if request.args.get("id"):
            bill = Billing.query.filter_by(id=request.args.get("id")).first()
            db.session.delete(bill)
            db.session.commit()
            return redirect(url_for("billing"))
        
        return render_template("backend/bill/createbill.html", bill=bill)
       
    if request.args.get("action") == "details":
        customer = request.form.get("customer_name")
        pattern = r"[0-9]"
        customers = re.sub(pattern, "", customer)
        customerid = customer.replace(" ", "")
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        m = r.match(customerid)
        id = m.group(2)
        details = CustomerUser.query.filter_by(id=id).first()
        todays_date = date.today()
        # rand = str(random.randint(6666, 9999))
        # print(type(ran))
        # year = todays_date.year
        # print(type(year))
        # newyear = str(year)
        # rand = str(ran)
        invno = "INV"+ str(todays_date.year) + str(random.randint(6666, 9999))
        ordno = "ORD"+ str(todays_date.month) + str(random.randint(6666, 9999))
        data = {
            "success": True,
            "address": str(details.address),
            "pan": str(details.pan),
            "gstin": str(details.gstin),
            "invno": invno,
            "ordno": ordno,

        }
        return jsonify(data)
    
    if request.args.get("action") == "calculate":
        # for x in range(1, 11):
        #     print(x)
        #     # b = str("qty_",x)
        #     # b = str(x)
        #     # c = str("qty_") + b
        #     # print("qty_x",float(request.form.get("qty_1")))
        #     qty_n = float(request.form.get(str("qty_") + str(x)))
        #     rate_n = float(request.form.get(str("rate_") + str(x)))
        #     amount_n ="amount_" + str(x)
        #     amount_n = qty_n * rate_n
        qty_1 = float(request.form.get("qty_1"))
        rate_1 = float(request.form.get("rate_1"))
        amount_1 = qty_1 * rate_1
        
        qty_2 = float(request.form.get("qty_2"))
        rate_2 = float(request.form.get("rate_2"))
        amount_2 = qty_2 * rate_2
        
        qty_3 = float(request.form.get("qty_3"))
        rate_3 = float(request.form.get("rate_3"))
        amount_3 = qty_3 * rate_3
        
        qty_4 = float(request.form.get("qty_4"))
        rate_4 = float(request.form.get("rate_4"))
        amount_4 = qty_4 * rate_4
        
        qty_5 = float(request.form.get("qty_5"))
        rate_5 = float(request.form.get("rate_5"))
        amount_5 = qty_5 * rate_5
        
        qty_6 = float(request.form.get("qty_6"))
        rate_6 = float(request.form.get("rate_6"))
        amount_6 = qty_6 * rate_6
        
        qty_7 = float(request.form.get("qty_7"))
        rate_7 = float(request.form.get("rate_7"))
        amount_7 = qty_7 * rate_7
        
        qty_8 = float(request.form.get("qty_8"))
        rate_8 = float(request.form.get("rate_8"))
        amount_8 = qty_8 * rate_8
        
        qty_9 = float(request.form.get("qty_9"))
        rate_9 = float(request.form.get("rate_9"))
        amount_9 = qty_9 * rate_9
        
        qty_10 = float(request.form.get("qty_10"))
        rate_10 = float(request.form.get("rate_10"))
        amount_10 = qty_10 * rate_10
        total = amount_1+amount_2+amount_3+amount_4+amount_5+amount_6+amount_7+amount_8+amount_9+amount_10
        data = {
            "success": True,
            "amount_1": str(amount_1),
            "amount_2": str(amount_2),
            "amount_3": str(amount_3),
            "amount_4": str(amount_4),
            "amount_5": str(amount_5),
            "amount_6": str(amount_6),
            "amount_7": str(amount_7),
            "amount_8": str(amount_8),
            "amount_9": str(amount_9),
            "amount_10": str(amount_10),
            "total": str(total),
        }
        # print(x)
        return jsonify(data)
    
    if request.args.get("action") == "gst":
        gst = float(request.form.get("gst"))
        print(type(request.form.get("gst")))
        print(type(request.form.get("total")))
        total = float(request.form.get("total"))
        gstper = total * (gst / 100)
        result = total + gstper
        print(result)
        data = {
            "success": True,
            "result": str(result),
        }
        # print(x)
        return jsonify(data)
    
    # customer = CustomerUser.query.all()
    bill = Billing.query.all()
    return render_template("backend/bill/billing.html", bill=bill)


# @app.route("/settings/")
# @login_required
# def settings():
#     company = Company.query.filter_by(id=request.args.get("id")).first()
#     company.email = request.form.get("email")
#     company.pan = request.form.get("pan")
#     company.gistin = request.form.get("gistin")
#     company.address = request.form.get("address")
#     company.city = request.form.get("city")
#     company.pin = request.form.get("pin")
#     company.state = request.form.get("state")
#     company.country = request.form.get("country")
#     db.session.commit()
#     return render_template("backend/settings/settings.html")


@app.route("/trips/", methods=["POST", "GET"])
@login_required
def trips():
    if request.args.get("q") == "nrl":
        if request.args.get("action") == "add":
            if request.method == "POST":
                nrl = NrlUser(
                    loadingdate=request.form.get("loadingdate"),
                    ttno=request.form.get("ttno"),
                    shipmentno=request.form.get("shipmentno"),
                    qty=request.form.get("qty"),
                    shortage=request.form.get("shortage"),
                    unloadingdate=request.form.get("unloadingdate"),
                    unloadingqty=request.form.get("unloadingqty"),
                    rate=request.form.get("rate"),
                    destination=request.form.get("destination"),
                    toll=request.form["toll"],
                    totalamount=request.form.get("totalamount"),
                    shortageamount=request.form.get("shortageamount"),
                    product=request.form.get("product"),
                    status=request.form.get("status"),
                )
                db.session.add(nrl)
                db.session.commit()
                return redirect("/trips/?q=nrl")
            vehicle = VehicleUser.query.all()
            return render_template("backend/trip/nrl/addnrl.html", vehicle=vehicle)
        

        if request.args.get("action") == "edit":
            if request.args.get("id"):
                if request.args.get("n") == "store":
                    nrl = NrlUser.query.filter_by(id=request.args.get("id")).first()
                    nrl.loadingdate = request.form.get("loadingdate")
                    nrl.ttno = request.form.get("ttno")
                    nrl.shipmentno = request.form.get("shipmentno")
                    nrl.qty = request.form.get("qty")
                    nrl.shortage = request.form.get("shortage")
                    nrl.unloadingdate = request.form.get("unloadingdate")
                    nrl.unloadingqty = request.form.get("unloadingqty")
                    nrl.rate = request.form.get("rate")
                    nrl.destination = request.form.get("destination")
                    nrl.toll = request.form.get("toll")
                    nrl.totalamount = request.form.get("totalamount")
                    nrl.shortageamount = request.form.get("shortageamount")
                    nrl.product = request.form.get("product")
                    nrl.status = request.form.get("status")
                    db.session.commit()
                    return redirect("/trips/?q=nrl")
                else:
                    nrl = NrlUser.query.filter_by(id=request.args.get("id")).all()
                    vehicle = VehicleUser.query.all()
                    return render_template("backend/trip/nrl/updatenrl.html", vehicle=vehicle, nrl=nrl)
                        

        if request.args.get("action") == "delete":
            if request.args.get("id"):
                nrl = NrlUser.query.filter_by(id=request.args.get("id")).first()
                db.session.delete(nrl)
                db.session.commit()
                return redirect("/trips/?q=nrl")
        
        nrl = NrlUser.query.all()
        return render_template("backend/trip/nrl/nrl.html", nrl=nrl)
    

    if request.args.get("q") == "acid":
        if request.args.get("action") == "add":
            # print("hello")
            if request.method == "POST":
                # print("joy")
                # print(request.form.get("product"))
                acid = AcidUser(
                    loadingdate=request.form.get("loadingdate"),
                    ttno=request.form.get("ttno"),
                    product=request.form.get("product"),
                    loadedat=request.form.get("loadedat"),
                    destination=request.form.get("destination"),
                    lrno=request.form.get("lrno"),
                    invoice=request.form.get("invoice"),
                    loadqty=request.form.get("loadqty"),
                    shortage=request.form.get("shortage"),
                    unloadingdate=request.form["unloadingdate"],
                    unloadingqty=request.form.get("unloadingqty"),
                    helperunload=request.form.get("helperunload"),
                    hsdqty=request.form.get("hsdqty"),
                    advcash=request.form.get("advcash"),
                    totaladv=request.form.get("totaladv"),
                    billingrate=request.form.get("billingrate"),
                    totalamount=request.form.get("totalamount"),
                    status=request.form.get("status"),
                )
                db.session.add(acid)
                db.session.commit()
                return redirect("/trips/?q=acid")
                # return redirect(url_for("trips"))
            vehicle = VehicleUser.query.all()
            return render_template("backend/trip/acid/addacid.html", vehicle=vehicle)
        
        # if request.args.get("action") == "update":
        #     if request.args.get("id"):
        #         acid = AcidUser.query.filter_by(id=request.args.get("id")).all()
        #         vehicle = VehicleUser.query.all()
        #         return render_template("backend/trip/acid/addacid.html", vehicle=vehicle, acid=acid)

        # return redirect(url_for("/trips/"))

        if request.args.get("action") == "edit":
            if request.args.get("id"):
                if request.args.get("n") == "store":
                    acid = AcidUser.query.filter_by(id=request.args.get("id")).first()
                    acid.loadingdate = request.form.get("loadingdate")
                    acid.ttno = request.form.get("ttno")
                    acid.product = request.form.get("product")
                    acid.loadedat = request.form.get("loadedat")
                    acid.destination = request.form.get("destination")
                    acid.lrno = request.form.get("lrno")
                    acid.invoice = request.form.get("invoice")
                    acid.loadqty = request.form.get("loadqty")
                    acid.shortage = request.form.get("shortage")
                    acid.unloadingdate = request.form.get("unloadingdate")
                    acid.unloadingqty = request.form.get("unloadingqty")
                    acid.helperunload = request.form.get("helperunload")
                    acid.hsdqty = request.form.get("hsdqty")
                    acid.advcash = request.form.get("advcash")
                    acid.totaladv = request.form.get("totaladv")
                    acid.billingrate = request.form.get("billingrate")
                    acid.totalamount = request.form.get("totalamount")
                    acid.status = request.form.get("status")
                    db.session.commit()
                    
                    return redirect("/trips/?q=acid")
                else:
                    acid = AcidUser.query.filter_by(id=request.args.get("id")).all()
                    vehicle = VehicleUser.query.all()
                    return render_template("backend/trip/acid/updateacid.html", vehicle=vehicle, acid=acid)
                
        # if request.args.get("action") == "update":
        #     if request.args.get("id"):
        #         acid = AcidUser.query.filter_by(id=request.args.get("id")).all()
        #         vehicle = VehicleUser.query.all()
        #         return render_template("backend/trip/acid/updateacid.html", vehicle=vehicle, acid=acid)

            # vehicle = VehicleUser.query.all()
            # acid = AcidUser.query.all()
            # return render_template("backend/trip/acid/updateacid.html", vehicle=vehicle, acid=acid)
        # acid = AcidUser.query.all()
        # return render_template("backend/trip/acid/acid.html", acid=acid)
        

        if request.args.get("action") == "delete":
            if request.args.get("id"):
                acid = AcidUser.query.filter_by(id=request.args.get("id")).first()
                db.session.delete(acid)
                db.session.commit()
                return redirect("/trips/?q=acid")
                # return redirect(url_for("trips"))
                # acid = AcidUser.query.all()
                # return render_template("backend/trip/acid/acid.html")
        
        acid = AcidUser.query.all()
        return render_template("backend/trip/acid/acid.html", acid=acid)

    # vehicle = VehicleUser.query.all()
    nrl = NrlUser.query.all()
    acid = AcidUser.query.all()
    return render_template("backend/trip/trips.html", nrl=nrl, acid=acid)


# SIGNUP --------------------------------------------------------------------


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        passwordshow = request.form["password"]
        a_string = str(request.form["password"])
        length = len(a_string)
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            return jsonify(
                success=False,
                msg="This User Id already RegistRegisterderd",
                url="register",
            )
        else:
            if length >= 4:
                if request.form["password"] == request.form["confirmpassword"]:
                    hashed_password = generate_password_hash(request.form["password"])
                    password = hashed_password
                    my_data = User(
                        email,
                        password,
                        passwordshow,
                        name="none",
                        phone="none",
                        is_superuser="1",
                        is_user="0",
                        approval="0",
                        is_active="none",
                    )
                    db.session.add(my_data)
                    db.session.commit()
                    return jsonify(
                        success=True,
                        msg="You have successfully register",
                        url="login",
                    )
                else:
                    return jsonify(success=False, msg="Password does not match")
            else:
                return jsonify(success=False, msg="Please Enter Minimum Four Character")
    return render_template("backend/login/signup.html")


if __name__ == "__main__":
    # app.run(debug=True, host="143.110.241.63", port=80)
    app.run(debug=True)