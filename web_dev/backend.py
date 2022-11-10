from flask import Flask,redirect,request,render_template,redirect,url_for
import sqlite3 as sql , json ,base64

app = Flask(__name__)

                                                    # login page ( homepage render )

@app.route('/')
def loginpage():
    return render_template('login.html')

                                                    # Login Function and userpage

@app.route('/homepage',methods=["GET","POST"])
def homepage():
    if request.method=='POST':
        username = request.form.get('u_name')
        password = request.form.get('u_pswd')
        if username=="Admin" and password=="123":
            return render_template('admin.html')
        try:
        # if True:
            con = sql.connect('maindatabase.db')
            c = con.cursor()
            users = c.execute('select username from logindb')
            users = [x[0] for x in users.fetchall()]
            if username in users:
                fetched_pswd = c.execute('select password from logindb where username=?',([username]))
                fetched_pswd = fetched_pswd.fetchall()[0][0]
                con.commit()
                con.close()
                if fetched_pswd==password:
                    product_details = product_page()
                    if product_details:
                        return render_template('home.html',details=product_details)
                    else:
                        return render_template('home.html',details="Items not available currently")
                else:
                    # print('wrong password')
                    return render_template('login.html',msg="Wrong Password")
            else:
                # print('User Notfound')
                return render_template('login.html',msg="Wrong Username")
        except:
        # else:
            print('Database Error')
            return render_template('login.html')
    
    # product_details = product_page()
    # if product_details:
    #     return render_template('home.html',details=product_details)
    # else:
    #     return render_template('home.html',details="Items not available currently")


                                                    # Product retrieve from DB

def product_page():
    try:
    # if True:
        con = sql.connect('maindatabase.db')
        c = con.cursor()
        product_details = c.execute('select * from product_details')
        product_details=product_details.fetchall()
        product_details_list =[]
        for i in product_details:
            temp=[]
            for j in i:
                temp.append(j)
            temp[-1] = base64.b64encode(temp[-1]).decode('UTF-8')
            product_details_list.append(temp)
        con.commit()
        con.close
        return product_details_list
    except:
    # else:
        print('Fetching error')


                                                    # description page Function

@app.route('/describe/<p_id>')
def description_page(p_id):
    con = sql.connect('maindatabase.db')
    c = con.cursor()
    product_details = c.execute('select * from product_details where id=?',([p_id]))
    product_details_list =[]
    for i in product_details:
        temp=[]
        for j in i:
            temp.append(j)
        temp[-1] = base64.b64encode(temp[-1]).decode('UTF-8')
        product_details_list.append(temp)
    con.commit()
    con.close
    print(product_details_list)
    return render_template('description.html', p_details = product_details_list)



                                                    # Databse upload and update Function


@app.route('/p_upload' ,methods=["GET","POST"])
def product_update():
    if request.method=="POST":
        p_id1 = request.form.get('p_id')
        p_name1 = request.form.get('p_name')
        p_desc1 = request.form.get('p_desc')
        p_category1 = request.form.get('p_category')
        p_mrp1 = request.form.get('p_mrp')
        p_prev_price1 = request.form.get('p_prev_price')
        p_img1 = request.files['p_img'].read()  # to be stored in db
        try:
        # if True:
            con = sql.connect('maindatabase.db')
            c = con.cursor()
            c.execute("insert into product_details(id,title,desc,category,mrp,prev_price,photo) values(?,?,?,?,?,?,?)",([p_id1,p_name1,p_desc1,p_category1,p_mrp1,p_prev_price1,p_img1]))
            con.commit()
            con.close()
            return render_template('admin.html',msg='Inserted succesfully')
        except sql.IntegrityError:
        # else:
            return render_template('admin.html',msg="Product Already exists")
        except sql.OperationalError:
            return render_template('admin.html',msg="Database Locked")
        except:
            return render_template('admin.html',msg="Sonmething Error")

    return render_template('admin.html')


                                                    # Register Function

@app.route('/register',methods=["GET","POST"])
def registerpage():
    if request.method=='POST':
        username = request.form.get('u_name')
        password1 = request.form.get('u_pswd1')
        password2 = request.form.get('u_pswd2')
        if password1==password2:
            try:
                con = sql.connect('maindatabase.db')
                c = con.cursor()
                c.execute('insert into logindb(username,password) values(?,?)',([username,password1]))
                con.commit()
                con.close()
                # print('Inserted Succesfully')
                return render_template('login.html',msg="Registration Successfull")
            except sql.IntegrityError:
                # print('user exists')
                return render_template('register.html',msg="User Already Exists...")
        else:
            # print('Password mismatch')
            return render_template('register.html',msg="Password mismatch")
    return render_template('register.html')

                                                    # Main Function

if __name__ == "__main__":
    app.run(debug=True)