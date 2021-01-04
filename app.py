from flask import Flask, render_template , url_for, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Product(db.Model):
    prod_id=db.Column(db.String(200) , primary_key=True)

    def pro_id (self):
        return '<P_roduct %r>' % self.prod_id


class Location(db.Model):
    loc_id=db.Column(db.String(200) , primary_key=True)
    ProductMovement = db.relationship("ProductMovement", backref="Location", lazy = "dynamic")
   


    def loca_id (self):
        return '<L_ocation %r>' % self.loc_id


class ProductMovement(db.Model):
    move_id=db.Column(db.String(200) , primary_key=True)
    timestamp=db.Column(db.DateTime , default=datetime.utcnow)
    from_location=db.Column( db.String(200), db.ForeignKey(Location.loc_id),nullable=True)
    #to_location=db.Column( db.String(200), db.ForeignKey(Location.loc_id),nullable=True)
    qty=db.Column(db.Integer , nullable=False)
    product_id=db.Column(db.String(200), db.ForeignKey('product.prod_id'),nullable=False)
    product = db.relationship('Product', backref=db.backref('ProductMovement', lazy=True))

    def pro_Movement (self):
        return '<P_Movement %r>' % self.move_id

@app.route('/' , methods=['POST' , 'GET'])
def index():
    if request.method == 'POST':
        product_name = request.form['product']
        new_Product = Product(prod_id=product_name)

        #push the new product obj to the database 
        try:
            db.session.add(new_Product)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was a problem in your added'
    else:
        #return all the products
        products = Product.query.all()

        return render_template('index.html' , products = products)

@app.route('/delete/<string:id>')
def delete(id):
    del_product = Product.query.get_or_404(id)

    try:
        db.session.delete(del_product)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that Product'


@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    update_pro = Product.query.get_or_404(id)

    if request.method == 'POST':
        update_pro.prod_id = request.form['product']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your product'

    else:
        return render_template('update.html', product = update_pro)

    #here we addd the small comment 

if __name__ == '__main__':
    app.run(debug=True)