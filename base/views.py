from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from . models import Room,Topic,Message
from . forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        print(username,password)
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,"User doesn't exist")
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            #user not log in
            messages.error(request,"Username or password doesn't exist")
            
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)#login lote pay
            return redirect('home')#sent user to home page
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/login_register.html',{'form':form})
    
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    #inline if statement
    # room = Room.objects.filter(topic__name__icontains=q,name__icontains)
    room = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topic = Topic.objects.all()
    room_count = room.count()
    contexts = {'rooms':room,'topics':topic,"room_count":room_count}
    return render(request,'base/home.html',contexts)

@login_required(login_url = 'login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    contexts = {'form':form}
    return render(request,'base/room_form.html',contexts)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    #descending order newest first
    #get all msg --> Model Message in lowercase message be
    #careful
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    contexts = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',contexts)

@login_required(login_url = 'login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)#to get old prefilled data
    if request.user != room.host:#if request user is not owner of the user
        return HttpResponse('You are not allowed here!')
    if request.method == "POST":
        form = RoomForm(request.POST,instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    contexts = {'form':form}
    return render(request,'base/room_form.html',contexts)

@login_required(login_url = 'login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:#if request user is not owner of the user
        return HttpResponse('You are not allowed here!')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    contexts = {'obj':room}
    return render(request,'base/delete.html',contexts)


@login_required(login_url = 'login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:#if request user is not owner of the user
        return HttpResponse('You are not allowed here!')
    if request.method == "POST":
        message.delete()
        return redirect('home')
    contexts = {'obj':message}
    return render(request,'base/delete.html',contexts)