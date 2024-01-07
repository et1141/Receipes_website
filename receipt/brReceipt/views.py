from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Avg
import random

from .models import Receipt
from .models import Category
from .models import RatesReceipt
from .models import RatesCategory

from .forms import ReceiptForm



##convention from brGuitars
def index(request):
    template = loader.get_template('brReceipt/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

##Using render django automaticly uses template and creates httpresponse, what makes code more clear
def categories(request):
    categories_list = Category.objects.all()
    context = {'categories': categories_list}
    return render(request, 'brReceipt/categories.html', context)

def category_recipes(request, category_id):
    receipts = Receipt.objects.filter(id_category=category_id).values() 
    category = get_object_or_404(Category, pk=category_id)
    average_rating = RatesCategory.objects.filter(id_category=category).aggregate(Avg('score')) 
    average_rating_value = average_rating.get('score__avg', None)

#    recipes = Receipt.objects.filter(category=category_id)
    return render(request, 'brReceipt/category_recipes.html', {'category': category, 'receipts': receipts ,'average_rating':average_rating_value})

def single_receipt(request, category_id, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    average_rating = RatesReceipt.objects.filter(id_receipt=receipt).aggregate(Avg('score')) 
    average_rating_value = average_rating.get('score__avg', None)

    return render(request, 'brReceipt/single_receipt.html',{'category_id':category_id, 'receipt':receipt, 'average_rating':average_rating_value})

@login_required
def rate_receipt(request, receipt_id):
    if request.method == 'POST':
        score = request.POST.get('score')
        user = request.user
        #to check if user already rated
        existing_rate = RatesReceipt.objects.filter(id_user=user, id_receipt=receipt_id).first()

        if existing_rate:
            #just update if user already rated
            existing_rate.score = score
            existing_rate.save()
        else:
            #reate new if user didn't rated
            receipt = get_object_or_404(Receipt, pk=receipt_id)
            new_rate = RatesReceipt(score=score, id_user=user, id_receipt=receipt)
            new_rate.save()
    return redirect('index')

@login_required
def rate_category(request, category_id):
    if request.method == 'POST':
        score = request.POST.get('score')
        user = request.user
        #to check if user already rated
        existing_rate = RatesCategory.objects.filter(id_user=user, id_category=category_id).first()

        if existing_rate:
            #just update if user already rated
            existing_rate.score = score
            existing_rate.save()
        else:
            #reate new if user didn't rated
            category = get_object_or_404(Category, pk=category_id)
            new_rate = RatesCategory(score=score, id_user=user, id_category=category)
            new_rate.save()
    return redirect('index')



@login_required
def add_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.id_author = request.user  # Przypisanie autora
            receipt.save()
            return redirect('index')
    else:
        form = ReceiptForm()

    return render(request, 'brReceipt/add_receipt.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'brReceipt/register.html', {'form': form})


def search_receipts(request):
    search_record = request.GET.get('query', '')  # Pobierz wartość wprowadzoną w formularzu

    receipts = Receipt.objects.filter(name__icontains=search_record)| Receipt.objects.filter(ingredients__icontains=search_record)
    if not receipts.exists():
        receipts = None
    return render(request, 'brReceipt/search_results.html', {'receipts': receipts})

def random_receipt(request):
    receipts = Receipt.objects.all()
    receipt = random.choice(receipts)
    average_rating = RatesReceipt.objects.filter(id_receipt=receipt).aggregate(Avg('score')) 
    average_rating_value = average_rating.get('score__avg', None)

    return render(request, 'brReceipt/single_receipt.html',{'category_id':receipt.id_category.id, 'receipt':receipt, 'average_rating':average_rating_value})

def show_ranking(request):
    receipts = Receipt.objects.all()
    ranked_receipts = []
    for receipt in receipts:
        average_score = RatesReceipt.objects.filter(id_receipt=receipt).aggregate(Avg('score'))
        average_score = average_score.get('score__avg', None)

        if average_score is not None:
            ranked_receipts.append({'receipt': receipt, 'average_score': average_score})
     
    ranked_receipts = sorted(ranked_receipts, key=lambda x: x['average_score'], reverse=True)

    return render(request, 'brReceipt/ranking.html', {'ranked_receipts': ranked_receipts})
 