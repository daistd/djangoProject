from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CustomerForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            seo = request.POST
            return HttpResponseRedirect('/thanks/'+seo.get('ceo'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()

    return render(request, 'index.html', {'form': form})


def thanks(request, name):
    return render(request, 'thanks.html', {'name': name})
