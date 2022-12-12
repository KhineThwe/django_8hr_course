from django.shortcuts import render,redirect
from . models import Room
from . forms import RoomForm

def home(request):
    room = Room.objects.all()
    contexts = {'rooms':room}
    return render(request,'base/home.html',contexts)

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
    contexts = {'room':room}
    return render(request,'base/room.html',contexts)

def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    if request.method == "POST":
        form = RoomForm(request.POST,instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    contexts = {'form':form}
    return render(request,'base/room_form.html',contexts)