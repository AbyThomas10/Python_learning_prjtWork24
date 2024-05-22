
from flask import Flask,render_template,request
import mysql.connector
mydb = mysql.connector.connect(
    host= 'localhost',
    user = 'root',
    password = '1234',  
    database = 'cms'
)
mycursor = mydb.cursor()

#create a flask application
app = Flask(__name__)

user_dict = {'admin':'1234','user':'4567'}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/backtohome')
def backtohome():
    return render_template('emp_home.html')

@app.route('/loginhome',methods=['POST'])
def loginhome():
    user = request.form["user"]
    pwd = request.form["pass"]

    if user not in user_dict:
        return render_template('login.html',msg = 'Invalid User')
    elif user_dict[user] != pwd:
        return render_template('login.html', msg = 'Password Wrong')
    else:
        return render_template('emp_home.html', msg ='Welcome '+user)

@app.route('/view_1')
def view():
    query = "select * from Staff"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return render_template('viewAll_Staff.html', sqldata =data)

@app.route('/add')
def add():
    return render_template('addemp.html')
@app.route('/add_emp',methods=['GET','POST'])
def addemp():
    if request.method == 'POST':
        
        name = request.form['name']
        address = request.form['address']
        salary = request.form['salary']
        dept = request.form['dept']
        s_id = request.form['id']
        query = "insert into staff values (%s,%s,%s,%s,%s)"
        data = (name,address,salary,dept,s_id)
        mycursor.execute(query,data) 
        mydb.commit()
        return render_template('emp_home.html')
    return render_template('addemp.html')

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        staff_name = request.form['name']
        staff_address = request.form['address']
        staff_salary = request.form['salary']
        staff_dept = request.form['dept']
        staff_id = request.form['id']
        query = "update staff set name=%s,address=%s,salary=%s,department=%s where id=%s"
        data = (staff_name,staff_address,staff_salary,staff_dept,staff_id)
        mycursor.execute(query,data) 
        mydb.commit()
        message = f"Staff {staff_name} - data updated successfully"
        query ="select * from staff"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('update.html',sqldata=data,msg= message)
    else:
        query = "select * from staff"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('update.html', sqldata =data)
    
 
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        query = "delete from staff where id=%s"
        data=(id,)
        mycursor.execute(query,data)
        mydb.commit()
        message = f"The Staff {name} is deleted successfully"
        query ="select * from staff"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('delete.html', sqldata=data, msg=message)
    else:
        query = "select * from staff"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('delete.html', sqldata =data)

  


#run flask application
if __name__ == '__main__':
    app.run(debug = True)