from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ghbdtnsql@127.0.0.1/ygolek'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_address = db.Column(db.String(100))


class Supplier(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class CoalBrand(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    price_per_ton = db.Column(db.Numeric(10, 2), nullable=False)

    supplier = db.relationship('Supplier', backref=db.backref('coal_brands', lazy=True))


class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coal_brand_id = db.Column(db.Integer, db.ForeignKey('coal_brand.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    coal_brand = db.relationship('CoalBrand', backref=db.backref('orders', lazy=True))
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))


# Создаем контекст приложения
with app.app_context():
    # Создаем таблицы в базе данных
    db.create_all()

# главная страница
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


# О нас страница
@app.route('/about')
def about():
    return render_template("about.html")


# контакты страница
@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':  # Если метод запроса - POST
        user = User.query.filter_by(email=request.form['email']).first()  # Проверяем, существует ли пользователь с указанным email
        if not user:  # Если пользователя нет, создаем нового пользователя
            user = User(
                name=request.form['name'],
                email=request.form['email'],
                password=generate_password_hash(request.form['password'], method='sha256'),
                last_address=request.form['address']
            )
            db.session.add(user)  # Добавляем пользователя в базу данных
            db.session.commit()  # Сохраняем изменения в базе данных

        coal_brand = CoalBrand.query.get(request.form['coal_brand'])  # Получаем марку угля, выбранную пользователем
        supplier = Supplier.query.get(coal_brand.supplier_id)  # Получаем поставщика, предоставляющего выбранную марку угля
        total_price = coal_brand.price_per_ton * int(request.form['quantity'])  # Вычисляем общую стоимость заказа
        order = Order(
            user_id=user.id,
            coal_brand_id=coal_brand.id,
            supplier_id=supplier.id,
            total_price=total_price,
            address=request.form['address']
        )
        db.session.add(order)  # Добавляем заказ в базу данных
        db.session.commit()  # Сохраняем изменения в базе данных
        return redirect(url_for('index'))  # Перенаправляем пользователя на главную страницу
    else:  # Если метод запроса - GET
        suppliers = Supplier.query.all()  # Получаем список всех поставщиков
        coal_brands = CoalBrand.query.all()  # Получаем список всех марок угля
        return render_template('order.html', suppliers=suppliers, coal_brands=coal_brands)

# @app.route('/order', methods=['GET', 'POST'])
# def order():
#     if request.method == 'POST':  # Если форма отправлена методом POST
#         user = User.query.filter_by(email=request.form['email']).first()  # Проверяем, есть ли пользователь с таким email в базе данных
#         if not user:  # Если пользователя с таким email нет в базе данных
#             user = User(name=request.form['name'], email=request.form['email'], password=generate_password_hash(request.form['password'], method='sha256'), last_address=request.form['address'])  # Создаем нового пользователя
#             db.session.add(user)  # Добавляем пользователя в базу данных
#             db.session.commit()  # Сохраняем изменения в базе данных
#         coal_brand = CoalBrand.query.get(request.form['coal_brand'])  # Получаем марку угля, которую выбрал пользователь
#         supplier = Supplier.query.get(coal_brand.supplier_id)  # Получаем поставщика, который предоставляет эту марку угля
#         total_price = coal_brand.price_per_ton * int(request.form['quantity'])  # Вычисляем общую стоимость заказа
#         order = Order(user_id=user.id, coal_brand_id=coal_brand.id, supplier_id=supplier.id, total_price=total_price, address=request.form['address'])  # Создаем новый заказ
#         db.session.add(order)  # Добавляем заказ в базу данных
#         db.session.commit()  # Сохраняем изменения в базе данных
#         return redirect(url_for('index'))  # Перенаправляем пользователя на главную страницу
#     else:  # Если форма не отправлена методом POST
#         coal_brand_id = request.args.get('coal_brand')  # Получаем идентификатор марки угля из параметров URL
#         coal_brand = CoalBrand.query.get(coal_brand_id)  # Получаем марку угля по идентификатору
#         return render_template('order.html', coal_brand=coal_brand)  # Отображаем страницу оформления заказа с выбранной маркой угля


if __name__ == "__main__":
    app.run(debug=True)