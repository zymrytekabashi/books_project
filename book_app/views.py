from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, UserManager, Book
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],bday=request.POST['bday'], email=request.POST['email'], password= password)
        request.session['uid']= user.id
        return redirect('/success')
    
    
    
        
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/success')
        else:
            messages.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/')
        


def success(request):
    context = {
        'user':User.objects.get(id=request.session['uid']),
        'all_books': Book.objects.all(),
        
    }
    
    return render(request, 'success.html',context)

def create_book(request):
    if len(request.POST['desc']) < 5:
        messages.error(request, 'Description should be at least 5 characters')
    elif request.POST['title'] == 0:
        messages.error(request, 'Title is required')
    else:
        Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploaded_by=User.objects.get(id=request.session['uid']))
        return redirect('/success')
    return redirect('/success')

def one_book(request, id):
    context={
        'viewed_book': Book.objects.get(id=id),
       
    }
    
    return render(request, 'one_book.html', context)

def create_like(request, book_id):
    user = User.objects.get(id=request.session['uid'])
    book = Book.objects.get(id=book_id)
    
    user.liked_books.add(book)
    
    return redirect('/success')

def delete_like(request, book_id):
    user = User.objects.get(id=request.session['uid'])
    book = Book.objects.get(id=book_id)
    
    user.liked_books.remove(book)
    
    return redirect('/success')

def log_out(request):
    request.session.clear()
    return redirect('/')
