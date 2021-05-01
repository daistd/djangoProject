from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CustomerForm
from .models import Customer


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            customer = form.save()
            return HttpResponseRedirect('/thanks/'+customer.ceo+'/'+customer.kaspi_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()

    return render(request, 'index.html', {'form': form})


def thanks(request, name, kaspi_id):
    return render(request, 'thanks.html', {'name': name, 'kaspi_id':kaspi_id})
