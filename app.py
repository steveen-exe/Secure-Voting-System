import csv
from urllib import response
from flask import Flask, render_template,request,session,g,jsonify
import mysql.connector

import cv2
import numpy as np
from PIL import Image,ImageTk
from datetime import datetime, timedelta

import time


import os
 


current_date = datetime.now()
today = current_date.strftime("%Y-%m-%d")
ctime = current_date.strftime("%H")

tom = current_date + timedelta(days=2)

# Convert tomorrow's date to the desired format
tommorow = tom.strftime('%Y-%m-%d')

print(today,ctime)
app = Flask(__name__)


app.secret_key = 'votingmate'

config = {
    'user': 'root',
    'password': 'toor',
    'host': 'localhost',
    'database': 'onlinevoting',
}

def insert_record(query,data):
	cnx = mysql.connector.connect(**config)
	crsr = cnx.cursor()
	crsr.execute(query, data)

	cnx.commit()
	crsr.close()
	cnx.close()	


def update_record(query, data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(query, data)

    cnx.commit()
    cursor.close()
    cnx.close()


def select_records(query):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return rows



def count_records(query):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return len(rows)




# -----------------Common Functions--------------------


@app.route("/")
def index():
	return render_template("index.html")
	

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/logaction",methods=["POST"])
def logaction():
	email=request.form['email']
	password=request.form['password']


	sql5="select * from login where email='"+email+"' and password='"+password+"'"

	data=select_records(sql5)
	if len(data)>0:
		status=data[0][2]
		usertype=data[0][3]
		if(usertype=='0'):
			
			
			return '''
							<script>
							alert('Admin Login Successful!');
							window.location.href = '/admin/';
							</script>
		
		
								'''
        

			
		elif(usertype=='1'):
			
			if(status=='1'):
				session['email'] = email

				sql4="select * from registration where email='"+email+"'"


				data=select_records(sql4)

				session['user']=data[0]

					
				return '''

							<script>
							alert('Student Login Successful!');
							window.location.href = '/user/';
							</script>
							'''

			    
			else:
					
				return '''
							<script>
							alert('Student inactive');
							window.location.href = '/';
							</script>
							'''
		else:
			return '''
							<script>
							alert('Invalid!');
							window.location.href = '/';
							</script>
							'''
	else:
		return '''
							<script>
							alert('Login Failed! Email and password doesnt matched');
							window.location.href = '/';
							</script>


					'''

@app.route("/user/")
def userindex():

	email=session['email']


	count=[]
	sql1="select * from contest where cid in (select cid from electoralroll e,registration r where e.admno=r.admno and r.email='"+email+"')"
	count.append(count_records(sql1))

	sql2="select * from candidates e,registration r where e.admno=r.admno and r.email='"+email+"'"
	count.append(count_records(sql2))

	sql3="select * from electoralroll e,registration r where e.admno=r.admno and r.email='"+email+"' and e.candidateid != 0"
	count.append(count_records(sql3))

	sql4="select * from complaints where email='"+email+"'"
	count.append(count_records(sql4))

	sql6="SELECT * FROM complaints WHERE email='"+email+"' ORDER BY reply DESC,time ASC"
	data=select_records(sql6)



	return render_template("user/index.html",count=count,rows=data)	

@app.route("/admin/")
def adminindex():


	count=[]

	sql1="select * from login where status=1 and usertype=1"
	count.append(count_records(sql1))

	sql2="select * from contest"
	count.append(count_records(sql2))

	sql3="select * from candidates"
	count.append(count_records(sql3))

	sql4="select * from complaints"
	count.append(count_records(sql4))


	sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '0')"
	data=select_records(sql6)



	return render_template("admin/index.html",count=count,rows=data)
	
@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/regaction",methods=["POST"])
def regaction():

	fname=request.form['fname']
	lname=request.form['lname']
	email=request.form['email']
	admno=request.form['admno']
	phone=request.form['phone']
	dob=request.form['dob']
	branch=request.form['branch']
	sem=request.form['sem']
	rollno=request.form['rollno']
	dist=request.form['dist']
	address=request.form['address']
	city=request.form['city']
	state=request.form['state']
	pin=request.form['pin']
	course=request.form['course']
	gender=request.form['gender']
	password=request.form['password']
	cpassword=request.form['cpassword']


	sql4="select * from registration where email='"+email+"'or admno='"+admno+"'"


	data=select_records(sql4)
	if len(data)>0:
		return '''
							<script>
							alert('Registeration Failed! Try another email');
							window.location.href = '/';
							</script>
							'''
	else:
		
		if password == cpassword:
			# array=[fname,lname,email,admno,phone,dob,branch,sem,rollno,dist,city,pin,course,gender,password,cpassword]
			
			sql="INSERT INTO registration(email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state, district, city, pincode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			# sql = "INSERT INTO login(email, password, usertype) VALUES (%s,%s,%s)"

			data = (email, admno, fname, lname, dob, gender, rollno, sem, branch, course, phone, address, state, dist, city, pin)


			insert_record(sql,data)

		
			sql2 = "INSERT INTO login(email, password, status, usertype) VALUES(%s,%s,%s,%s)"
			data2 = (email, password, 0, 1)

			sql4="select max(stdid) from registration"
			data4=select_records(sql4)

			stdid=str(data4[0][0])

			insert_record(sql2,data2)
			face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

			def face_croped(img):
				# conver gary sacle
				gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				faces = face_classifier.detectMultiScale(gray,1.3,5)
				#Scaling factor 1.3
				# Minimum naber 5
				for (x,y,w,h) in faces:
					face_croped=img[y:y+h,x:x+w]
					return face_croped
			cap=cv2.VideoCapture(0)
			img_id=0
			while True:
				ret,my_frame=cap.read()
				if face_croped(my_frame) is not None:
					img_id+=1
					face=cv2.resize(face_croped(my_frame),(200,200))
					face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
					file_path="dataset/stdudent."+stdid+"."+str(img_id)+".jpg"
					cv2.imwrite(file_path,face)
					cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)       
					cv2.imshow("Capture Images",face)

				if cv2.waitKey(1)==13 or int(img_id)==100:
					break
			cap.release()
			cv2.destroyAllWindows()




			return '''
							<script>
							alert('Registered successfully!');
							window.location.href = '/';
							</script>
							'''


		else:
			return '''
						<script>
						alert('Password doesn't match');
						window.location.href = '/userhome';
						</script>
						'''

@app.route("/Register")
def register():
	return render_template("Register.html")

# -----------------Common Functions--------------------



# -----------------Admin Functions--------------------



@app.route("/userlist/")
def userlist():
	sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '1')"
	data=select_records(sql6)
	return render_template("admin/userlist.html",rows=data)

@app.route("/userverification/")
def userverification():
	sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '0')"
	data=select_records(sql6)
	return render_template("admin/userverification.html",rows=data)

@app.route("/suspended/")
def suspendeduser():
	sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '-2')"
	data=select_records(sql6)
	return render_template("admin/suspended.html",rows=data)

@app.route("/rejected/")
def rejecteduser():
	sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '-1')"
	data=select_records(sql6)
	return render_template("admin/rejected.html",rows=data)

@app.route("/viewcomplaint/")
def complaintuser():
	sql6="select * from complaints c , registration r where c.email = r.email and status = '0'"
	data=select_records(sql6)
	return render_template("admin/viewcomplaint.html",rows=data)

@app.route("/replyaction", methods=["POST"])
def replyaction():
    cmpid = request.form['cmpid']
    reply = request.form['reply']

    sql = "UPDATE complaints SET status = %s, reply = %s WHERE cmpid = %s"
    data = ('1', reply, cmpid)
    update_record(sql, data)

    return '''
        <script>
            alert('Replied!');
            window.location.href = '/viewcomplaint/';
        </script>
    '''


@app.route("/campaction",methods=["POST"])
def campaction():
	name=request.form['name']
	date=request.form['date']
	starttime=request.form['starttime']
	endtime=request.form['endtime']
	designation=request.form['designation']


	sql7= "INSERT INTO contest(name, date, starttime, endtime, designation) VALUES (%s,%s,%s,%s,%s)"

	data = (name, date, starttime, endtime, designation)

	insert_record(sql7,data)

	return '''
				<script>
				alert('Campaign Created Successfully!');
				window.location.href = '/upcomingcampaign/';
				</script>
				'''

@app.route("/activecampaign/")
def activecampaignindex():
	
	sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = 1 and date='"+today+"' and starttime<="+ctime+" and endtime>"+ctime+" ORDER BY date ASC;"
	data=select_records(sql8)	
	return render_template("admin/activecampaign.html",rows=data)

@app.route("/viewresults/",methods=['GET','POST'])
def viewresults():
	id = request.args['id']
	sql8="SELECT r.fname,r.lname,c.symbol,c.admno,count(*) FROM electoralroll e,candidates c,registration r WHERE e.cid='"+id+"' and e.candidateid in (select candidateid from candidates c where c.cid='"+id+"') and c.candidateid=e.candidateid and c.admno=r.admno GROUP by e.candidateid"
	data=select_records(sql8)	
	return render_template("admin/result.html",rows=data)



@app.route("/managecampaign/",methods=['GET','POST'])
def managecampaign():
	id = request.args['id']

	sql8="SELECT * FROM `contest` WHERE cid ='"+id+"';"
	data=select_records(sql8)
	
	sql9="SELECT * FROM registration r,candidates c WHERE c.admno=r.admno and cid ='"+id+"';"
	candidates=select_records(sql9)	

	sql3="SELECT * FROM registration r,electoralroll c WHERE c.admno=r.admno and c.cid ='"+id+"';"
	v=select_records(sql3)	

	return render_template("admin/managecampaign.html",rows=data[0],c=candidates,voters=v)


@app.route("/addcandidate",methods=["POST"])
def addcandidate():
	id=request.form['id']
	admno=request.form['admno']
	symbol = request.files['symbol']
	filename=symbol.filename
	file_extension = os.path.splitext(filename)[1]

	name=admno+str(id)+file_extension

	file_path = os.path.join('static/symbols', name)
	symbol.save(file_path)


	
	sql1="SELECT * FROM registration where admno ='"+admno+"' and email in (select email from login where status=1);"
	count=select_records(sql1)

	sql2="SELECT * FROM candidates where admno ='"+admno+"' and cid ='"+id+"';"
	cc=select_records(sql2)

	if(len(count)>0 and len(cc)<1):
		sql7= "INSERT INTO candidates(cid, admno,symbol) VALUES (%s,%s,%s)"

		data = (id, admno,name)

		insert_record(sql7,data)

		sql8="SELECT * FROM `contest` WHERE cid ='"+id+"';"
		data=select_records(sql8)
		

		sql9="SELECT * FROM registration r,candidates c WHERE c.admno=r.admno and cid ='"+id+"';"
		candidates=select_records(sql9)	

		return render_template("admin/managecampaign.html",rows=data[0],c=candidates)
	else:
		sql8="SELECT * FROM `contest` WHERE cid ='"+id+"';"
		data=select_records(sql8)	

		sql9="SELECT * FROM registration r,candidates c WHERE c.admno=r.admno and cid ='"+id+"';"
		candidates=select_records(sql9)	

		return render_template("admin/managecampaign.html",rows=data[0],c=candidates)

@app.route("/addvoter",methods=["POST"])
def addvoter():
	id=request.form['id']
	admno=request.form['admno']
	
	sql1="SELECT * FROM registration where admno ='"+admno+"' and email in (select email from login where status=1);"
	count=select_records(sql1)

	sql2="SELECT * FROM electoralroll where admno ='"+admno+"' and cid ='"+id+"';"
	cc=select_records(sql2)

	if(len(count)>0 and len(cc)<1):
		sql7= "INSERT INTO electoralroll(cid, admno) VALUES (%s,%s)"
		data = (id, admno)
		insert_record(sql7,data)
		
	sql8="SELECT * FROM `contest` WHERE cid ='"+id+"';"
	data=select_records(sql8)
	
	sql9="SELECT * FROM registration r,candidates c WHERE c.admno=r.admno and cid ='"+id+"';"
	candidates=select_records(sql9)	

	sql3="SELECT * FROM registration r,electoralroll c WHERE c.admno=r.admno and c.cid ='"+id+"';"
	v=select_records(sql3)	

	return render_template("admin/managecampaign.html",rows=data[0],c=candidates,voters=v)



@app.route("/addvoterfile",methods=["POST"])
def addvoterfile():
	id=request.form['id']
	file=request.files['csv']

	if file.filename == '':
		return jsonify({'error': 'No selected file'}), 400

	file.save(f'static/files/{file.filename}')

	data_list = []
	with open('static/files/'+file.filename, 'r', newline='') as csvfile:
		csv_reader = csv.reader(csvfile)
		header = next(csv_reader)  # Skip the header row
		for row in csv_reader:
			data_list.append(row)
    

	for row in data_list:
		sql1="SELECT * FROM registration where admno ='"+row[0]+"' and email in (select email from login where status=1);"
		count=select_records(sql1)

		sql2="SELECT * FROM electoralroll where admno ='"+row[0]+"' and cid ='"+id+"';"
		cc=select_records(sql2)

		if(len(count)>0 and len(cc)<1):
			sql7= "INSERT INTO electoralroll(cid, admno) VALUES (%s,%s)"
			data = (id, row[0])
			insert_record(sql7,data)
			
	sql8="SELECT * FROM `contest` WHERE cid ='"+id+"';"
	data=select_records(sql8)

	sql9="SELECT * FROM registration r,candidates c WHERE c.admno=r.admno and cid ='"+id+"';"
	candidates=select_records(sql9)	

	sql3="SELECT * FROM registration r,electoralroll c WHERE c.admno=r.admno and c.cid ='"+id+"';"
	v=select_records(sql3)	

	return render_template("admin/managecampaign.html",rows=data[0],c=candidates,voters=v)
		





	


@app.route("/upcomingcampaign/")
def upcomingcampaignindex():
	
	sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = 1 and ( (date>'"+today+"') or (date='"+today+"' and starttime>"+ctime+"))   ORDER BY date ASC;"
	data=select_records(sql8)	
	return render_template("admin/upcomingcampaign.html",rows=data,query=sql8)


@app.route("/completedcampaign/")
def completedcampaignindex():
	sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = 2 or ( (date<'"+today+"') or (date='"+today+"' and endtime<'"+ctime+"'))   ORDER BY date ASC;"
	data=select_records(sql8)
	return render_template("admin/completedcampaign.html",rows = data,query=sql8 )

@app.route("/inactivecampaign/")
def inactivecampaignindex():
	sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = -1 ORDER BY date ASC;"
	data=select_records(sql8)
	return render_template("admin/inactivecampaign.html",rows = data)

@app.route("/campaign/")
def campaignindex():
	sql8="select * from time;"
	time=select_records(sql8)
	return render_template("admin/campaign.html",time = time,dat=tommorow)

@app.route("/markascomplete/",methods=['GET','POST'])
def markascomplete():
	if request.method=='GET':
		
		id = request.args['id']
		
		sql7="UPDATE contest set status=%s where cid=%s"
		data=(2,id)
		update_record(sql7, data)

		sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = 2 or ( (date<'"+today+"') or (date='"+today+"' and endtime>'"+ctime+"'))   ORDER BY date ASC;"
		data=select_records(sql8)
		return render_template("admin/completedcampaign.html",rows = data)
	else:
		sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = 2 or ( (date<'"+today+"') or (date='"+today+"' and endtime>'"+ctime+"'))   ORDER BY date ASC;"
		data=select_records(sql8)
		return render_template("admin/completedcampaign.html",rows = data)

@app.route("/rejectcampaign/",methods=['GET','POST'])
def rejectcampaign():
	if request.method=='GET':
		
		id = request.args['id']
		
		sql7="UPDATE contest set status=%s where cid=%s"
		data=(-1,id)
		update_record(sql7, data)

		sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = -1 ORDER BY date ASC;"
		data=select_records(sql8)
		return render_template("admin/inactivecampaign.html",rows = data)
	else:
		sql8="SELECT `cid`, `name`, `date`, `starttime`, `endtime`, `status`, `designation` FROM `contest` WHERE status = -1 ORDER BY date ASC;"
		data=select_records(sql8)
		return render_template("admin/inactivecampaign.html",rows = data)




@app.route("/suspenduser/",methods=['GET','POST'])
def suspenduser():
	if request.method=='GET':
		status = request.args['status']
		user = request.args['id']
		
		sql7="UPDATE login set status=%s where email=%s"
		data =(status,user)
		update_record(sql7, data)

		sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '1')"
		data=select_records(sql6)
		return render_template("admin/userlist.html",rows=data)
	else:
		sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '1')"
		data=select_records(sql6)
		return render_template("admin/userlist.html",rows=data)


@app.route("/userverify/",methods=['GET','POST'])
def userverify():
	if request.method=='GET':
		status = request.args['status']
		user = request.args['id']

		sql7="UPDATE login set status=%s where email=%s"
		data =(status,user)
		update_record(sql7, data)
		
		data_dir=("dataset")
		path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]
		faces=[]
		ids=[]
		for image in path:
			img=Image.open(image).convert('L') # conver in gray scale 
			imageNp = np.array(img,'uint8')
			id=int(os.path.split(image)[1].split('.')[1])
			faces.append(imageNp)
			ids.append(id)
			
		ids=np.array(ids)
		print(ids)
		print("hello")
		
		#=================Train Classifier=============
		clf= cv2.face.LBPHFaceRecognizer_create()
		clf.train(faces,ids)
		clf.write("clf.xml")
		
		

		sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '1')"
		data=select_records(sql6)
		return render_template("admin/userlist.html",rows=data)
	else:
		sql6="SELECT stdid, email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM `registration` WHERE `email` IN (SELECT `email` FROM `login` WHERE `status` = '1')"
		data=select_records(sql6)
		return render_template("admin/userlist.html",rows=data)

# -----------------------------admin-------------------------







# -----------------User Functions--------------------




@app.route("/complaintaction",methods=["POST"])
def complaintaction():
	title=request.form['title']
	subject=request.form['subject']
	email=session['email']



	sql7= "INSERT INTO complaints(title,content,email) VALUES (%s,%s,%s)"

	data = (title, subject,email)

	insert_record(sql7,data)

	return '''
				<script>
				alert('Complaint submitted!');
				window.location.href = '/mycomplaint/';
				</script>
				'''

@app.route("/mycomplaint/")
def mycomplaints():
	email=session['email']
	sql6="SELECT * FROM complaints WHERE email='"+email+"' ORDER BY reply DESC,time ASC"
	data=select_records(sql6)
	

	

	return render_template("user/mycomplaint.html",rows=data)

@app.route("/profile/")
def profile():
	email=session['email']
	sql6="SELECT email, admno, fname, lname, dob, gender, rollno, semester, branch, course, phn, address, state FROM registration WHERE email='"+email+"'"
	data=select_records(sql6)
	return render_template("user/profile.html",rows=data[0])

@app.route("/update_profile",methods=["POST"])
def update_profile():
	email=session['email']

	# admno = session['admno']
	fname=request.form['fname']
	lname=request.form['lname']
	dob=request.form['dob']
	gender=request.form['gender']
	rollno=request.form['rollno']
	sem=request.form['sem']
	branch=request.form['branch']
	course=request.form['course']
	phone=request.form['phone']
	# sql7="UPDATE registration set fname='"+fname+"'lname='"+lname+"'dob='"+dob+"'gender='"+gender+"'rollno='"+rollno+"'semester='"+sem+"'branch='"+branch+"'course='"+course+"'phone='"+phone+"' where email='"+email+"'"
	sql7="UPDATE registration set fname=%s,lname=%s,dob=%s,gender=%s,rollno=%s,semester=%s,branch=%s,course=%s,phn=%s where email=%s"
	data =(fname, lname, dob, gender, rollno, sem, branch, course, phone,email)


	update_record(sql7, data)
	return '''
						<script>
						alert('Profile Updated Successfully!!');
						window.location.href = '/profile/';
						</script>
						'''
@app.route("/activecontest/")
def activecontestindex():
	user=session['user']
	admno=user[2]

	print(ctime)
	sql8="SELECT cid, name, date, starttime, endtime, status, designation FROM contest WHERE status = 1 and date='"+today+"' and starttime<="+ctime+" and endtime>"+ctime+" and cid in (select cid from electoralroll where admno='"+admno+"' and candidateid = 0) ORDER BY date ASC"
	print(sql8)
	data1=select_records(sql8)

	# sql2="SELECT cid, name, date, starttime, endtime, status, designation FROM contest WHERE status = 1 and date='"+today+"' and starttime<'"+ctime+"' and endtime>'"+ctime+"' and cid in (select cid from electoralroll where admno='"+admno+"' and candidateid = 0) ORDER BY date ASC"
	# data2=select_records(sql2)
	
	return render_template("user/activecontest.html",rows=data1)

@app.route("/completedcontest/")
def completedcontestindex():
	user=session['user']
	admno=user[2]
	sql8="SELECT cid, name, date, starttime, endtime, status, designation  FROM contest WHERE (status = 2) OR (date < '"+today+"' OR (date = '"+today+"' AND endtime < "+ctime+"))OR (cid IN (SELECT cid FROM electoralroll WHERE candidateid != 0 AND admno ='"+admno+"')) ORDER BY date ASC"	
	data1=select_records(sql8)

	return render_template("user/completedcontest.html",rows=data1)


@app.route("/upcomingcontest/")
def upcomingcontestindex():
	user=session['user']
	admno=user[2]
	sql8="SELECT cid, name, date, starttime, endtime, status, designation FROM contest WHERE status = 1 and ( (date>'"+today+"') or (date='"+today+"' and starttime>"+ctime+")) and cid in (select cid from electoralroll where admno='"+admno+"' and candidateid = 0) ORDER BY date ASC"
	data1=select_records(sql8)

	# sql2="SELECT cid, name, date, starttime, endtime, status, designation FROM contest WHERE status = 1 and date='"+today+"' and starttime<'"+ctime+"' and endtime>'"+ctime+"' and cid in (select cid from electoralroll where admno='"+admno+"' and candidateid = 0) ORDER BY date ASC"
	# data2=select_records(sql2)
	
	return render_template("user/upcomingcontest.html",rows=data1)

@app.route("/addcomplaint/")
def addcomplaintindex():
	return render_template("user/addcomplaint.html")

@app.route("/detectface/",methods=['GET','POST'])
def detectfaceindex():
	user=session['user']
	id=user[0]
	cid= request.args['id']

	faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	clf=cv2.face.LBPHFaceRecognizer_create()
	clf.read("clf.xml")

	start_time = time.time()

	videoCap=cv2.VideoCapture(0)

	while True:
		ret,img=videoCap.read()
		data=recognize(img,clf,faceCascade)
		cv2.imshow("Face Detector",data[0])
		print(data[1])
		if data[1]==True:
			time.sleep(10)

			videoCap.release()
			cv2.destroyAllWindows()

			return "<script>alert('Face verification Successfully!!');window.location.href = '/gotovote?id="+cid+"';</script>"

		elapsed_time = time.time() - start_time
		if elapsed_time>10:
			

			videoCap.release()
			cv2.destroyAllWindows()

			return '''
						<script>
						alert('Time Out..!! Contact Admin about the same');
						window.location.href = '/activecontest/';
						</script>
						'''

		if cv2.waitKey(1) == 27:
			

			videoCap.release()
			cv2.destroyAllWindows()

			return '''
						<script>
						alert('Time Out..!! Contact Admin about the same');
						window.location.href = '/activecontest/';
						</script>
						'''


	


@app.route("/gotovote/",methods=['GET','POST'])
def gotovote():
	user=session['user']
	id=user[0]
	cid= request.args['id']



	sql8="SELECT * from candidates c,registration r where r.admno=c.admno and c.cid='"+cid+"'"
	candidates=select_records(sql8)
	print(sql8)

	sql2="SELECT * from contest where cid='"+cid+"'"
	contest=select_records(sql2)


	return render_template("user/castvote.html",candidates=candidates,contest=contest[0])




@app.route("/markvote/",methods=['GET','POST'])
def markvote():
	user=session['user']
	admno=user[2]
	candidateid= request.args['id']
	cid= request.args['cid']

	sql7="UPDATE electoralroll set candidateid=%s where admno=%s and cid=%s"
	data=(candidateid,admno,cid)
	update_record(sql7, data)




	return '''
						<script>
						alert('Vote Casted Successfully!!');
						window.location.href = '/activecontest/';
						</script>
						'''





@app.route("/signout/")
def signout():
	session.clear()
	return render_template("login.html")

def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
	gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	featuers=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

	user=session['user']
	userid=user[0]

	flag=False


	coord=[]
	
	for (x,y,w,h) in featuers:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)#croping the face
		id,predict=clf.predict(gray_image[y:y+h,x:x+w])

		confidence=int((100*(1-predict/300)))

		

		# print(id==userid)

		if confidence > 80:
			if userid==id:
				flag=True
		

		coord=[x,y,w,y]
	
	return flag

def recognize(img,clf,faceCascade):
	flag=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
	return (img,flag)


    



# -------------------------------------------------------------



if __name__ == "__main__":
	app.run()
