# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py!"
    return dict(message=T('Hello World'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

import datetime
def index():
	form=SQLFORM.factory(
			Field('From',requires=IS_IN_DB(db,db.places.body)),
			Field('To',requires=IS_IN_DB(db,db.places.body)),
			Field('d','date',label='Departure(Date)',requires=IS_DATE()),
			Field('d1','date',label='Arrival(Date)'),
			Field('Class',requires=IS_IN_SET(['Business','Economy'])),
			Field('seats',label='Number of passengers',requires=IS_IN_SET((1,2,3,4,5,6,7,8,9,10))))
	if form.accepts(request.vars,session):
		if form.vars.From == form.vars.To:
			session.flash="Source and Destination should not be the same!"
			redirect(URL('index'))
		elif form.vars.d<datetime.date.today():
			session.flash="Enter a valid date!"
			redirect(URL('index'))
		elif form.vars.d1:
			session.seats=request.vars.seats
			session.date=request.vars.d
			session.date2=request.vars.d1
		 	redirect(URL('round_search',args=(request.vars.From,request.vars.To,request.vars.d,request.vars.seats,request.vars.Class,request.vars.d1)))
		else:
			session.seats=request.vars.seats
			session.date=request.vars.d
			redirect(URL('search',args=(request.vars.From,request.vars.To,request.vars.d,request.vars.seats,request.vars.Class)))
	session.var=1
	return dict(form=form)

def round_search():
	src=db((db.trips.src==request.args(0))&(db.trips.d==request.args(2))&(db.trips.cl==str(request.args(4)))).select()
	dest=db((db.trips.dest==request.args(1))&(db.trips.cl==str(request.args(4)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Trips Found! :( "
        	redirect(URL('index'))
	lis=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis.append(que)
	if len(lis)==0:
	  	session.flash="No trips found!"
	  	redirect(URL('index'))
	seats=[]
	price=[]
	logo=[]
	dtime=[]
	atime=[]
	n=[]
	company=[]
	for i in range(len(lis)):
		send=[]
		some=db((db.trips.name==lis[i])&(db.trips.src==request.args(0))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime.append(some[0].departure)
			while desti!=request.args(1):
				some=db((db.trips.name==lis[i])&(db.trips.src==desti)).select()
				if len(some):	
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No trips Found!"
#					redirect(URL('index'))
			atime.append(some[0].arrival)
			n.append(send)
			logo.append(some[0].logo)
			company.append(some[0].company)
			seats.append(m)
			price.append(p)
		else:
			session.flash="No trips found!"
#			redirect(URL('index'))
	l=len(lis)
	for i in range(l):
		if seats[i]<int(request.args(3)):
			seats.remove(seats[i])
			price.remove(price[i])
			logo.remove(logo[i])
			atime.remove(atime[i])
			dtime.remove(dtime[i])
			lis.remove(lis[i])
	new=[]
	for i in n:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new.append(st[0:-1])

	src=db((db.trips.src==request.args(1))&(db.trips.d==request.args(5))&(db.trips.cl==str(request.args(4)))).select()
	dest=db((db.trips.dest==request.args(0))&(db.trips.cl==str(request.args(4)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Trips Found! :( "
        	redirect(URL('index'))
	lis1=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis1.append(que)
	if len(lis1)==0:
	  	session.flash="No trips found!"
	  	redirect(URL('index'))
	seats1=[]
	price1=[]
	logo1=[]
	dtime1=[]
	atime1=[]
	n1=[]
	company1=[]
	for i in range(len(lis1)):
		send=[]
		some=db((db.trips.name==lis1[i])&(db.trips.src==request.args(1))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime1.append(some[0].departure)
			while desti!=request.args(0):
				some=db((db.trips.name==lis1[i])&(db.trips.src==desti)).select()
				if len(some):	
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No trips Found!"
#					redirect(URL('index'))
			atime1.append(some[0].arrival)
			n1.append(send)
			logo1.append(some[0].logo)
			company1.append(some[0].company)
			seats1.append(m)
			price1.append(p)
		else:
			session.flash="No trips found!"
#			redirect(URL('index'))
	l=len(lis1)
	for i in range(l):
		if seats[i]<int(request.args(3)):
			seats.remove(seats1[i])
			price.remove(price1[i])
			logo.remove(logo1[i])
			atime.remove(atime1[i])
			dtime.remove(dtime1[i])
			lis.remove(lis1[i])
	new1=[]
	for i in n1:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new1.append(st[0:-1])
	return dict(lis=lis,seats=seats,new=new,price=price,dtime=dtime,atime=atime,logo=logo,company=company,lis1=lis1,seats1=seats1,new1=new1,price1=price1,dtime1=dtime1,atime1=atime1,logo1=logo1,company1=company1)

def search():
	session.date=request.args(2)
	src=db((db.trips.src==request.args(0))&(db.trips.d==request.args(2))&(db.trips.cl==str(request.args(4)))).select()
	dest=db((db.trips.dest==request.args(1))&(db.trips.cl==str(request.args(4)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Trips Found! :( "
        	redirect(URL('index'))
	lis=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis.append(que)
	if len(lis)==0:
	  	session.flash="No trips found!"
	  	redirect(URL('index'))
	seats=[]
	price=[]
	logo=[]
	dtime=[]
	atime=[]
	n=[]
	company=[]
	for i in range(len(lis)):
		send=[]
		some=db((db.trips.name==lis[i])&(db.trips.src==request.args(0))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime.append(some[0].departure)
			while desti!=request.args(1):
				some=db((db.trips.name==lis[i])&(db.trips.src==desti)).select()
				if len(some):	
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No trips Found!"
					redirect(URL('index'))
			atime.append(some[0].arrival)
			n.append(send)
			logo.append(some[0].logo)
			company.append(some[0].company)
			seats.append(m)
			price.append(p)
		else:
			session.flash="No trips found!"
			redirect(URL('index'))
	l=len(lis)
	for i in range(l):
		if seats[i]<int(request.args(3)):
			seats.remove(seats[i])
			price.remove(price[i])
			logo.remove(logo[i])
			atime.remove(atime[i])
			dtime.remove(dtime[i])
			lis.remove(lis[i])
	new=[]
	for i in n:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new.append(st[0:-1])
	return dict(lis=lis,seats=seats,new=new,price=price,dtime=dtime,atime=atime,logo=logo,company=company)

import time
@auth.requires_login()
def confirm():
	return dict()	

@auth.requires_login()	
def round_confirm():
	flight1=request.vars.flight1.split('^')
	flight2=request.vars.flight2.split('^')
	return dict(flight1=flight1,flight2=flight2)

def round_ticket():
#	print session.date
#	print session.date2
#	print session.seats

	flight1=request.vars.flight1.split('^')
	n1=flight1[len(flight1)-1].split('_') 
	flight2=request.vars.flight2.split('^')
	n2=flight2[len(flight2)-1].split('_')
	for i in range(len(n1)):
		seats=db(db.trips.id==n1[i]).select()
		seat=seats[0].seats
		db(db.trips.id==n1[i]).update(seats=seat-int(session.seats))
	for i in range(len(n2)):
		seats=db(db.trips.id==n2[i]).select()
		seat=seats[0].seats
		db(db.trips.id==n2[i]).update(seats=seat-int(session.seats))
	date=datetime.datetime.strptime(session.date,"%Y-%m-%d").date()
	arrival=datetime.datetime.strptime(flight1[2],"%H:%M:%S").time()
	depart=datetime.datetime.strptime(flight1[3],"%H:%M:%S").time()
	print date, arrival, depart
	db.flight_bookings.insert(user_id=auth.user.id,d=date,arrival=arrival,depart=depart,lis=flight1[6],price=flight1[5],booked_in=flight1[0],src=request.args(0),dest=request.args(1),cl=request.args(2),num=int(session.seats))
	date=datetime.datetime.strptime(session.date2,"%Y-%m-%d").date()
	arrival=datetime.datetime.strptime(flight2[2],"%H:%M:%S").time()
	depart=datetime.datetime.strptime(flight2[3],"%H:%M:%S").time()
	print date, arrival, depart
	db.flight_bookings.insert(user_id=auth.user.id,d=date,arrival=arrival,depart=depart,lis=flight2[6],price=flight2[5],booked_in=flight2[0],src=request.args(1),dest=request.args(0),cl=request.args(2),num=int(session.seats))
	redirect(URL('index'))

from gluon.tools import Mail
mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'Traveller\'s paradise'
mail.settings.login = 'ayushkhandelwal115@gmail.com:ayush115'
def book():
	n=request.vars.send
	n=request.vars.send.split('_')
	red=db((db.trips.name==request.vars.lis)&(db.trips.cl==request.vars.cl)).select()
	for i in range(len(n)):
		seats=db(db.trips.id==n[i]).select()
		seat=seats[0].seats
		db(db.trips.id==n[i]).update(seats=seat-int(request.vars.seats))
	db.flight_bookings.insert(user_id=auth.user.id,num=request.vars.seats,d=session.date,arrival=request.vars.atime,depart=request.vars.dtime,lis=request.vars.send,price=request.vars.price,booked_in=request.vars.lis,src=request.vars.src,dest=request.vars.dest,cl=request.vars.cl)
	email=auth.user.email
	mail.send(to=[email],
			subject='Ticket booked!',
			message='Flight id :'+request.vars.lis+'\nDeparture time : '+request.vars.dtime+'\nArrival time : '+request.vars.atime+'\nNumber of seats : '+request.vars.seats+'\n')
	session.flash="Your ticket has been booked!"
	redirect(URL('index'))


def bus_booking():
	session.var=3	
	form=SQLFORM.factory(
			Field('From',requires=IS_IN_DB(db,db.places.body)),
			Field('To',requires=IS_IN_DB(db,db.places.body)),
			Field('d','date',label='Date of journey',requires=IS_DATE()),
			Field('seats',label='Number of passengers',requires=IS_IN_SET((1,2,3,4,5,6,7,8,9,10))))
	if form.accepts(request.vars,session):
		if form.vars.From == form.vars.To:
			session.flash="Source and Destination should not be the same!"
			redirect(URL('bus_booking'))
		if form.vars.d<datetime.date.today():
			session.flash="Enter a valid date!"
			redirect(URL('bus_booking'))
		else:
			redirect(URL('bus_result',args=(request.vars.From,request.vars.To,request.vars.d,request.vars.seats)))  
	return dict(form=form)

def bus_result():
	session.date=request.args(2)
	src=db((db.bus_trips.src==request.args(0))&(db.bus_trips.d==request.args(2))&(db.bus_trips.seats>int(request.args(3)))).select()
	dest=db((db.bus_trips.dest==request.args(1))&(db.bus_trips.seats>int(request.args(3)))).select()
    	if len(src)==0 or len(dest)==0:
       	 	session.flash="No Trips Found! :( "
        	redirect(URL('bus_booking'))
	lis=[]
	for i in range(0,len(dest)):
		que=dest[i].name
		for j in range(len(src)):
			if que==src[j].name:
				lis.append(que)
	if len(lis)==0:
	  	session.flash="No trips found!"
	  	redirect(URL('bus_booking'))
	seats=[]
	price=[]
	logo=[]
	dtime=[]
	atime=[]
	n=[]
	company=[]
	for i in range(len(lis)):
		send=[]
		some=db((db.bus_trips.name==lis[i])&(db.bus_trips.src==request.args(0))).select()
		if len(some):
			send.append(some[0].id)
			desti=some[0].dest
			m=some[0].seats
			p=some[0].price
			dtime.append(some[0].departure)
			while desti!=request.args(1):
				some=db((db.bus_trips.name==lis[i])&(db.bus_trips.src==desti)).select()
				if len(some):	
					desti=some[0].dest
					if some[0].seats<m:
						m=some[0].seats
					p+=some[0].price
					send.append(some[0].id)
				else:
					session.flash="No trips Found!"
					redirect(URL('index'))
			atime.append(some[0].arrival)
			n.append(send)
			logo.append(some[0].logo)
			company.append(some[0].company)
			seats.append(m)
			price.append(p)
		else:
			session.flash="No trips found!"
			redirect(URL('bus_booking'))
	new=[]
	for i in n:
		st=""
		for j in i:
			st+=str(j)
			st+='_'
		new.append(st[0:-1])
	return dict(lis=lis,seats=seats,new=new,price=price,dtime=dtime,atime=atime,logo=logo,company=company)

def bus_confirm():
	print session.date
	return dict()	


from gluon.tools import Mail
mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'Traveller\'s paradise'
mail.settings.login = 'ayushkhandelwal115@gmail.com:ayush115'
def bus_book():
	n=request.vars.send
	n=request.vars.send.split('_')
	red=db(db.bus_trips.name==request.vars.lis).select()
	for i in range(len(n)):
		seats=db(db.bus_trips.id==n[i]).select()
		seat=seats[0].seats
		db(db.bus_trips.id==n[i]).update(seats=seat-int(request.vars.seats))
	db.bus_bookings.insert(user_id=auth.user.id,num=request.vars.seats,d=session.date,arrival=request.vars.atime,depart=request.vars.dtime,lis=request.vars.send,price=request.vars.price,booked_in=request.vars.lis,src=request.vars.src,dest=request.vars.dest)
	email=auth.user.email
	mail.send(to=[email],
			subject='Ticket booked!',
			message='Bus id :'+request.vars.lis+'\nDeparture time : '+request.vars.dtime+'\nArrival time : '+request.vars.atime+'\nNumber of seats : '+request.vars.seats+'\n')
	session.flash="Your ticket has been booked!"
	redirect(URL('index'))

@auth.requires_login()	
def manage():
	if (auth.user.Member_Type!='admin'):
		redirect (URL('index'))
		session.flash('Only the site adin can access this page!')
	form=SQLFORM(db.trips)
	if form.accepts(request.vars,session):
		session.flash="something"
		redirect(URL('manage'))
	form2=SQLFORM(db.hotels)
	if (form.accepts(request.vars,session)):
		session.flash="Hotel added!!Good Work"
		redirect(URL('manage'))
	form3=SQLFORM(db.places)
	if (form.accepts(request.vars,session)):
		session.flash="New Place added in the database!(y)"
		redirect(URL('manage'))
	return dict(form=form,form2=form2,form3=form3)

import urllib
import json
from pprint import pprint
import datetime
def hotel_search():
	session.var=4
	form=SQLFORM.factory(
		Field('city',requires=IS_IN_DB(db,db.places.body)),
		Field('arrivalDate','date'),
		Field('departDate','date'),
		Field('rooms','integer',requires=IS_IN_SET((1,2,3,4,5))))
	if form.accepts(request.vars,session):
		arrivalDate=form.vars.arrivalDate
		departDate=form.vars.departDate
#		arrivalDate=str(form.vars.arrivalDate.strftime("%m/%d/%Y"))
#		departDate=str(form.vars.departDate.strftime("%m/%d/%Y"))
		redirect(URL(r=request,f='hotel',args=(form.vars.city,form.vars.arrivalDate,form.vars.departDate,form.vars.rooms)))
	return dict(form=form)


import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
	return TAG_RE.sub('', text)


def hotel_desc():
	session.var=4
	arrivalDate=request.args(1).split('-')
	departDate=request.args(2).split('-')
	adate=arrivalDate[1]+'/'+arrivalDate[2]+'/'+arrivalDate[0] 
	ddate=departDate[1]+'/'+departDate[2]+'/'+departDate[0] 
	rooms=""
	for i in range(0,int(request.args(3))):
		rooms+="&room"+str(i+1)+"=2"
	link="http://api.ean.com/ean-services/rs/hotel/v3/avail?&cid=55505&apiKey=nmtccjsdemu6hkg73wcct44t&locale=en_US&currencyCode=INR&hotelId="+request.args(0)+"&arrivalDate="+adate+"&departureDate="+ddate+"&includeDetails=true&includeRoomImages=true"+rooms
	link2="http://api.ean.com/ean-services/rs/hotel/v3/info?cid=55505&apiKey=nmtccjsdemu6hkg73wcct44t&locale=en_US&currencyCode=INR&xml=<HotelInformationRequest><hotelId>"+request.args(0)+"</hotelId><options>0</options></HotelInformationRequest>"
	a=urllib.urlopen(link)
	data=json.loads(a.read())
	a=urllib.urlopen(link2)
	data2=json.loads(a.read())
	hotel=data['HotelRoomAvailabilityResponse']
	li=data['HotelRoomAvailabilityResponse']['HotelRoomResponse']
	desc=data2['HotelInformationResponse']['HotelDetails']['propertyDescription']
	rooms=data2['HotelInformationResponse']['RoomTypes']
	return dict(li=li,hotel=hotel,rooms=rooms,desc=desc)	

@auth.requires_login()
def profile():
	rec=db(auth.user.id==db.auth_user.id).select()
	form=crud.update(db.auth_user,auth.user.id)
	crud.settings.update_deletable = False
	if (form.process().accepted):
		redirect(URL('profile'))
	return locals()

@auth.requires_login()
def viewbookings():
        print auth.user.id
        ctr1=0
        ctr2=0
        c1=0
        c2=0
        import datetime
        d1=datetime.date.today()
        rec=db(db.hotels.user_id==auth.user.id).select(db.hotels.ALL,orderby=db.hotels.checkin)
        flag1=0
        flag2=0
        f1=0
        f2=0
        print len(rec),
        print 'dad'
        print ctr1
        for i in range(len(rec)):
                print 'i m hrer'
                if ((rec[i]['checkin']-d1)<datetime.timedelta(0)):
                        ctr1=ctr1+1 
                elif ((rec[i]['checkin']-d1)>=datetime.timedelta(0)):
                        c1=c1+1
        if (ctr1==0):
                flag1=1
        if (c1==0):
                f1=1
        print flag1
        flight=db(db.flight_bookings.user_id==auth.user.id).select(db.flight_bookings.ALL,orderby=db.flight_bookings.d)
        for i in range(len(flight)):
                if ((flight[i]['d']-d1)<datetime.timedelta(0)):
                        ctr2=ctr2+1 
                if ((flight[i]['d']-d1)>=datetime.timedelta(0)):
                        c2=c2+1
        if (ctr2==len(flight)):
                flag2=1
        if (c2==len(flight)):
                f2=1
        return locals()

def cheap():
        getcheap=db().select(db.trips.ALL,orderby=~db.trips.price)
        sr=""
        de=""
        gc=db((db.trips.src==sr) & (db.trips.dest==de)).select(db.trips.ALL,orderby=~db.trips.price)
        return locals()

def hotel():
	session.var=4
	rooms=""
	adate=""
	ddate=""
	for i in range(0,int(request.args(3))):
		rooms+="&room"+str(i+1)+"=2"
	arrivalDate=request.args(1).split('-')
	departDate=request.args(2).split('-')
	adate=arrivalDate[1]+'/'+arrivalDate[2]+'/'+arrivalDate[0] 
	ddate=departDate[1]+'/'+departDate[2]+'/'+departDate[0] 
	link="http://api.ean.com/ean-services/rs/hotel/v3/list?cid=55505&apiKey=nmtccjsdemu6hkg73wcct44t&locale=en_US&currencyCode=INR&city="+request.args(0)+"&countryCode=IN&supplierCacheTolerance=MED&arrivalDate="+adate+"&departureDate="+ddate+rooms+"&numberOfResults=10&supplierCacheTolerance=MED_ENHANCED"
	a=urllib.urlopen(link)
	data=json.loads(a.read())
	li=data["HotelListResponse"]["HotelList"]["HotelSummary"]
	return dict(li=li,rooms=rooms)

def hotel_confirm():
	session.var=4
	arrivalDate=request.args(1).split('-')
	departDate=request.args(2).split('-')
	adate=arrivalDate[1]+'/'+arrivalDate[2]+'/'+arrivalDate[0] 
	ddate=departDate[1]+'/'+departDate[2]+'/'+departDate[0] 
	rooms=""
	for i in range(0,int(request.args(3))):
		rooms+="&room"+str(i+1)+"=2"
	link="http://api.ean.com/ean-services/rs/hotel/v3/avail?&cid=55505&apiKey=nmtccjsdemu6hkg73wcct44t&locale=en_US&currencyCode=INR&hotelId="+request.args(0)+"&arrivalDate="+adate+"&departureDate="+ddate+"&includeDetails=true&includeRoomImages=true"+rooms
	a=urllib.urlopen(link)
	data=json.loads(a.read())
	hotel=data['HotelRoomAvailabilityResponse']
	li=hotel['HotelRoomResponse']
	fin=[]
	for i in range(len(li)):
		if str(li[i]['roomTypeCode'])==str(request.args(4)):
			fin=li[i]
			break
	return dict(hotel=hotel,fin=fin)

@auth.requires_login()
def booking_done():
	session.var=4
	db.hotels.insert(user_id=str(auth.user.id),checkin=request.args(1),checkout=request.args(2),hotel_code=request.args(0),room_code=request.args(4),rooms=request.args(3))
	redirect(URL('index'))
	return dict()

def add_flight():
	cities=db(db.places.id>0).select(db.places.body)
	return dict(cities=cities)

def add_new():
	a=type("")
	src=request.vars.src
	dest=request.vars.dest
	price=request.vars.price
	atime=request.vars.arrival
	dtime=request.vars.depart
	day=request.vars.day
	tmp=[]
	if type(src)==a:
		print 'yes'
		tmp.append(src)
		src=tmp
		tmp=[]
		tmp.append(dest)
		dest=tmp
		tmp=[]
		tmp.append(price)
		price=tmp
		tmp=[]
		tmp.append(atime)
		atime=tmp
		tmp=[]
		tmp.append(dtime)
		dtime=tmp
		tmp=[]
		tmp.append(day)
		day=tmp
	print src
	print dest
	print atime
	print dtime
	seatseconomy=int(request.vars.seatseconomy)
	seatsbusiness=int(request.vars.seatsbusiness)
	date=datetime.datetime.strptime(request.vars.d,"%Y-%m-%d")
	day_len=len(day)
	to=datetime.date.today()
	delta=datetime.timedelta(days=1)
	while(day_len):
		if to.weekday() in day:
			add_date.append(to)
		to+=delta
		day_len-=1
	add_date=[]
	if seatseconomy:
	  	tmp=add_date
	  	for k in range(52):
	  		for j in tmp:
				for i in range(len(src)):
					db.trips.insert(src=src[i],dest=dest[i],d=date,price=price[i],departure=dtime[i],arrival=atime[i],cl='Economy',seats=seatseconomy,company=request.vars.company,name=request.vars.name)
			for j in tmp:
				tmp[j]+=datetime.timedelta(days=7)
	if seatsbusiness:
		for k in range(52):
			tmp=add_date
			for j in tmp:
				for i in range(len(src)):
					db.trips.insert(src=src[i],dest=dest[i],d=date,price=price[i],departure=dtime[i],arrival=atime[i],cl='Business',seats=seatsbusiness,company=request.vars.company,name=request.vars.name)
			for j in tmp:
				tmp[j]+=datetime.timedelta(days=7)
	return dict()
def recent():
        fl=db().select(db.flight_booking.ALL,orderby=~db.flight_booking.ALL)
        ht=db().select(db.flight_booking.ALL,orderby=~db.flight_booking.ALL)
        return locals()

from random import randint
def advertisement():
        fl=db().select(db.trips.ALL)
        l=len(fl)
        flnum=randint(0,l)
        ht=db().select(db.trips.ALL)
        lh=len(ht)
        htnum=randint(0,lh)
        return locals()

def dum():
#       print "DADSDAS"
        print "id=",
        print int(request.args[1])
        if (int(request.args[0])==1):
                db(db.hotels.id==int(request.args[1])).delete()
                email=auth.user.email
	        mail.send(to=[email],
			        subject='Hotel Cancellation',
			        message='You have Cancelled your booking for the hotel'+str(request.args[3])+'which was booked from'+str(request.args[1])+'to'+str(request.args[2])+'. TheAmount after cutting the cancelation prices will be transfered to you.' 
                        )
        elif (int(request.args[0])==0):
                q=db((db.flight_bookings.id==int(request.args[1]))).select()
                a=q[0]['lis'].split('_')
                #print a[0]+'ds'+a[1],
                #print len(a)
                for i in range(len(a)):
                        s= db(db.trips.id==int(a[i])).select(db.trips.seats)
                        db(db.trips.id==int(a[i])).update(seats=s[0]['seats']+int(request.args[3]))
                db(db.flight_bookings.id==int(request.args[1])).delete()
                email=auth.user.email
	        mail.send(to=[email],
			        subject='Flight Cancellation',
			        message='Your flight booking for '+q[0]['booked_in']+' from '+q[0]['src']+' to '+q[0]['dest']+' on '+str(q[0]['d'])+' has been cancelled.'   
                        )

        redirect(URL('viewbookings'))
        
        return locals()

@auth.requires_login()
def profile():
	rec=db(auth.user.id==db.auth_user.id).select()
	form=crud.update(db.auth_user,auth.user.id)
	crud.settings.update_deletable = False
	if (form.process().accepted):
		redirect(URL('profile'))
	return locals()

@auth.requires_login()
def flight_review():
        form=SQLFORM(db.review)
        form.vars.user_id=auth.user.id
        if (form.process().accepted):
                f=form.vars.id
                rec=db((db.trips.name==form.vars.flight_name)).select(db.trips.Rating)
                count=db(db.review.flight_name==form.vars.flight_name).select()
                print 'dsads',
                print rec[0]['Rating']
                c=float(len(count))
                print c
                x=float((float(form.vars.rating)+(float(rec[0]['Rating'])*(c-1)))/c)
                print x,
                print 'here',
                print x
                if (c<=0):
                        db((db.trips.name==form.vars.flight_name)).update(Rating=(rec[0]['Rating']+((int(form.vars.rating)))))
                else:
                        db((db.trips.name==form.vars.flight_name)).update(Rating=x)
        return locals()

@auth.requires_login()
def viewbookings():
        print auth.user.id
        ctr1=0
        ctr2=0
        c1=0
        c2=0
        import datetime
        d1=datetime.date.today()
        rec=db(db.hotels.user_id==auth.user.id).select(db.hotels.ALL,orderby=db.hotels.checkin)
        flag1=0
        flag2=0
        f1=0
        f2=0
        print len(rec),
        print 'dad'
        print ctr1
        for i in range(len(rec)):
                print 'i m hrer'
                if ((rec[i]['checkin']-d1)<datetime.timedelta(0)):
                        ctr1=ctr1+1 
                elif ((rec[i]['checkin']-d1)>=datetime.timedelta(0)):
                        c1=c1+1
        if (ctr1==0):
                flag1=1
        if (c1==0):
                f1=1
        print flag1
        flight=db(db.flight_bookings.user_id==auth.user.id).select(db.flight_bookings.ALL,orderby=db.flight_bookings.d)
        for i in range(len(flight)):
                if ((flight[i]['d']-d1)<datetime.timedelta(0)):
                        ctr2=ctr2+1 
                if ((flight[i]['d']-d1)>=datetime.timedelta(0)):
                        c2=c2+1
        if (ctr2==len(flight)):
                flag2=1
        if (c2==len(flight)):
                f2=1
        return locals()
import re
import os
import bs4
from bs4 import BeautifulSoup
from mechanize import Browser
browser=Browser()
soup=''
def railway():
        session.var=2
	form=SQLFORM.factory(
			Field('From',requires=IS_IN_DB(db,db.rail.body)),
			Field('To',requires=IS_IN_DB(db,db.rail.body)),
			Field('d','date',label='Date of journey',requires=IS_DATE()))
        if form.accepts(request.vars,session):
            if form.vars.From == form.vars.To:
                session.flash="Source and Destination should not be the same!"
                redirect(URL('index'))
            if form.vars.d<datetime.date.today():
                session.flash="Enter a valid date!"
                redirect(URL('index'))
            else:
                redirect(URL(r=request,f='rail',args=(form.vars.From,form.vars.To,form.vars.d)))
        return dict(form=form)
def rail():
        browser.open("http://www.indianrail.gov.in/know_Station_Code.html")
        browser.select_form(nr=0)
        browser.set_all_readonly(False)
        source=request.args(0).split('_')
        browser['lccp_src_stncode_dis']=str(source[-1])
        browser['lccp_src_stncode']=str(source[-1])
        dest=request.args(1).split('_')
        browser['lccp_dstn_stncode_dis']=str(dest[-1])
        browser['lccp_dstn_stncode']=str(dest[-1])
        
        

        browser['lccp_classopt']=['ZZ']
        p=request.args(2).split('-')
        browser['lccp_day']=str(p[2])
        browser['lccp_month']=str(p[1])
        response=browser.submit()
        content=response.read()
       # print content
        f=''
        trains=re.findall('<INPUT TYPE=.*>.*</TR>',content,re.DOTALL)
        for f in trains:
              f=f.replace('lccp_class2','lccp_class1')
              f=f.replace('lccp_class3','lccp_class1')
              f=f.replace('lccp_class4','lccp_class1')
              f=f.replace('lccp_class5','lccp_class1')
              f=f.replace('lccp_class6','lccp_class1')
              f=re.sub('<input name=.*?/>','✔',str(f))
              f=re.sub('<input checked=.*?/>','✔',str(f))
        soup=BeautifulSoup(f)
        soup=re.sub('<input name=.*?/>','✔',str(soup))
        soup=re.sub('<input checked=.*?/>','✔',str(soup))
        soup=re.sub('<input name=.*?/>','✔',str(soup))
        a=re.findall('<td>✔\d+</td>',soup)
        q=[]
        for i in a:
            q.append(eval(((re.findall('\d+',i))[0])))
        #soup=re.sub('✔[^\\n]',' ',str(soup))
        soup=BeautifulSoup(soup)
        soup=soup.table
        if str(soup)=="None":
            redirect(URL('railway'))
            session.flash="no trains found"
        form2=SQLFORM.factory(
                Field('trainno',label='Train Number',requires=IS_IN_SET(q)),
                Field('Class',requires=IS_IN_SET(['1A','2A','3A','CC','3E','SL','2S'])))
        qwe=""
        if form2.accepts(request.vars,session):
            ab=[]
            ab.append(form2.vars.Class)
            qwe=""
            for i in q:
                qwe+=str(i)
                qwe+=' '
            print qwe
            redirect(URL(r=request,f='fare',args=(form2.vars.trainno,str(p[2]),str(p[1]),str(source[-1]),str(dest[-1]),form2.vars.Class,'30','ZZZZZZ',qwe[0:-1])))
        return dict(soup=soup,q=q,form2=form2)

def fare():
        br=Browser()
        br.open("http://www.indianrail.gov.in/fare_Enq.html")
        br.select_form(nr=0)
        ab=[]
        ab.append(request.args(5))
        br.set_all_readonly(False)
        br['lccp_trnno']=str(request.args(0))
        br['lccp_day']=str(request.args(1))
        br['lccp_month']=str(request.args(2))
        br['lccp_srccode']=str(request.args(3))
        br['lccp_dstncode']=str(request.args(4))
        br['lccp_classopt']=ab
        br['lccp_age']=['30']
        br['lccp_conc']=['ZZZZZZ']
        response=br.submit()
        content=response.read()
        a=re.findall('<TR class="heading_table_top">.*</TABLE>',content,re.DOTALL)
        for f in a:
            w=1
        soup1=BeautifulSoup(f)
        soup1=soup1.table
        qwer=request.args(0).split(' ')
        form=SQLFORM.factory(
                    Field('t',label='Train Schedule',requires=IS_IN_SET(qwer)))
        if form.accepts(request.vars,session):
                       redirect(URL(r=request,f='route',args=(form.vars.t)))
        return dict(soup1=XML(soup1),a=request.args(0))
def route():
        br=Browser()
        br.open("http://www.indianrail.gov.in/inet_trn_num.html")
        br.select_form(nr=0)
        br.set_all_readonly(False)
        br['lccp_trnname']=str(request.vars.a)
        response=br.submit()
        content=response.read()
        route=re.findall('<TR class="heading_table_top">.*</TABLE>',content,re.DOTALL)
        f=''
        for f in route:
            a=1
        soup=BeautifulSoup(f)
        soup=soup.table
        return dict(soup=soup)
