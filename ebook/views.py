from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import time 

from . import models
from . import emailAPI

def home(request):
    return render(request, 'home.html')  # Render the home template

def register(request):
    if request.method=="GET":    
        return render(request,"register.html",{"output":""})
    else:
        #to recieve from data
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        #to insert record in database
        p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
        p.save()

        #to send mail using api
        emailAPI.sendMail(email, password)

        return render(request,"register.html",{"output":"User register successfully."})    
        
def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)        
    return redirect("/login/")

def login(request):
    if request.method=="GET":
        return render(request,"login.html",{"output":""})
    else:
        #recieve data for login
        email=request.POST.get("email")
        password=request.POST.get("password")

        #to match user details in database
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userDetails)>0:
            #to store user details in session
            request.session["sunm"]=userDetails[0].email
            request.session["srole"]=userDetails[0].role
            # print(request.session["sunm"])
            
            #print(userDetails[0].role) #to get user role
            if userDetails[0].role=="admin":
                return redirect("/myadmin/")
            else:
                return redirect("/user/")                
        else:
            return render(request,"login.html",{"output":"Invalid user or verify your account."})

def adminhome(request):
    email = request.session.get("sunm")
    userDetails = models.Register.objects.filter(email=email).first()
    
    users=models.Register.objects.filter(role="user")
    totalusers = len(users)

    activeusers=models.Register.objects.filter(role="user", status="1")
    active = len(activeusers)
    
    inactiveusers=models.Register.objects.filter(role="user", status="0")
    inactive = len(inactiveusers)
    return render(request, "adminhome.html", {"userDetails" : userDetails, "totalusers":totalusers,"active":active,"inactive":inactive})    

def manageusers(request):
    #to fetch user details
    userDetails=models.Register.objects.filter(role="user")
    return render(request, "manageusers.html", {"userDetails" : userDetails})

def manageuserstatus(request):
    #to get status data from url
    s=request.GET.get("s")
    regid=int(request.GET.get("regid"))

    if s=="active":
        models.Register.objects.filter(regid=regid).update(status=1)
    elif s=="inactive":
        models.Register.objects.filter(regid=regid).update(status=0)    
    else:
        models.Register.objects.filter(regid=regid).delete()

    return redirect("/manageusers/")


def userhome(request):
    email = request.session.get("sunm")
    userDetails = models.Register.objects.filter(email=email).first()
    
    return render(request,"userhome.html", {"userDetails" : userDetails})

def sharenotes(request):
    if request.method=="GET":
        return render(request,"sharenotes.html",{"sunm":request.session.get("sunm"),"output":""})
    else:
        #to recieve data from UI
        title=request.POST.get("title")
        category=request.POST.get("category")
        description=request.POST.get("description")

        #to recieve file from UI & to push in media folder
        files=request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(files.name,files)
        
        sunm = request.session.get("sunm")
    
        p=models.Sharenotes(title=title,category=category,description=description,filename=filename,uid=sunm,info=time.asctime())
        p.save()

        return render(request,"sharenotes.html",{"sunm":sunm, "output":"Content uploaded successfully."})

def viewnotes(request):
    data=models.Sharenotes.objects.all()
    return render(request,"viewnotes.html",{"data":data})


def buynotes(request):
    paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID="sb-ptqqq43008250@business.example.com"
    amt=100
    return render(request,"buynotes.html",{"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})

def payment(request):
    uid=request.GET.get("uid")
    amt=request.GET.get("amt")
    p=models.Payment(uid=uid,amt=amt,info=time.asctime())
    p.save()
    return redirect("/success/")

def success(request):
    return render(request,"success.html")

def cancel(request):
    return render(request,"cancel.html")    

# Change Password for Admin
def cpadmin(request):
    if request.method=="GET":
        return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":""})
    else:
        #to get data from form
        email=request.session["sunm"]
        opassword=request.POST.get("oldpass")
        npassword=request.POST.get("newpass")
        cnpassword=request.POST.get("conpass")
        
        #to check old password is valid or not
        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":"Password changes successfully."})    
            else:    
                return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch."})                
        else:
            return render(request,"cpadmin.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again."})


# Change Password for Users
def cpusers(request):
    if request.method=="GET":
        return render(request,"cpusers.html",{"sunm":request.session["sunm"],"output":""})
    else:
        #to get data from form
        email=request.session["sunm"]
        opassword=request.POST.get("oldpass")
        npassword=request.POST.get("newpass")
        cnpassword=request.POST.get("conpass")
        
        #to check old password is valid or not
        userDetails=models.Register.objects.filter(email=email,password=opassword)
        if len(userDetails)>0:
            if npassword==cnpassword:
                models.Register.objects.filter(email=email).update(password=cnpassword)
                return render(request,"cpusers.html",{"sunm":request.session["sunm"],"output":"Password changes successfully."})    
            else:    
                return render(request,"cpusers.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch."})                
        else:
            return render(request,"cpusers.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again."})


# my profile admin view
def mpadmin(request):
    email = request.session.get("sunm")
    userDetails = models.Register.objects.filter(email=email).first()
    return render(request, "mpadmin.html", {"user" : userDetails})


# my profile user view
def mpusers(request):
    email = request.session.get("sunm")
    userDetails = models.Register.objects.filter(email=email).first()
    return render(request, "mpusers.html", {"user" : userDetails})

# edit profile admin
def epadmin(request):
    email = request.session.get("sunm")
    userDetails = models.Register.objects.filter(email=email)
    
    m,f="",""
    if userDetails[0].gender=="male":
        m="checked"
    else:        
        f="checked"
    
    if request.method=="GET":
        return render(request,"epadmin.html",{"sunm":email,"user":userDetails[0],"output":"","m":m,"f":f})
    else:
        #to get edited content
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        
        #to update data in database
        models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)   
        
        # return redirect("/epadmin/")   
        return render(request, "mpadmin.html", {"user" : userDetails[0]}) 


def epusers(request):
    email = request.session.get("sunm")
    userDetails = models.Register.objects.filter(email=email)
    
    m,f="",""
    if userDetails[0].gender=="male":
        m="checked"
    else:        
        f="checked"
    
    if request.method=="GET":
        return render(request,"epusers.html",{"sunm":email,"user":userDetails[0],"output":"","m":m,"f":f})
    else:
        #to get edited content
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        
        #to update data in database
        models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)   
        
        # return redirect("/epadmin/")   
        return render(request, "mpusers.html", {"user" : userDetails[0]}) 

def enquiry(request):
    if request.method=="GET":    
        return render(request,"home.html")
    else:
        #to recieve from data
        name=request.POST.get("name")
        email=request.POST.get("email")

        #to insert record in database
        p=models.Enquiry(name=name,email=email,info=time.asctime())
        p.save()

        return render(request,"home.html")
    
def viewenquiry(request):
    data=models.Enquiry.objects.all()
    return render(request,"viewenquiry.html",{"data":data})