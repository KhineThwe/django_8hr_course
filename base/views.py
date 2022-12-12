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
    return render(request,'base/create_room.html',contexts)