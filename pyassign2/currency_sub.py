'''currency_sub.py: Module for currency exchange

This module provides several string parsing functions to implement a 
simple currency exchange routine using an online currency service. 
The primary function in this module is exchange

programming using the method given by Cornell
__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
'''


from urllib.request import urlopen


def currency_response(currency_from, currency_to, amount_from):
    """Returns: a JSON string that is a response to a currency query.

    A currency query converts amount_from money in currency currency_from
    to the currency currency_to. The response should be a string of the form

        '{"from":"<old-amt>","to":"<new-amt>","success":true, "error":""}'

    where the values old-amount and new-amount contain the value and name
    for the original and new currencies. If the query is invalid, both
    old-amount and new-amount will be empty, while "success" will be followed
    by the value false.

    Parameter currency_from: the currency on hand
    Precondition: currency_from is a string

    Parameter currency_to: the currency to convert to
    Precondition: currency_to is a string

    Parameter amount_from: amount of currency to convert
    Precondition: amount_from is a float"""

    data = {'currency_from': currency_from,
            'currency_to': currency_to,
            'amount_from': amount_from}
    doc = urlopen('http://cs1110.cs.cornell.edu/2016fa/a1server.php?' +
      'from={currency_from}&to={currency_to}&amt={amount_from}'.format(**data))
    docstr = doc.read()    # the content on the website as bianry stream
    doc.close()
    jstr = docstr.decode()  # convert the content into json string
    return jstr


def get_to(json):
    """Returns: The TO value in the response to a currency query as str.

    Given a JSON response to a currency query, this returns the string
    inside double quotes (") immediately following the keyword "to".
    Returns an empty string if the JSON is the result of an invalid query.

    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""

    left = json.find('"to"')
    right = json.find('"success"')
    currency_to = json[left + 8:right - 3]
    if currency_to:  # valid query
        amount_to = currency_to.split()[0]
    else:           # invalid query
        amount_to = ''
    return amount_to


def get_error(json):
    '''Returns: the error information if an error happens.

    Given a JSON response to a currency query, this returns the string
    inside double quotes (") immediately following the keyword "error".
    Returns an empty string if the JSON is the result of a valid query.

    Parameter json: a json string to parse
    Precondition: json is the response to a currency query
    '''

    left = json.find('"error"')
    error = json[left + 11:len(json) - 3]
    return error


def exchange(currency_from, currency_to, amount_from):
    """Returns: amount of currency received in the given exchange.

    In this exchange, the user is changing amount_from money in
    currency currency_from to the currency currency_to. The value
    returned represents the amount in currency currency_to.

    The value returned has type float.
    For invalid query, return float('nan') and print error information

    Parameter currency_from: the currency on hand
    Precondition: currency_from is a string for a valid currency code

    Parameter currency_to: the currency to convert to
    Precondition: currency_to is a string for a valid currency code

    Parameter amount_from: amount of currency to convert
    Precondition: amount_from is a float"""

    json = currency_response(currency_from, currency_to, amount_from)
    amount_to = get_to(json)
    if amount_to:   # valid query
        return float(amount_to)
    # invalid query
    if __name__ != '__main__':
        # provide this notice to users,
        # but won't print anything when testing the module
        print('ERROR:', get_error(json))
    return float('nan')


##########################
# Above is the main program.
# Below is the test part.
##########################


def test_currency_response():
    """to test if the function currency_response can
    return right answers for different arguments"""

    data = {
        ('USD', 'EUR', 2.5): '{ "from" : "2.5 United States Dollars", \
"to" : "2.1589225 Euros", "success" : true, "error" : "" }',
        ('CNY', 'JPY', 6.66): '{ "from" : "6.66 Chinese Yuan", \
"to" : "108.27590665635 Japanese Yen", "success" : true, "error" : "" }',
        ('RUB', 'BTC', 0.0): '{ "from" : "0 Russian Rubles", \
"to" : "0 Bitcoins", "success" : true, "error" : "" }',
        ('USD', 'EUR', 'not'): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Currency amount is invalid." }',
        ('not', 'EUR', 2.5): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Source currency code is invalid." }',
        ('USD', 'not', 2.5): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Exchange currency code is invalid." }'
    }

    for datum in data.keys():
        assert currency_response(*datum) == data[datum]


def test_get_to():
    """to test if the function get_to can
    return right answers for different arguments"""
    data = {
        ('USD', 'EUR', 2.5): '2.1589225',
        ('CNY', 'JPY', 6.66): '108.27590665635',
        ('USD', 'CNY', 100.0): '685.21',
        ('KPW', 'KRW', 0.0): '0',  # be cautious that '0' != '0.0'
        ('USD', 'EUR', 'not'): '',
        ('not', 'EUR', 2.5): '',
        ('USD', 'not', 2.5): ''
    }

    for datum in data.keys():
        json = currency_response(*datum)
        assert get_to(json) == data[datum]


def test_get_error():
    """to test if the function get_error can
    return right answers for different arguments"""

    data = {
        ('USD', 'EUR', 2.5): '',
        ('CNY', 'JPY', 6.66): '',
        ('KPW', 'KRW', 0.0): '',
        ('USD', 'EUR', 'not'): 'Currency amount is invalid.',
        ('not', 'EUR', 2.5): 'Source currency code is invalid.',
        ('USD', 'not', 2.5): 'Exchange currency code is invalid.',
        # if there're multiple kinds of error, only return the first kind
        ('CNY', 'not', 'not'): "Exchange currency code is invalid.",
        ('not', 'not', 'not'): "Source currency code is invalid."
    }

    for datum in data.keys():
        json = currency_response(*datum)
        assert get_error(json) == data[datum]


def test_exchange():
    """to test if the function exchange can
    return right answers for different arguments"""

    data = {
        ('USD', 'EUR', 2.5): 2.1589225,
        ('CNY', 'JPY', 6.66): 108.27590665635,
        ('USD', 'CNY', 100.0): 685.21,
        ('KPW', 'KRW', 0.0): 0.0
    }

    for datum in data.keys():
        assert exchange(*datum) == data[datum]

    invalid_data = [('USD', 'EUR', 'not'),
                ('not', 'EUR', 2.5),
                ('USD', 'not', 2.5)]
    for invalid_datum in invalid_data:
        # a != a implies a == float('nan')
        assert exchange(*invalid_datum) != exchange(*invalid_datum)


def test_all():
    """test all cases"""

    test_currency_response()
    test_get_to()
    test_get_error()
    test_exchange()
    print('All tests passed.')


if __name__ == '__main__':
    test_all()
