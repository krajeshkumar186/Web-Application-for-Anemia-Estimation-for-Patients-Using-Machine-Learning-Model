import mysql
from flask import Flask,render_template,url_for,request
from mysql.connector import cursor
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import pandas as pd

mydb = mysql.connector.connect(host='localhost',user='root',password="",port='3306',database='anemia')
app=Flask(__name__)

def preprocessing(file):
    file.drop(index=df.index[0], axis=0, inplace=True)
    file.rename(columns={'Sex  ':'Sex','Age      ': 'Age', '  RBC    ': 'RBC', 'MCV  ': 'MCV', ' MCHC  ': 'MCHC', ' RDW    ': 'RDW',
                       ' PLT /mm3': 'PLT', ' HGB ': 'HGB'}, inplace=True)
    return file


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration',methods=['POST','GET'])
def registration():
    if request.method=="POST":
        print('a')
        un=request.form['name']
        print(un)
        em=request.form['email']
        pw=request.form['password']
        print(pw)
        cpw=request.form['cpassword']
        if pw==cpw:
            sql = "SELECT * FROM hmg"
            cur = mydb.cursor()
            cur.execute(sql)
            all_emails=cur.fetchall()
            mydb.commit()
            all_emails=[i[2] for i in all_emails]
            if em in all_emails:
                return render_template('registration.html',msg='a')
            else:
                sql="INSERT INTO hmg(name,email,password) values(%s,%s,%s)"
                values=(un,em,pw)
                cursor=mydb.cursor()
                cur.execute(sql,values)
                mydb.commit()
                cur.close()
                return render_template('registration.html',msg='success')
        else:
            return render_template('registration.html',msg='repeat')
    return render_template('registration.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        em=request.form['email']
        print(em)
        pw=request.form['password']
        print(pw)
        cursor=mydb.cursor()
        sql = "SELECT * FROM hmg WHERE email=%s and password=%s"
        val=(em,pw)
        cursor.execute(sql,val)
        results=cursor.fetchall()
        mydb.commit()
        print(results)
        print(len(results))
        if len(results) >= 1:
            return render_template('home.html',msg='login usuccesful')
        else:
            return render_template('login.html',msg='Invalid Credentias')


    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload',methods=['POST','GET'])
def upload():
    global df
    if request.method=="POST":
        file=request.files['file']
        print(type(file.filename))
        print('hi')
        df=pd.read_csv(file)
        print(df.heapd(2))
        return render_template('upload.html', msg='Dataset Uploaded Successfully')
    return render_template('upload.html')

@app.route('/view_data')
def view_data():
    print(df)
    print(df.head(2))
    print(df.columns)
    return render_template('viewdata.html',columns=df.columns.values,rows=df.values.tolist())
@app.route('/split',methods=["POST","GET"])
def split():
    global X,y,X_train,X_test,y_train,y_test
    if request.method=="POST":
        size=int(request.form['split'])
        size=size/100
        print(size)
        dataset=preprocessing(df)
        print(df)
        print(df.columns)
        dataset = dataset.loc[0:364]
        X=dataset.drop(['HGB','S. No.'],axis=1)
        y=dataset['HGB']
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=size,random_state=52)
        print(y_test)

        return render_template('split.html',msg='Data Preprocessed and It Splits Succesfully')
    return render_template('split.html')

@app.route('/model',methods=['POST','GET'])
def model():
    if request.method=="POST":
        model=int(request.form['algo'])
        if model==0:
            return render_template('model.html',msg='Please Choose any Algorithm')
        elif model==1:
            model=Lasso()
            model.fit(X_train,y_train)
            y_pred=model.predict(X_test)
            score=r2_score(y_test,y_pred).round(4)
            score=score*100
            msg='The R2 Score for Lasso is ', score
            return render_template('model.html',msg=msg)

        else:
            model = Ridge()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred).round(4)
            score = score * 100
            msg = 'The R2 Score for Ridge is ', score
        return render_template('model.html',msg=msg)
    return render_template('model.html')

@app.route('/prediction',methods=["POST","GET"])
def prediction():
    if request.method=="POST":
        val=request.form['d']
        # if f1=="male":
        #     val=0
        # else:
        #     val=1
        print(val)
        f2=request.form['age']
        f3=request.form['rbc']
        f4=request.form['pcv']
        f5=request.form['mcv']
        f6=request.form['mch']
        f7=request.form['mchc']
        f8=request.form['rdw']
        f9=request.form['tlc']
        f10=request.form['plt']
        print(f10)
        print(type(f10))
        l=[val,f2,f3,f4,f5,f6,f7,f8,f9,f10]
        model=Ridge()
        model.fit(X_train,y_train)
        ot=model.predict([l])
        print(ot)
        if ot<12:
            a='The Person is Diagnosed with Anemia'
        else:
            a="The Person is safe and not effected with Anemia"
        return render_template('prediction.html',msg=a)
    return render_template('prediction.html')

@app.route('/about')
def about():
    return render_template('about.html')







if __name__=="__main__":
    app.run(debug=True)