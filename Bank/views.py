import smtplib,secrets  #Sending mail and OTP
from email.mime.text import MIMEText    #Sending mail
from email.mime.multipart import MIMEMultipart  #Sending mail
from django.contrib import messages
from django.shortcuts import render,redirect    #render & redirect the urls
from .models import tb_admin, tb_account, tb_customer   #Database
from .forms import captchaTester    #Captcha form
from datetime import date
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.http import Http404     #For the 404 error page

#------------------------------------------------------Captcha-------------------------------------------------------------

#Captcha Validater
def captchaValidate(request):
    if request.method == 'POST':
        form = captchaTester(request.POST)
        if form.is_valid():
            return {'valid' : True}
    else:
        form = captchaTester()
    context = {'form' : form,'valid' : False}
    return context       
    
#Function to send Mail
def send_mail(rmail,sub,body):
    smail = "ip.tracker.mailer@gmail.com"
    password = "iqtovoynrterpepv"
    msg=MIMEMultipart()
    msg["From"]=smail
    msg["To"]=rmail
    msg["Subject"]=sub
    msg.attach(MIMEText(body,"plain"))
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(smail,password)
    server.sendmail(smail,rmail,msg.as_string())
    server.quit()
    
#---------------------------------------------------------User---------------------------------------------------

#Function to the index page(starting page).
def index(request):
    return render(request,'index.html')

#Function to the netbaking page.
def netBanking(request):
    return render(request,'netBanking.html')

#Function to the about page.
def about(request):
    return render(request,'about.html')

#Function to the contact page.
def contact(request):
    return render(request,'contact.html')

#Function to the sign-up page.
def sign_up(request):
    return render(request,'sign-up.html')

#Function for authenticating the login details.
def user_sign_in(request):
    if request.method =="POST":
        try:
            key=tb_customer.objects.get(c_name=request.POST['cusId'],c_password=request.POST['password'])
            key_exists=True
            context={'key_exists':key_exists}
            request.session['UserName']=key.c_name
            return render(request,'index.html',context)
        except tb_customer.DoesNotExist as e:
            messages.success(request,'UserName/Password  invalid!!')
            return render(request,'about.html')
        
#Function for sign out button and follow to index page.
def user_sign_out(request):
    return render(request,'index.html')

#Function to the account page.
def account(request):

    return render(request,'account.html')


#-------------------------------------------------------Admin-------------------------------------------------------------

#Function for the 404 - Page not found.


#Function to the login page of admin(starting page).
def adminindex(request):
    return render(request,'Admin/index.html')

#Function for authenticating the login details and follow to the dashboard
def adminlogin(request):
    if request.method == "POST":
        adminId = request.POST.get('adminId')
        password = request.POST.get('Password')
        try:
            ad_data=tb_admin.objects.get(admin_id=adminId)
            if ad_data.admin_id == adminId and ad_data.password == password:
                request.session['adminId']=ad_data.admin_id
                return redirect('adminDashboard')
            else:
                messages.error(request,'Incorrect password. Please try again.')
                return redirect('admin')  
        except tb_admin.DoesNotExist as e:
            messages.error(request,"Admin ID doesn't exists.")
            return redirect('admin')
    else:
        return redirect("admin")
    
#Function for logout.
def adminlogout (request):
    del request.session['adminId']
    return redirect('admin')

#Function for redirect to forget password page.
def forgetpass(request):
    if request.method == 'POST':
        if request.POST.get('adminId'):
            adminId = request.POST.get('adminId')
            captcha_result = captchaValidate(request)
            if not captcha_result['valid']:
                messages.error(request,'Invalid captcha. Please try again.')
                context = captchaValidate(request)
                context['form1']="form1"
                return render(request, 'Admin/forgetPassword.html', context)
            try:
                ad_data = tb_admin.objects.get(admin_id=adminId)
                request.session['adminId'] = adminId
            except Exception as e:
                messages.error(request,"Admin ID doesn't exist. Please enter the valid ID.")
                context = captchaValidate(request)
                context['form1']="form1"
                return render(request,'Admin/forgetPassword.html',context)
            otp = str(secrets.randbelow(900000)+100000)
            request.session['otp']=otp
            mail_body = f"Hi {ad_data.admin_name},\n\nThe OTP for your password change request is {otp}\n\nBest Regards\nY Bank."
            mail_sub = "OTP For Password Change Request - Y Bank"
            try:
                send_mail(ad_data.ad_email,mail_sub,mail_body)
                context={'form2':'form2'}
                return render(request,'Admin/forgetPassword.html',context)
            except Exception as e:
                del request.session['otp']
                messages.error(request,f"Failed to send OTP. Please try again.\n{e}")
                return render(request,'Admin/forgetPassword.html',{'form1':'form1'})           
        elif request.POST.get('otpfield'):
            otp = request.session.get('otp')
            U_otp = request.POST.get("otpfield")
            if U_otp == otp:
                del request.session['otp']
                context={'form3':'form3'}
                return render(request,'Admin/forgetPassword.html',context)
            else:
                messages.error(request,"Incorrect OTP.")
                context={"form2":"form2"}
                return render(request,'Admin/forgetPassword.html',context)
        elif request.POST.get('newPass'):
            new_pass = request.POST.get("newPass")
            r_new_pass = request.POST.get("rNewPass")
            if new_pass == r_new_pass:
                adminId = request.session.get('adminId')
                ad_data = tb_admin.objects.get(admin_id=adminId)
                ad_data.password = new_pass
                ad_data.save()
                del request.session['adminId']
                return redirect('admin')
            else:
                messages.error(request,"Please enter the same password on both the fields")
                context={'form3':'form3'}
                return render(request,'Admin/forgetPassword.html',context)
    else:
        context = captchaValidate(request)
        context['form1']="form1"
        return render(request,'Admin/forgetPassword.html',context)
        
#Function to the dashboard page.
def dashboard(request):
    try:
        adminId = request.session.get('adminId')    
        ad_data = tb_admin.objects.get(admin_id=adminId)
        context = {
            'adminId' : ad_data.admin_id,
            'adminName' : ad_data.admin_name
        }
        return render(request,'Admin/dashboard.html',context)
    except Exception as e:
        return redirect('admin')

# Function to the add account page.
def add_account(request):
    tDay = date.today()
    currentYear = str(tDay.year)
    last_row=tb_account.objects.last()
    if last_row:
        last_id = last_row.account_id
        id_no = int(last_id[7:])
        id_no+=1
        newID = "AC"+ currentYear + "Y" + str(id_no)
    else:
        newID = "AC" + currentYear + "Y1" 
    context = {
            'newID': newID
        }
    
    return render(request,'Admin/addAccount.html',context)

#Function to insert account details.
def AddFiles(request):
    if request.method =='POST' and request.FILES:
    
        add_acc=tb_account()
        add_acc.account_id=request.POST.get('ActId')
        add_acc.customer_photo=request.FILES['Photo']
        add_acc.account_type=request.POST.get('ActType')
        add_acc.customer_name=request.POST.get('Name')
        add_acc.date_of_birth=request.POST.get('Birth')
        add_acc.aadhar_number=request.POST.get('Aadhar')
        add_acc.c_residence=request.POST.get('Residence')
        add_acc.c_phone_number=request.POST.get('Mobile')
        add_acc.c_email=request.POST.get('Mail')
        add_acc.opening_date=date.today()
        add_acc.branch_code=request.POST.get('BCode')
        add_acc.main_balance=request.POST.get('InDepo')
        add_acc.min_balance=500
        add_acc.co_name=request.POST.get('CoName')
        add_acc.co_relation=request.POST.get('CoRel')
        add_acc.co_idproof=request.FILES['CoProof']
        add_acc.co_residence=request.POST.get('CoResidence')
        
        default_storage.save("Photo", ContentFile(add_acc.customer_photo.read()))
        default_storage.save("CoProof", ContentFile(add_acc.co_idproof.read()))
#  the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
        add_acc.save()
        messages.success(request,'Details Added Successfully...!!!')
        return render(request,'Admin/dashboard.html')
    else:
        return render(request,'Admin/addAccount.html')