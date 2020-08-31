from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import request,jsonify
from backend.app import app
from .app import db
from .models import User, Ticket, MovieShow
import atexit
import time
from datetime import datetime,timedelta



#business case1 for booking ticket
@app.route('/bookticket' , methods = ['POST'])
def new_user():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        name = data['name']
        phoneNumber = data['phoneNumber']
        
        #basic validation

        if phoneNumber and len(phoneNumber)>10:
          return "Phone number should not exceed for more than 10 digits."
        elif not phoneNumber:
          return "Please enter your phonenumber."
        if name and len(name)>50:
          return "Phone number should not exceed for more than 50 characters."
        elif not name:
          return "Please enter your name."
        if not str.isalpha(name):
          return 'Name can contain only alphabets.'
        if not data["timings"] :
          return 'Please enter the timings for which you want to book the ticket.'


        d=[]
        dt={}
        user = User.query.filter_by(phoneNumber=phoneNumber).first()
        if not user:
            new_user = User(name=name,phoneNumber = phoneNumber)
            db.session.add(new_user)
            db.session.commit()
        user = User.query.filter_by(phoneNumber=phoneNumber).first()
        cust_id=user.id
        for time in data['timings']:
           tm=time
           p=MovieShow.query.filter_by(timing=tm).first()
           if p is not None:
             if p.number_of_tickets!=0:
              k=p.number_of_tickets-1
              p.number_of_tickets=k
              db.session.commit()
              new_tkt=Ticket(cust_id=cust_id,time_of_movie=p.timing,hasexpired=0)
              db.session.add(new_tkt)
              db.session.commit()
              dt = {'time' : time,'Booking':"Confirmed"}
              d.append(dt)
             else:
              dt = {'time' : time,'Booking':"All tickets are booked for this timings! Please choose another"}
              d.append(dt)
           else:
              dt = {'time' : time,'Booking':"Incorrect time entered."}
              d.append(dt)
        
        return jsonify(d)
        
#business case2 for updating time of the show to a new time given.
@app.route('/updatetime/<string:old_time>', methods = ['PUT'])
def updateTime(old_time):
  if request.method =="PUT":
    data=request.get_json()
    if not data["new_timing"]:
      return "You have left the new_timing empty."
    d=data["new_timing"].split(" ")
    l1=d[0].split('-')
    l2=d[1].split(':')
    nw_tm = datetime(int(l1[0]),int(l1[1]),int(l1[2]),int(l2[0]),int(l2[1]),int(l2[1]))
    timings = MovieShow.query.filter_by(timing = old_time).first()
    if not timings:    
            return "Please check if you have entered the time to be updated correctly."
    if datetime.now()>nw_tm:
      return "You can update the new time to be later than the current time."
    
    try:
       timings = MovieShow.query.filter_by(timing = old_time).update(dict(timing=nw_tm))
       tkt_update = Ticket.query.filter_by(time_of_movie= old_time).update(dict(time_of_movie=nw_tm))
       db.session.commit()
       return "Database updated successfully"
    except:
       return "This time-slot already exists."
    
#business case3  for viewing tickets booked for a particular show timing
@app.route('/viewtickets/<string:time_for_show>', methods = ['GET'])
def get_tickets(time_for_show):
  if request.method =="GET":
    data=[]
    try:
        ticket_list = Ticket.query.filter_by(time_of_movie =time_for_show).all()
    except:
        return "No such timing of the show exists. Please enter correct timing."
    if not ticket_list:
       return "No such timing of the show exists. Please enter correct timing. Or no ticket has been bought for this show."
    for ticket in ticket_list:
            dict = {'tid' : ticket.tid,"time_of_movie":time_for_show,"customer_id":ticket.cust_id,"hasexpired":ticket.hasexpired}
            data.append(dict)
    return jsonify(data)

#business case4 for cancelling ticket given a ticket id.
@app.route('/ticketcancel/<int:ticket_id>', methods = ['DELETE'])
def cancel_ticket(ticket_id):
  if request.method =="DELETE":
    
    try:
       tkt=Ticket.query.filter_by(tid=ticket_id).first()
    except:
       return "The ticket id you have entered is incorrect or has expired."
    if not tkt:
       return "The ticket id you have entered is incorrect or has expired."

    db.session.delete(tkt)
    db.session.commit()
    return jsonify({"response":"Ticket successfully cancelled."})

#business case5 for viewing the details of an user on the basis of given ticket id.
@app.route('/viewuser/<int:tkt_id>', methods = ['GET'])
def view_user(tkt_id):
  if request.method =="GET":
    data=request.get_json()
    try:
       tkt=Ticket.query.filter_by(tid=tkt_id).first()
    except:
       return "Could not fetch details."
    if not tkt:
       return "The ticket id you have entered is incorrect or has expired."
    cid=tkt.cust_id
    user = User.query.filter_by(id=cid).first()
    return jsonify({"customer_id":user.id,"name":user.name,"phoneNumber":user.phoneNumber})

#business case6 for marking tickets that have expired as 1
def mark_expire():
  tkt=Ticket.query.all()
  for ticket in tkt:
    if datetime.now()-timedelta(hours=8)>=ticket.time_of_movie:
       try:
          expire = Ticket.query.filter_by(tid = ticket.tid).update(dict(hasexpired=1))
          db.session.commit()
       except:
          return "Could not change state of hasexpired column."
    else:
       try:
          expire = Ticket.query.filter_by(tid = ticket.tid).update(dict(hasexpired=0))
          db.session.commit()
       except:
          return "Could not change state of hasexpired column."
  delete_tkt()
  

#business case7 for deleting all the expired tickets
def delete_tkt():
  tkt=Ticket.query.filter_by(hasexpired=1).all()
  for ticket in tkt:
      try:
          db.session.delete(ticket)
          db.session.commit()
      except:
          return "Could not delete ticket."



#scheduler for deleting the expired tickets automatically.
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=mark_expire,
    trigger=IntervalTrigger(seconds=600),
    id='marking_expiry',
    name='Mark expired tickets',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
