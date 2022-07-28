from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.http import Http404

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")

    return render(request, "flights/flight.html",{
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers":Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    # with method POST transfer variables flight.id(from header) and passenger_id(from form)
    if request.method == "POST":
        #flight = Flight.objects.filter(id = flight_id).first()  #is the same with next
        flight = Flight.objects.get(pk=flight_id) #pk is PrimaryKey shortcut
        passenger = Passenger.objects.get(pk=int(request.POST["passenger_id"]))
        passenger.flights.add(flight)
        return redirect(reverse("flights:flight", args=(flight.id,)))