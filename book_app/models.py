from django.db import models
import re
from datetime import datetime
import bcrypt



class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] ='Password should be at least 8 characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password'] = 'Passwords should match'
        if postData['bday'] == None:
            errors['bday'] = 'Birthday can not be empty'
        date = datetime.strptime(postData['bday'], '%Y-%m-%d')
        if date > datetime.now():
            errors['bday'] = "Birthdate must be in the past"            
        result = User.objects.filter(email=postData['email'])
        if len(result) > 0:
            errors['email'] = 'Email has already been registered!'
            
        return errors
    
class BookManager(models.Manager):
    def book_val(self, postData):
        errors = {}        
        if postData['title']== '':
            errors["title"] = "Title is required"
        if len(postData['desc']) < 5:
            errors["desc"] = "Description should be at least 5 characters"

        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bday= models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name = 'has_books', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name= 'liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    
    
    
    
    
    