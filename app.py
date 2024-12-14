from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime,timedelta
import random
app=Flask(__name__)

db_uri='mysql+pymysql://root:@localhost/pokemonsleep?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI']=db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
rank=1
class Sleep(db.Model):
    __tablename__='sleep'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    day=db.Column(db.Date,nullable=False)
    sleeptime=db.Column(db.Time,nullable=False)
    getuptime=db.Column(db.Time,nullable=False)
    sleepminute=db.Column(db.Integer,nullable=False)
    sleepscore=db.Column(db.Integer,nullable=False)
    sleeppower=db.Column(db.Integer,nullable=False)
class Rank(db.Model):
    __tablename__='rank'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    ranknow=db.Column(db.TEXT,nullable=False)
    minpower=db.Column(db.Integer,nullable=False)
class Cavigon(db.Model):
    __tablename__='cavigon'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    power=db.Column(db.Integer)
    content=db.Column(db.TEXT)
class Pokemon(db.Model):
    __tablename__='pokemon'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    time=db.Column(db.DATETIME,nullable=True)
    flg=db.Column(db.Boolean)
class Nut(db.Model):
    __tablename__='nut'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    num=db.Column(db.INTEGER,nullable=False)
    limitnum=db.Column(db.INTEGER,nullable=False)
    cooknum=db.Column(db.INTEGER,nullable=False)

@app.route('/')
def main():
    global rank
    db.session.expire_all()
    rankpos=Rank.query.get(rank)
    cavigonid=Cavigon.query.get(1)
    randnutnum=Nut.query.get(1)
    if request.args.get('message'):
        message=request.args.get('message')
    else:
        message="pokemon sleepヘようこそ"
    if request.args.get('randnutnum'):
        if randnutnum.num+int(request.args.get('randnutnum'))<randnutnum.limitnum:
            randnutnum.num+=int(request.args.get('randnutnum'))
        else:
            print("食材を追加できません")
        db.session.add(randnutnum)
        db.session.commit()
        return render_template('main.html',rankpos=rankpos,cavigonid=cavigonid,message=message,randnutnum=randnutnum)
    return render_template('main.html',rankpos=rankpos,cavigonid=cavigonid,message=message,randnutnum=randnutnum)
@app.route('/sleep')
def sform():
    return render_template('sleep_form.html')
@app.route('/sleep/store',methods=['POST'])
def sstore():
    new_sleep=Sleep()
    refer_cavigon=Cavigon.query.get(1)
    new_sleep.day=request.form['day']
    new_sleep.sleeptime=request.form['sleeptime']
    new_sleep.getuptime=request.form['getuptime']
    time1=datetime.strptime(new_sleep.sleeptime,"%H:%M")
    time2=datetime.strptime(new_sleep.getuptime,"%H:%M")
    if time1>time2:
        time2+=timedelta(days=1)
    time_diff=time2-time1
    sleeptime=time_diff.total_seconds()/60
    sleepscore=min((sleeptime/510)*100,100)
    sleeppower=sleeptime*refer_cavigon.power
    new_sleep.sleepminute=sleeptime
    new_sleep.sleepscore=sleepscore
    new_sleep.sleeppower=sleeppower
    
    print(sleeptime)
    print(sleepscore)
    print((sleeptime/510)*100)
    db.session.add(new_sleep)
    db.session.commit()
    return render_template("sleep_store.html",new_sleep=new_sleep)
@app.route('/collect/<int:id>')
def collect(id):
    global rank
    ranknow=Rank.query.get(rank)
    update_cavigon=Cavigon.query.get(1)
    update_pokemon=Pokemon.query.get(id)
    
    if update_pokemon.time!=None:
        time1=update_pokemon.time
        time2=datetime.now()
        time_diff=((time2-time1).total_seconds())/60
        if time_diff>=0:
            update_pokemon.flg=True
    else:
        update_pokemon.flg=True
    if update_pokemon.flg==True:
        sumpower=0
        randcollectnum=random.randint(0,10)
        for i in range(randcollectnum):
            randpower=random.randint(35,65)
            sumpower+=randpower
        randnutnum=random.randint(1,15)
        update_cavigon.power+=sumpower
        update_pokemon.time=datetime.now()
        update_pokemon.flg=False
        db.session.commit()
        if ranknow.minpower<update_cavigon.power:
            rank+=1
        return redirect(url_for('main',randnutnum=randnutnum))
    else:
        message="まだ木の実はないようです"
        return redirect(url_for('main',message=message))
@app.route('/cooking')
def cooking():
    cook_nut=Nut.query.get(1)
    cook_power=Cavigon.query.get(1)
    cnut_num=min(cook_nut.num,cook_nut.cooknum)
    if cnut_num>0:
        cook_nut.num-=cnut_num
        db.session.add(cook_nut)
        randcookpower=random.randint(1000,3000)
        cook_power.power+=randcookpower
        db.session.add(cook_power)
        db.session.commit()
        message="料理でカビゴンは"+str(randcookpower)+"のパワーを得ました"
        return redirect(url_for('main',message=message))
    message="材料が足りないため、料理ができません"
    return redirect(url_for('main',message=message))
@app.route('/reset')
def reset():
    global rank
    rank=1
    reset_cavigon=Cavigon.query.get(1)
    reset_nut=Nut.query.get(1)
    reset_cavigon.power=0
    reset_nut.num=0
    reset_nut.cooknum=20
    for i in range(1,6):
        reset_pokemon=Pokemon.query.get(i)
        reset_pokemon.time=None
    db.session.commit()
    return redirect('/')
@app.route('/cookquantity')
def cquantity():
    cquantity=Nut.query.get(1)
    cquantity.cooknum+=5
    db.session.commit()
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)