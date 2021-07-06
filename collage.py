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

import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "transport!"

# For PostgreSQL
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://nandan:nandan2537@@localhost:5432/transport"

db = SQLAlchemy(app)
app.secret_key = "Secret Key"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)

# app = Flask(__name__)
# app.config["SECRET_KEY"] = "tradianautotrade!"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/nandan/Music/pictures/TRANSPORT/database.db"

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
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(450))
    passwordshow = db.Column(db.String(80))
    name = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(50), nullable=True, default="None")
    is_superuser = db.Column(db.String(50), nullable=True, default="None")
    is_user = db.Column(db.String(50), nullable=True, default="None")
    is_staff = db.Column(db.String(50), nullable=True, default="None")
    is_active = db.Column(db.String(50), nullable=True, default="True")

    def __init__(
        self,
        email,
        password,
        passwordshow,
        name,
        phone,
        is_superuser,
        is_user,
        is_staff,
        is_active,
    ):

        self.email = email
        self.password = password
        self.passwordshow = passwordshow
        self.name = name
        self.phone = phone
        self.is_superuser = is_superuser
        self.is_user = is_user
        self.is_staff = is_staff
        self.is_active = is_active


# VEHICLES -------------------------------------------------------------


# class Vehicle(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     date = db.DateField(default=datetime.date.today)
#     supplier = db.ForeignKey(CustomUser, on_delete=db.CASCADE)
#     vehicle_name = db.CharField(max_length=50, null=True)
#     vehicle_type = db.CharField(max_length=50, null=True)
#     dimension = db.CharField(max_length=30, null=True)
#     weight_capacity = db.CharField(max_length=30, null=True)
#     ground_clearance = db.CharField(max_length=30, null=True)
#     make_model = db.CharField(max_length=30, null=True)
#     yom = db.CharField(max_length=20, null=True)
#     color = db.CharField(max_length=20, null=True)
#     reg_no = db.CharField(max_length=20, null=True)
#     engine_no = db.CharField(max_length=20, null=True)
#     chassis_no = db.CharField(max_length=20, null=True)
#     fuel_type = db.CharField(max_length=20, null=True)
#     fuel_measurement = db.CharField(max_length=20, null=True)
#     track_usage = db.CharField(max_length=20, null=True)
#     status = db.BooleanField(default=True)

#     def __init__(
#         self,
#         id,
#         company,
#         date,
#         supplier,
#         vehicle_name,
#         vehicle_type,
#         dimension,
#         weight_capacity,
#         ground_clearance,
#         make_model,
#         yom,
#         color,
#         reg_no,
#         engine_no,
#         chassis_no,
#         fuel_type,
#         fuel_measurement,
#         track_usage,
#         status,
#     ):
#         self.id = id
#         self.company = company
#         self.supplier = supplier
#         self.vehicle_name = vehicle_name
#         self.vehicle_type = vehicle_type
#         self.dimension = dimension
#         self.weight_capacity = weight_capacity
#         self.ground_clearance = ground_clearance
#         self.make_model = make_model
#         self.yom = yom
#         self.color = color
#         self.reg_no = reg_no
#         self.engine_no = engine_no
#         self.chassis_no = chassis_no
#         self.fuel_type = fuel_type
#         self.fuel_measurement = fuel_measurement
#         self.track_usage = track_usage
#         self.status = status


class Company(UserMixin, db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    showpassword = db.Column(db.String(50), nullable=False)
    created = db.Column(db.Date, nullable=True, default=date.today())
    pan = db.Column(db.String(50), nullable=False)
    gistin = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False, default="None")
    city = db.Column(db.String(50), nullable=False, default="None")
    pin = db.Column(db.String(50), nullable=False, default="None")
    state = db.Column(db.String(50), nullable=False, default="None")
    country = db.Column(db.String(50), nullable=False, default="None")
    status = db.Column(db.String(50), nullable=False, default="True")
    approval = db.Column(db.String(50), nullable=True, default="True")

    def __init__(
        self,
        name,
        email,
        password,
        showpassword,
        pan,
        gistin,
        address,
        city,
        pin,
        state,
        country,
        status,
        approval,
    ):
        self.name = name
        self.email = email
        self.password = password
        self.showpassword = showpassword
        self.pan = pan
        self.gistin = gistin
        self.address = address
        self.city = city
        self.pin = pin
        self.state = state
        self.country = country
        self.status = status
        self.approval = approval


# # FUEL --------------------------------------------------------------


# class Fuel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     supplier = db.ForeignKey(CustomUser, on_delete=db.CASCADE)
#     vehicle = db.ForeignKey(Vehicle, on_delete=db.CASCADE)
#     slip_no = db.CharField(max_length=30, null=True)
#     slip_date = db.DateField(default=datetime.date.today)
#     recived_date = db.DateField(default=datetime.date.today)
#     qty = db.FloatField(null=True, default=0.0)
#     rate = db.FloatField(null=True, default=0.0)
#     amount = db.FloatField(null=True, default=0.0)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         supplier,
#         vehicle,
#         slip_no,
#         slip_date,
#         recived_date,
#         qty,
#         rate,
#         amount,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.supplier = supplier
#         self.vehicle = vehicle
#         self.slip_no = slip_no
#         self.slip_date = slip_date
#         self.recived_date = recived_date
#         self.qty = qty
#         self.rate = rate
#         self.amount = amount


# # BILLING -----------------------------------------------------------


# class Billing(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     service_recever = db.CharField(max_length=30, null=True)
#     address = db.TextField(null=True)
#     pannumber = db.CharField(max_length=20, null=True)
#     gstin = db.CharField(max_length=30, null=True)
#     inv_no = db.CharField(max_length=30, null=True)
#     inv_date = db.DateField(default=datetime.date.today)
#     job_date = db.DateField(null=True)
#     comp_date = db.DateField(null=True)
#     order_no = db.CharField(max_length=30, null=True)
#     order_date = db.DateField(null=True)
#     payble = db.FloatField(null=True, default=0.0)
#     due = db.FloatField(null=True, default=0.0)
#     gst_rate = db.FloatField(null=True, default=0.0)
#     sgst = db.FloatField(null=True)
#     cgst = db.FloatField(null=True)
#     igst = db.FloatField(null=True)
#     inwords = db.TextField(null=True)
#     status = db.BooleanField(default=False)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         service_recever,
#         address,
#         pannumber,
#         gstin,
#         inv_no,
#         inv_date,
#         job_date,
#         comp_date,
#         order_no,
#         order_date,
#         payble,
#         due,
#         gst_rate,
#         sgst,
#         cgst,
#         igst,
#         inwords,
#         status,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.service_recever = service_recever
#         self.address = address
#         self.pannumber = pannumber
#         self.gstin = gstin
#         self.inv_no = inv_no
#         self.inv_date = inv_date
#         self.job_date = job_date
#         self.comp_date = comp_date
#         self.order_no = order_no
#         self.order_date = order_date
#         self.payble = payble
#         self.due = due
#         self.gst_rate = gst_rate
#         self.sgst = sgst
#         self.cgst = cgst
#         self.igst = igst
#         self.inwords = inwords
#         self.status = status


# # TRIPS ----------------------------------------------------------------


# class Trip_Nrl(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     loading_date = db.DateField(default=datetime.date.today)
#     vehicle = db.ForeignKey(Vehicle, on_delete=db.CASCADE)
#     shipment_no = db.CharField(max_length=100, null=True)
#     qty_mt = db.FloatField(null=True)
#     shortage = db.IntegerField(null=True)
#     unloading_date = db.DateField(null=True)
#     unloading_qty = db.FloatField(null=True)
#     rate = db.FloatField(null=True)
#     distance = db.FloatField(null=True)
#     toll = db.FloatField(null=True)
#     total_amount = db.FloatField(null=True)
#     shortage_amount = db.FloatField(null=True)
#     product = db.CharField(max_length=30, null=True)
#     billed = db.BooleanField(default=False)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         loading_date,
#         vehicle,
#         shipment_no,
#         qty_mt,
#         shortage,
#         unloading_date,
#         unloading_qty,
#         rate,
#         distance,
#         toll,
#         total_amount,
#         shortage_amount,
#         product,
#         billed,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.loading_date = loading_date
#         self.vehicle = vehicle
#         self.shipment_no = shipment_no
#         self.qty_mt = qty_mt
#         self.shortage = shortage
#         self.unloading_date = unloading_date
#         self.unloading_qty = unloading_qty
#         self.rate = rate
#         self.distance = distance
#         self.toll = toll
#         self.total_amount = total_amount
#         self.shortage_amount = shortage_amount
#         self.product = product
#         self.billed = billed


# class Trip_Acid(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     loading_date = db.DateField(default=datetime.date.today)
#     vehicle = db.ForeignKey(Vehicle, on_delete=db.CASCADE)
#     product = db.CharField(max_length=30, null=True)
#     loaded_at = db.CharField(max_length=50, null=True)
#     destination = db.CharField(max_length=50, null=True)
#     lr_no = db.IntegerField(null=True)
#     invoice_no = db.CharField(max_length=100, null=True)
#     load_qty_mt = db.FloatField(null=True)
#     shortage = db.IntegerField(null=True)
#     unloading_date = db.DateField(null=True)
#     unloading_qty = db.FloatField(null=True)
#     helper_unload = db.FloatField(null=True)
#     hsd_qty = db.FloatField(null=True)
#     adv_cash = db.FloatField(null=True)
#     total_adv = db.FloatField(null=True)
#     billing_rate = db.FloatField(null=True)
#     billed_amount = db.FloatField(null=True)
#     billed = db.BooleanField(default=False)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         loading_date,
#         vehicle,
#         product,
#         loaded_at,
#         destination,
#         lr_no,
#         invoice_no,
#         load_qty_mt,
#         shortage,
#         unloading_date,
#         unloading_qty,
#         helper_unload,
#         hsd_qty,
#         adv_cash,
#         total_adv,
#         billing_rate,
#         billed_amount,
#         billed,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.loading_date = loading_date
#         self.vehicle = vehicle
#         self.product = product
#         self.loaded_at = loaded_at
#         self.destination = destination
#         self.lr_no = lr_no
#         self.invoice_no = invoice_no
#         self.load_qty_mt = load_qty_mt
#         self.shortage = shortage
#         self.unloading_date = unloading_date
#         self.unloading_qty = unloading_qty
#         self.helper_unload = helper_unload
#         self.hsd_qty = hsd_qty
#         self.adv_cash = adv_cash
#         self.total_adv = total_adv
#         self.billing_rate = billing_rate
#         self.billed_amount = billed_amount
#         self.billed = billed


# class Trip_Fcl(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     loading_date = db.DateField(default=datetime.date.today)
#     vehicle = db.ForeignKey(Vehicle, on_delete=db.CASCADE)
#     deport = db.CharField(max_length=50, null=True)
#     destination_sp = db.CharField(max_length=50, null=True)
#     destination = db.CharField(max_length=50, null=True)
#     unloading_date = db.DateField(null=True)
#     billing_doc = db.CharField(max_length=100, null=True)
#     material = db.CharField(max_length=30, null=True)
#     kl = db.IntegerField(null=True)
#     km = db.IntegerField(null=True)
#     hsd_1 = db.IntegerField(null=True)
#     hsd = db.IntegerField(null=True)
#     card = db.FloatField(null=True)
#     ct_toll = db.FloatField(null=True)
#     cash = db.FloatField(null=True)
#     supply_fooding = db.FloatField(null=True)
#     supply_toll_tax = db.FloatField(null=True)
#     kanta = db.FloatField(null=True)
#     entery = db.FloatField(null=True)
#     repairing = db.FloatField(null=True)
#     toll = db.FloatField(null=True)
#     mech = db.FloatField(null=True)
#     union = db.FloatField(null=True)
#     total = db.FloatField(null=True)
#     ltr = db.FloatField(null=True)
#     shortage = db.FloatField(null=True)
#     ltr_1 = db.FloatField(null=True)
#     product = db.CharField(max_length=30, null=True)
#     rate = db.FloatField(null=True)
#     billed = db.BooleanField(default=False)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         loading_date,
#         vehicle,
#         deport,
#         destination_sp,
#         destination,
#         unloading_date,
#         billing_doc,
#         material,
#         kl,
#         km,
#         hsd_1,
#         hsd,
#         card,
#         ct_toll,
#         cash,
#         supply_fooding,
#         supply_toll_tax,
#         kanta,
#         entery,
#         repairing,
#         toll,
#         mech,
#         union,
#         total,
#         ltr,
#         shortage,
#         ltr_1,
#         product,
#         rate,
#         billed,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.loading_date = loading_
#         self.vehicle = vehicle
#         self.deport = deport
#         self.destination_sp = destination_sp
#         self.destination = destination
#         self.unloading_date = unloading_date
#         self.billing_doc = billing_doc
#         self.material = material
#         self.kl = kl
#         self.km = km
#         self.hsd_1 = hsd_1
#         self.hsd = hsd
#         self.card = card
#         self.ct_toll = ct_toll
#         self.cash = cash
#         self.supply_fooding = supply_fooding
#         self.supply_toll_tax = supply_toll_tax
#         self.kanta = kanta
#         self.entery = entery
#         self.repairing = repairing
#         self.toll = toll
#         self.mech = mech
#         self.union = union
#         self.total = total
#         self.ltr = ltr
#         self.shortage = shortage
#         self.ltr_1 = ltr_1
#         self.product = product
#         self.rate = rate
#         self.billed = billed


# class Trip_Bpcl(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     date = db.DateField(default=datetime.date.today)
#     vehicle = db.ForeignKey(Vehicle, on_delete=db.CASCADE)
#     destination = db.CharField(max_length=50, null=True)
#     supply_pump = db.CharField(max_length=100, null=True)
#     supply_km = db.IntegerField(null=True)
#     capacity_kl = db.IntegerField(null=True)
#     supply_fa = db.IntegerField(null=True)
#     km = db.IntegerField(null=True)
#     rate = db.FloatField(null=True)
#     freight_amt = db.FloatField(null=True)
#     recived_payment = db.FloatField(null=True)
#     diffn = db.FloatField(null=True)
#     short = db.FloatField(null=True)
#     hsd_ltr = db.FloatField(null=True)
#     fuel_rs = db.FloatField(null=True)
#     cash_adv = db.FloatField(null=True)
#     total_exp = db.FloatField(null=True)
#     chalan = db.FloatField(null=True)
#     # company = db.FloatField(null=True)
#     invoice_no = db.CharField(max_length=100, null=True)
#     shipment_no = db.CharField(max_length=100, null=True)
#     challan_rcv_date = db.DateField(null=True)
#     short_1 = db.FloatField(null=True)
#     actual_toll = db.FloatField(null=True)
#     short_recovery = db.FloatField(null=True)
#     billed = db.BooleanField(default=False)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         date,
#         vehicle,
#         destination,
#         supply_pump,
#         supply_km,
#         capacity_kl,
#         supply_fa,
#         km,
#         rate,
#         freight_amt,
#         recived_payment,
#         diffn,
#         short,
#         hsd_ltr,
#         fuel_rs,
#         cash_adv,
#         total_exp,
#         chalan,
#         invoice_no,
#         shipment_no,
#         challan_rcv_date,
#         short_1,
#         actual_toll,
#         short_recovery,
#         billed,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.date = date
#         self.vehicle = vehicle
#         self.destination = destination
#         self.supply_pump = supply_pump
#         self.supply_km = supply_km
#         self.capacity_kl = capacity_kl
#         self.supply_fa = supply_fa
#         self.km = km
#         self.rate = rate
#         self.freight_amt = freight_amt
#         self.recived_payment = recived_payment
#         self.diffn = diffn
#         self.short = short
#         self.hsd_ltr = hsd_ltr
#         self.fuel_rs = fuel_rs
#         self.cash_adv = cash_adv
#         self.total_exp = total_exp
#         self.chalan = chalan
#         # self.company = company
#         self.invoice_no = invoice_no
#         self.shipment_no = shipment_no
#         self.challan_rcv_date = challan_rcv_date
#         self.short_1 = short_1
#         self.actual_toll = actual_toll
#         self.short_recovery = short_recovery
#         self.billed = billed


# # ACCOUNTING -----------------------------------------------------------


# class Accounts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.CharField(max_length=30, null=True)

#     def __init__(self, id, name):
#         self.id = id
#         self.name = name


# # SERVICES ----------------------------------------------------------------


# class Service(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     journal = db.ForeignKey(Journal, on_delete=db.CASCADE, null=True)
#     vehicle = db.ForeignKey(Vehicle, on_delete=db.CASCADE)
#     service_on = db.DateField(default=datetime.date.today)
#     odometer = db.CharField(max_length=30, null=True)
#     labor = db.FloatField(null=True, default=0.0)
#     parts = db.FloatField(null=True, default=0.0)
#     tax = db.FloatField(null=True, default=0.0)
#     total = db.FloatField(null=True, default=0.0)
#     inv_no = db.CharField(max_length=30, null=True)

#     def __init__(
#         self,
#         id,
#         company,
#         journal,
#         vehicle,
#         service_on,
#         odometer,
#         labor,
#         parts,
#         tax,
#         total,
#         inv_no,
#     ):
#         self.id = id
#         self.company = company
#         self.journal = journal
#         self.vehicle = vehicle
#         self.service_on = service_on
#         self.odometer = odometer
#         self.labor = labor
#         self.parts = parts
#         self.tax = tax
#         self.total = total
#         self.inv_no = inv_no


# # GST ----------------------------------------------------------


# class Billing_table(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     billing = db.ForeignKey(Billing, on_delete=db.CASCADE)
#     description = db.TextField(null=True)
#     hsn_sac = db.CharField(max_length=30, null=True)
#     qty = db.FloatField(null=True, default=0.0)
#     rate = db.FloatField(null=True, default=0.0)
#     amount = db.FloatField(null=True, default=0.0)

#     def __init__(self, id, company, billing, description, hsn_sac, qty, rate, amount):
#         self.id = id
#         self.company = company
#         self.billing = billing
#         self.description = description
#         self.hsn_sac = hsn_sac
#         self.qty = qty
#         self.rate = rate
#         self.amount = amount


# # COMPANY_MATER --------------------------------------------------


# class Journal(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     j_id = db.IntegerField(null=True)
#     j_type = db.CharField(max_length=20, null=True)
#     date = db.DateField(default=datetime.date.today)
#     company = db.ForeignKey(Company, on_delete=db.CASCADE)
#     account = db.ForeignKey(Accounts, on_delete=db.CASCADE)
#     service_recever = db.CharField(max_length=50, null=True)
#     amount = db.FloatField(null=True, default=0.0)
#     credit = db.BooleanField(default=False)
#     debit = db.BooleanField(default=False)
#     refno = db.CharField(max_length=30, null=True)

#     def __init__(
#         self,
#         id,
#         j_id,
#         j_type,
#         date,
#         company,
#         account,
#         service_recever,
#         amount,
#         credit,
#         debit,
#         refno,
#     ):
#         self.id = id
#         self.j_id = j_id
#         self.j_type = j_type
#         self.date = date
#         self.company = company
#         self.account = account
#         self.service_recever = service_recever
#         self.amount = amount
#         self.credit = credit
#         self.debit = debit
#         self.refno = refno


# # CUSTOMER_USER ----------------------------------------------------------------


class CustomUser(db.Model):
    # company = db.ForeignKey(Company, on_delete=db.CASCADE, null=True)
    # is_admin = db.BooleanField(default=False)
    # is_customer = db.BooleanField(default=False)
    # is_supplier = db.BooleanField(default=False)
    # pword = db.CharField(max_length=20, null=True)
    id = db.Column(db.Integer, primary_key=True) 
    gstin_number = db.Column(db.String(50), nullable=True)
    pan_number = db.Column(db.String(50), nullable=True)
    mobile = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50),nullable=True)
    city = db.Column(db.String(50), nullable=True)
    pin = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    # otp = db.CharField(max_length=10, null=True)

    def __init__(
        self,
        # company,
        # is_admin,
        # is_customer,
        # is_supplier,
        # pword,
        gstin_number,
        pan_number,
        mobile,
        address,
        city,
        pin,
        state,
        country,
        # otp,
    ):
        # self.company = company
        # self.is_admin = is_admin
        # self.is_customer = is_customer
        # self.is_supplier = is_supplier
        # self.pword = pword
        self.gstin_number = gstin_number
        self.pan_number = pan_number
        self.mobile = mobile
        self.address = address
        self.city = city
        self.pin = pin
        self.state = state
        self.country = country
        # self.otp = otp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @login_manager.user_loader
# def load_company(user_id):
#     return Company.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("backend/login/login2.html")


# @app.route("/login/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         user = User.query.filter_by(email=request.values.get("email")).first()
#         if user:
#             if check_password_hash(user.password, request.values.get("password")):
#                 login_user(user)
#                 db.session.commit()
#                 return jsonify(
#                     success=True, msg="You have successfully logged in", url="dashboard"
#                 )
#             else:
#                 return jsonify(success=False, msg="Incorrect password")
#         else:
#             return jsonify(success=False, msg="Invalid email or password")
#     return render_template("backend/login/login2.html")


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
            company = Company(
                name=request.form.get("name"),
                email=request.form.get("email"),
                password=generate_password_hash(request.form.get("password")),
                showpassword=request.form.get("password"),
                pan="",
                address=request.form.get("address"),
                city="",
                pin="",
                state="",
                country="",
                status="True",
                approval="True",
                gistin="",
            )
            db.session.add(company)
            db.session.commit()
            # return jsonify(success=True, url="pharmacy")
            return redirect(url_for("superuser"))
    if request.args.get("action") == "dashboard":
        if request.args.get("id"):
            company = Company.query.filter_by(id=request.args.get("id"))
            return render_template("backend/index.html", company=company)
    company = Company.query.all()
    return render_template("backend/superuser.html", company=company)


# ------------------------------------------------------------------------


@app.route("/customers/", methods=["POST", "GET"])
@login_required
def customers():
    if request.args.get("action") == "add":
        if request.method == "POST":
            customer = CustomUser(
                
                gstin_number=request.form.get("gstin_number"),
                pan_number=request.form.get("pan_number"),
                mobile=request.form.get("mobile"),
                address=request.form.get("address"),
                city=request.form.get("city"),
                pin=request.form.get("pin"),
                state=request.form.get("state"),
                country=request.form.get("country"),
            )
            db.session.add(customer)
            db.session.commit()
            # return jsonify(success=True, url="pharmacy")
            return redirect(url_for("customers"))
        return render_template("backend/customer/addcustomer.html")
    customer=CustomUser.query.all()
    return render_template("backend/customer/customers.html", customer=customer)


@app.route("/suppliers/")
@login_required
def suppliers():
    if request.args.get("action") == "add":
        return render_template("backend/supplier/addsupplier.html")
        pass
    return render_template("backend/supplier/suppliers.html")


@app.route("/vehicles/")
@login_required
def vehicles():
    if request.args.get("action") == "add":
        return render_template("backend/vehicle/addvehicle.html")
        pass
    return render_template("backend/vehicle/vehicles.html")


@app.route("/fuel/")
@login_required
def fuel():
    if request.args.get("action") == "add":
        return render_template("backend/fuel/addfuel.html")
        pass
    return render_template("backend/fuel/fuel.html")


@app.route("/billing/")
@login_required
def billing():
    if request.args.get("action") == "add":
        return render_template("backend/bill/createbill.html")
        pass
    return render_template("backend/bill/billing.html")


@app.route("/accounting/")
@login_required
def accounting():
    if request.args.get("action") == "add":
        return render_template("backend/accounting/addaccounting.html")
        pass
    return render_template("backend/accounting/accounting.html")


@app.route("/services/")
@login_required
def services():
    if request.args.get("action") == "add":
        return render_template("backend/service/addservice.html")
        pass
    return render_template("backend/service/services.html")


@app.route("/gst/")
@login_required
def gst():
    return render_template("backend/bill/gst.html")


@app.route("/company-master/")
@login_required
def companymaster():
    return render_template("backend/companymaster/company-master.html")


# SETTINGS -------------------------------------------------------------------


@app.route("/settings/")
@login_required
def settings():
    return render_template("backend/settings/settings.html")


@app.route("/user/")
@login_required
def user():
    if request.args.get("action") == "edit":
        return render_template("backend/user/edit.html")
        pass
    return render_template("backend/user/user.html")


@app.route("/trips/")
@login_required
def trips():
    if request.args.get("q") == "nrl":
        if request.args.get("action") == "add":
            return render_template("backend/trip/nrl/addnrl.html")
        if request.args.get("action") == "edit":
            if request.args.get("id"):
                pass
        if request.args.get("action") == "delete":
            if request.args.get("id"):
                pass
        return render_template("backend/trip/nrl/nrl.html")
    if request.args.get("q") == "bpcl":
        if request.args.get("action") == "add":
            return render_template("backend/trip/bpcl/addbpcl.html")
        if request.args.get("action") == "edit":
            if request.args.get("id"):
                pass
        if request.args.get("action") == "delete":
            if request.args.get("id"):
                pass
        return render_template("backend/trip/bpcl/bpcl.html")
    if request.args.get("q") == "acid":
        if request.args.get("action") == "add":
            return render_template("backend/trip/acid/addacid.html")
        if request.args.get("action") == "edit":
            if request.args.get("id"):
                pass
        if request.args.get("action") == "delete":
            if request.args.get("id"):
                pass
        return render_template("backend/trip/acid/acid.html")
    if request.args.get("q") == "fcl":
        if request.args.get("action") == "add":
            return render_template("backend/trip/fcl/addfcl.html")
        if request.args.get("action") == "edit":
            if request.args.get("id"):
                pass
        if request.args.get("action") == "delete":
            if request.args.get("id"):
                pass
        return render_template("backend/trip/fcl/fcl.html")
    return render_template("backend/trip/trips.html")


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
                        is_superuser="none",
                        is_user="none",
                        is_staff="none",
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