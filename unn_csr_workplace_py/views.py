from django.shortcuts import render, redirect

from unn_csr_workplace_py.forms import CustomerSearchByPhone
from unn_csr_workplace_py.models import *


def customer_search(request):
    if request.method == 'POST':
        customer_search_form = CustomerSearchByPhone(request.POST)
        phone_number = customer_search_form.data.get('phone_number')
        customer = get_customer_by_phone(phone_number)
        if customer.is_not_empty():
            customer_is_found = render(
                request, '../templates/customer_search.html',
                {'customer_search_form': customer_search_form,
                 'customer': customer.get()})
            return customer_is_found
    return render(request,
                  '../templates/customer_search.html',
                  {'customer_search_form': CustomerSearchByPhone()})


def to_customer_search(request):
    return redirect('search')


def customer_details(request, customer_id):
    customer = get_customer_details_by_customer_id(customer_id)
    if customer.is_empty():
        return redirect('search')
    return render(request, '../templates/customer_details.html',
                  {'customer': customer.get()})


def service_details(request, customer_id, service_id):
    if request.method == 'POST':
        return None
    service = get_service_details_by_service_id(service_id)
    if service.is_empty():
        return redirect('/customer/' + str(customer_id))
    return render(request,
                  '../templates/service_details.html',
                  {'service': service.get(), 'customer_id': customer_id})


def service_is_broken(request, customer_id, service_id):
    call_service_is_broken(customer_id, service_id)
    return redirect('/customer/' + str(customer_id) + '/service/' + str(service_id))
