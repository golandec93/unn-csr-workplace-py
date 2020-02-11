import http.client
import json


# todo: looks like redundant
class Optional:
    def __init__(self, data=None):
        self._data = data

    @classmethod
    def of(cls, data):
        return cls(data)

    @classmethod
    def empty(cls):
        return cls(None)

    def is_empty(self):
        return self._data is None

    def is_not_empty(self):
        return self._data is not None

    def map(self, func):
        if self.is_empty():
            return self
        self._data = func(self._data)
        return self

    def get(self):
        return self._data

    def or_else_get(self, func):
        if self.is_empty():
            return func()
        return self._data

    def if_present(self, func):
        if self.is_empty():
            return
        func(self._data)


class Customer:
    def __init__(self, json_data=None):
        if json_data is None:
            self.id = None
            self.first_name = None
            self.last_name = None
            self.phone_number = None
            self.customer_status = None
            self.services = None
        else:
            data = json.loads(json_data)
            self.id = data['id']
            self.first_name = data['firstName']
            self.last_name = data['lastName']
            self.phone_number = data['phoneNumber']
            self.customer_status = Status(data['customerStatus'])
            if 'services' in data:
                self.services = list(map(lambda x: Service.from_dict(x), data['services']))
            else:
                self.services = []


class Service:
    def __init__(self):
        self.id = None
        self.name = None
        self.service_status = None
        self.hardwares = None

    @classmethod
    def from_dict(cls, dictionary):
        service = cls()
        service.name = dictionary['name']
        service.id = dictionary['id']
        service.service_status = Status.from_dictionary(dictionary['serviceStatus'])
        if 'hardwares' in dictionary:
            service.hardwares = list(map(lambda x: Hardware.from_dict(x), dictionary['hardwares']))
        return service

    @staticmethod
    def from_json(json_bytes):
        dictionary = json.loads(json_bytes)
        return Service.from_dict(dictionary)


class Hardware:
    def __init__(self):
        self.id = None
        self.status = None
        self.name = None

    @classmethod
    def from_dict(cls, dictionary):
        hardware = cls()
        hardware.id = dictionary['id']
        hardware.name = dictionary['name']
        hardware.status = Status.from_dictionary(dictionary['hardwareStatus'])
        return hardware


class Status:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def from_dictionary(cls, dictionary):
        status = cls()
        status.id = dictionary['id']
        status.name = dictionary['name']
        return status


def get_customer_by_phone(phone_number):
    connection = http.client.HTTPSConnection('nnsu-nc.herokuapp.com')
    connection.request('GET', '/customers/search/getCustomerByPhoneNumber?phoneNumber=' + phone_number)
    response = connection.getresponse()
    if 200 <= response.code < 300:
        customer = Customer(response.read())
        connection.close()
        return Optional.of(customer)
    connection.close()
    return Optional.empty()


def get_customer_details_by_customer_id(customer_id):
    connection = http.client.HTTPSConnection('nnsu-nc.herokuapp.com')
    connection.request('GET', '/customers/' + str(customer_id) + '?projection=plain')
    response = connection.getresponse()
    if 200 <= response.code < 300:
        customer = Customer(response.read())
        connection.close()
        return Optional.of(customer)
    connection.close()
    return Optional.empty()


def get_service_details_by_service_id(service_id):
    connection = http.client.HTTPSConnection('nnsu-nc.herokuapp.com')
    connection.request('GET', '/services/' + str(service_id) + '?projection=plain')
    response = connection.getresponse()
    if 200 <= response.code < 300:
        service = Service.from_json(response.read())
        connection.close()
        return Optional.of(service)
    connection.close()
    return Optional.empty()


def call_service_is_broken(service_id, customer_id):
    connection = http.client.HTTPSConnection('nnsu-nc.herokuapp.com')
    connection.request('GET', '/services/search/setServiceStatusFailByCustomer_IdAndService_Id?'
                              'customerId=' + str(customer_id) + '&serviceId' + str(service_id))
    return
