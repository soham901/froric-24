from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm, BraintreePaymentForm
from conf.braintree_integration import gateway


@login_required
def item_list(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, 'demo/item_list.html', {'items': items})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    return render(request, 'demo/item_detail.html', {'item': item})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('demo:item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'demo/item_form.html', {'form': form})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('demo:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'demo/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('demo:item_list')
    return render(request, 'demo/item_confirm_delete.html', {'item': item})


def generate_client_token():
    return gateway.client_token.generate()


def payment_view(request):
    client_token = ""
    if request.method == "POST":
        form = BraintreePaymentForm(request.POST)
        if form.is_valid():
            nonce = form.cleaned_data['payment_method_nonce']
            result = gateway.transaction.sale({
                "amount": "10.00",
                "payment_method_nonce": nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                request.user.add_coins(10)
                return redirect('demo:payment_success')
            else:
                return redirect('demo:payment_failed')
    else:
        client_token = generate_client_token()
        form = BraintreePaymentForm()

    return render(request, "demo/payment.html", {"form": form, "client_token": client_token})


def payment_success(request):
    return render(request, 'demo/payment_success.html')

def payment_failed(request):
    return render(request, 'demo/payment_failed.html')
