from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
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
class Rank(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    ranknow=db.Column(db.TEXT,nullable=False)
    minpower=db.Column(db.Integer,nullable=False)
@app.route('/')
def main():
    db.session.expire_all()
    rankpos=Rank.query.get(rank)


    return render_template('main.html',rankpos=rankpos)
@app.route('/sleep')
def sform():
    return render_template('sleep_form.html')
@app.route('/sleep/store',methods=['POST'])
def sstore():
    new_sleep=Sleep()
    new_sleep.day=request.form['day']
    new_sleep.sleeptime=request.form['sleeptime']
    new_sleep.getuptime=request.form['getuptime']
    db.session.add(new_sleep)
    db.session.commit()
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)