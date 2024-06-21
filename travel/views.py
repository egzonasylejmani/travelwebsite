from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Trip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Booking 
from .models import Cart 
# import Cart
from django.db.models import Q



def index(request):
    trip_list = Trip.objects.all()
    query = request.GET.get('q')

    if query:
        trip_list = trip_list.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

    paginator = Paginator(trip_list, 6)
    page_number = request.GET.get('page')

    try:
        trips = paginator.page(page_number)
    except PageNotAnInteger:
        trips = paginator.page(1)
    except EmptyPage:
        trips = paginator.page(paginator.num_pages)

    context = {
        'trips': trips,
        'query': query  # Pass the query back to the template for display
    }
    return render(request, 'travel.html', context)



def view_trip(request, id):
    context = {
        'trip': Trip.objects.filter(id=id).first(),

    }

    return render(request, 'view-trip.html', context)
  

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')

        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                user.groups.add(Group.objects.get(name='customer'))
                login(request, user)
                return redirect('index')
        return render(request, 'registration/register.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('login')

    
@login_required
def dashboard(request):
    context = {
        'bookings': Booking.objects.filter(customer_id=request.user.id)
    }
    return render(request, 'dashboard.html', context)
@login_required
def add_to_cart(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, trip=trip)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)  # Assuming Cart has a 'user' field for user association
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.trip.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart_detail.html', context)

def item_decrement(request, trip_id):
    cart_item = get_object_or_404(Cart, user=request.user, trip_id=trip_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart_detail')
def item_increment(request, trip_id):
    cart_item = get_object_or_404(Cart, user=request.user, trip_id=trip_id)
    
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')
