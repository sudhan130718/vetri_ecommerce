
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import logout

from .models import Product, Category, Brands
from .models import  Cart, CartItem, Order, OrderItem

from .forms import CheckoutForm, ProductForm  
from .forms import SignupForm





def home(request):
    return HttpResponse("Hello, this is myapp's home page!")


def test(request):
    return HttpResponse("Welcome, Maha Sudharson")

def combined_view(request):
    response1 = "Hello, this is myapp's home page!<br>"
    response2 = "Welcome, Maha Sudharson"
    return HttpResponse(response1 + response2)


def product_list_new(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brands.objects.all()
    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
    })
   


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') 
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list1')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')

# READ
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# CREATE
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

# UPDATE
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

# DELETE
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

#product_detail 
def product_detail(request, product_id):
    product= get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Cart start

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart': cart, 'items': items})


@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return redirect('view_cart')


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')

# Cart end





@login_required
def checkout(request):
    try:
        # Get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)
        items = cart.cartitem_set.all()

        if not items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('product_list')  # Or wherever you want to send them if the cart is empty

        if request.method == 'POST':
            # If the user submits the form (Place Order button clicked)
            form = CheckoutForm(request.POST)
            if form.is_valid():
                # Save order details to the Order model
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=form.cleaned_data['address'],
                    total_amount=cart.total(),
                    status='Pending',
                    payment_method=form.cleaned_data['payment_method'],
                )

                # Add each item to the OrderItem model
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )

                # Clear the cart
                cart.cartitem_set.all().delete()

                # Show success message and redirect to a confirmation page
                messages.success(request, "Your order has been placed successfully!")
                return redirect('order_confirmation', order_id=order.id)  # Redirect to order confirmation page
        else:
            # If GET request, show the checkout page with an empty form
            form = CheckoutForm()

        # Calculate the total amount
        total = cart.total()

        return render(request, 'checkout.html', {
            'form': form,
            'cart': cart,
            'items': items,
            'total': total,
        })

    except Cart.DoesNotExist:
        messages.error(request, "You don't have a cart yet.")
        return redirect('product_list')
    

#  order 
   
@login_required
def order_confirmation(request, order_id):
    # Get the order based on the order_id
    order = get_object_or_404(Order, id=order_id)

    # Fetch the order items related to this order
    order_items = order.items.all()

    # Render the confirmation page
    return render(request, 'order_confirmation.html', {
        'order': order,
        'order_items': order_items
    })




