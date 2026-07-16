from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import SignUpForm
from .models import Category, Order, OrderItem, Product


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'store/product_list.html', {
        'products': products, 'categories': categories,
        'selected_category': category_slug, 'query': query or '',
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': product})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = Cart(request)
    cart.add(product, quantity=int(request.POST.get('quantity', 1)))
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart-detail')


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    messages.info(request, f'Removed {product.name} from your cart.')
    return redirect('cart-detail')


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).set_quantity(product, int(request.POST.get('quantity', 1)))
    return redirect('cart-detail')


def cart_detail(request):
    return render(request, 'store/cart_detail.html', {'cart': Cart(request)})


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('product-list')

    if request.method == 'POST':
        order = Order.objects.create(customer=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        messages.success(request, f'Order #{order.pk} placed successfully!')
        return redirect('order-detail', pk=order.pk)

    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_history(request):
    return render(request, 'store/order_history.html', {'orders': Order.objects.filter(customer=request.user)})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


def signup(request):
    if request.user.is_authenticated:
        return redirect('product-list')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product-list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})