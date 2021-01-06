from flask import Flask, render_template , request , redirect
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
    def loca_id (self):
        return '<L_ocation %r>' % self.loc_id


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp=db.Column(db.DateTime , default=datetime.utcnow.__format__)
   
    from_location=db.Column( db.String(200), db.ForeignKey(Location.loc_id),nullable=True)
    to_location=db.Column( db.String(200), db.ForeignKey(Location.loc_id),nullable=True)
    locationf = db.relationship("Location" , foreign_keys=[from_location])
    locationt = db.relationship("Location" , foreign_keys=[to_location])
   
    qty=db.Column(db.Integer , nullable=False)
    product_id=db.Column(db.String(200), db.ForeignKey('product.prod_id'),nullable=False)
    product = db.relationship('Product', backref=db.backref('ProductMovement', lazy=True))

    def pro_Movement (self):
        return '<P_Movement %r>' % self.id

#Home Page
@app.route('/')
def index():
    return render_template('index.html')

#Product Page
@app.route('/product' , methods=['POST' , 'GET'])
def product():
    if request.method == 'POST':
        if(request.form['product']):
         product_name = request.form['product']
         new_Product = Product(prod_id=product_name)

         #push the new product obj to the database 
         try:
            db.session.add(new_Product)
            db.session.commit()
            return redirect('/product')
         except:
            return 'there was a problem in your added'
        else:
            return 'You should fill the input '
    else:
        #return all the products
        products = Product.query.all() 

        return render_template('product.html' , products = products)

@app.route('/delete/<string:id>')
def delete(id):
    del_product = Product.query.get_or_404(id)

    try:
        db.session.delete(del_product)
        db.session.commit()
        return redirect('/product')
    except:
        return 'There was a problem deleting th at Product'

@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    update_pro = Product.query.get_or_404(id)

    if request.method == 'POST':
        update_pro.prod_id = request.form['product']

        try:
            db.session.commit()
            return redirect('/product')
        except:
            return 'There was an issue updating your product'

    else:
        return render_template('update.html', product = update_pro)



 #Location Page
@app.route('/location' , methods=['POST' , 'GET'])
def location():
    if request.method == 'POST':
         if(request.form['location']):
            location_name = request.form['location']
            new_location = Location( loc_id= location_name)
   
            #push the new location obj to the database 
            try:
              db.session.add( new_location)
              db.session.commit()
              return redirect('/location')
            except:
              return 'there was a problem in your added'
         else:
            return 'You should fill the input '
    else:
        #return all the locations
        locations = Location.query.all()

        return render_template('location.html' , locations = locations)

@app.route('/deletel/<string:id>')
def deleteLoc(id):
    del_location = Location.query.get_or_404(id)

    try:
        db.session.delete(del_location)
        db.session.commit()
        return redirect('/location')
    except:
        return 'There was a problem deleting that location'


@app.route('/updatel/<string:id>', methods=['GET', 'POST'])
def updatel(id):
    update_loc = Location.query.get_or_404(id)

    if request.method == 'POST':
        update_loc.loc_id = request.form['location']

        try:
            db.session.commit()
            return redirect('/location')
        except:
            return 'There was an issue updating your location'

    else:
        return render_template('update_loc.html', location = update_loc)


#Product-Movement Page
@app.route('/proMovement' , methods=['POST' , 'GET'])
def proMovement():
    if request.method == 'POST':
        new_proMovement = ProductMovement(from_location= request.form['from'] , to_location=request.form['to'] ,qty=request.form['pro_qty'] ,product_id=request.form['pro_id']  )
            #push the new Product-Movement obj to the database 
        try:
          db.session.add(new_proMovement)
          db.session.commit()
          return redirect('/proMovement')
        except:
              return 'there was a problem in your added'
    else:
        #return all the Product-Movements
        productsmove = ProductMovement.query.all()
        return render_template('productMovement.html' , productsmove = productsmove)


@app.route('/updateMovement/<int:id>', methods=['GET', 'POST'])
def updateMovement(id):
    update_Move = ProductMovement.query.get_or_404(id)

    if request.method == 'POST':
        update_Move.from_location = request.form['from']
        update_Move.to_location=request.form['to']
        update_Move.qty=request.form['pro_id']
        update_Move.product_id=request.form['pro_id']

        try:
            db.session.commit()
            return redirect('/proMovement')
        except:
            return 'There was an issue updating your Movement'

    else:
        return render_template('update_Movement.html', productm =  update_Move)

# @app.route('/deleteM')
# def deleteM():
#     id='7'
#     del_location = ProductMovement.query.get_or_404(id)

#     try:
#         db.session.delete(del_location)
#         db.session.commit()
#         return redirect('/proMovement')
#     except:
#         return 'There was a problem deleting that location'



#Product Balance
@app.route('/ProductBalance', methods=['POST' , 'GET'])
def ProductB():
    if request.method == 'POST':
      prodMov =ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
      loc = Location.query.all()
      result={}
      
      for y in loc:
           myarray=[] 
           for x in prodMov:
             #print('pro ->>>>' , x.to_location , x.product_id , x.qty)
             if y.loc_id == x.to_location:
                 result[x.to_location]=myarray
                 v={'product':x.product_id , 'Location':x.to_location , "Qty":x.qty}
                 myarray.append(v)
                
      print("v = " ,result)
    #   finalResult={}
    #   for y in loc:
    #       mynewarray=[]
    #       for x , z in result.items():
    #           finalResult[x]=mynewarray
    #           print("x= ",x , "y" ,z)
    #           value=z[0]['product']
    #           if y.loc_id == x:
                  
    #               for i in range(len(z)):
                      
    #                   if z[i]['product'] == value:
    #                       mynewarray.append(z[i])
                      
    #       print("the final = " , finalResult)         

      return render_template('balancePro.html' , balanc = result)

    else :
        return 'There was a problem '



   

if __name__ == '__main__':
    app.run(debug=True)