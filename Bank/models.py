from django.db import models

# Create your models here.
class tb_admin(models.Model):
    admin_id=models.CharField(max_length=10, unique=True,primary_key=True)
    admin_name=models.CharField(max_length=50)
    password=models.CharField(max_length=30)
    ad_email=models.EmailField(unique=True)
    ad_phone=models.BigIntegerField(unique=True)
    class Meta:
        managed = True
        db_table="tb_admin"

class tb_account(models.Model):
    account_id=models.CharField(max_length=15,unique=True,primary_key=True)
    branch_code=models.CharField(max_length=10)
    account_type=models.CharField(max_length=30)
    customer_name=models.CharField(max_length=50)
    customer_photo=models.FileField(upload_to="static/Admin/lib/cus-photo")
    date_of_birth=models.DateField()
    c_residence=models.CharField(max_length=100)
    c_phone_number=models.BigIntegerField(unique=True)
    c_email=models.EmailField()
    aadhar_number=models.BigIntegerField(unique=True)
    min_balance=models.BigIntegerField()
    main_balance=models.BigIntegerField()
    opening_date=models.DateField()
    co_name=models.CharField(max_length=50, null=True)
    co_relation=models.CharField(max_length=30, null=True)
    co_residence=models.CharField(max_length=100, null=True)
    co_idproof=models.FileField(upload_to='static/Admin/lib/co-id-proof', null=True)
    account_status=models.CharField(max_length=50)
    class Meta:
        managed=True
        db_table="tb_account"

class tb_customer(models.Model):
    customer_id=models.CharField(max_length=10,unique=True,primary_key=True)
    account_id=models.ForeignKey(tb_account,on_delete=models.CASCADE)
    c_name=models.CharField(max_length=50)
    c_password=models.CharField(max_length=30)
    security_pin=models.IntegerField()
    class Meta:
        managed=True
        db_table="tb_customer"
'''
class tb_transaction(models.Model):
    customer_id=models.ForeignKey(tb_customer,on_delete=models.CASCADE)
    transaction_id=models.CharField(primary_key=True,max_length=15,unique=True)
    transaction_type=models.CharField(max_length=50)
    from_account=models.BigIntegerField()
    transaction_date=models.DateField()
    payee_account=models.BigIntegerField()
    ifsc_code=models.CharField(max_length=20)
    payee_name=models.CharField(max_length=50)
    amount=models.BigIntegerField()
    checque_id=models.CharField(max_length=30,unique=True)
    remarks=models.CharField(max_length=100)
    transaction_status=models.CharField(max_length=50)
    class Meta:
        db_table="tb_transaction"

class tb_bank(models.Model):
    ifsc_code=models.CharField(primary_key=True,max_length=15,unique=True)
    manager_name=models.CharField(max_length=30)
    branch_loc=models.CharField(max_length=30)
    pincode = models.IntegerField()
    class Meta:
        db_table="tb_bank"

'''