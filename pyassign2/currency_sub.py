"""currency_sub.py: Module for currency exchange

This module provides several string parsing functions to implement a
simple currency exchange routine using an online currency service.

The primary function named 'exchange' will take a tentive check on the
arguments, while the other functions will completely depend on the website.

__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
Programming using the method given by Cornell"""

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

    data = {'from': currency_from,
            'to': currency_to,
            'amt': amount_from}
    doc = urlopen('http://cs1110.cs.cornell.edu/2016fa/a1server.php?' +
                  'from={from}&to={to}&amt={amt}'.format(**data))
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
    """Returns: the error information if an error happens.

    Given a JSON response to a currency query, this returns the string
    inside double quotes (") immediately following the keyword "error".
    Returns an empty string if the JSON is the result of a valid query.

    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""

    left = json.find('"error"')
    error = json[left + 11:len(json) - 3]
    return error


def exchange(currency_from, currency_to, amount_from):
    """Returns: amount of currency received in the given exchange.

    In this exchange, the user is changing amount_from money in
    currency currency_from to the currency currency_to. The value
    returned represents the amount in currency currency_to.

    The value returned has type float.
    For invalid query, print error information and return float('nan')
    to avoid exception when using this function to calculate.

    Parameter currency_from: the currency on hand
    Precondition: currency_from is a string for a valid currency code

    Parameter currency_to: the currency to convert to
    Precondition: currency_to is a string for a valid currency code

    Parameter amount_from: amount of currency to convert
    Precondition: amount_from is a non-negative float"""

    # check the input tentively
    if type(currency_from) != str or type(currency_to) != str \
            or len(currency_from) != 3 or len(currency_to) != 3:
        print('ERROR: currency_from and currency_to must be' +
              ' standard Currency Symbol in type str.')
        return float('nan')
    if type(amount_from) not in (float, int) or amount_from < 0:
        print('ERROR: amount_from must be non-negative float (or int).')
        return float('nan')

    json = currency_response(currency_from, currency_to, amount_from)
    amount_to = get_to(json)
    if amount_to:   # valid query
        return float(amount_to)
    # invalid query
    print('ERROR:', get_error(json))
    return float('nan')


def main():
    """enable that the user can input arguments endlessly to call 'exchange'
    use 'ctrl+c' to stop"""

    while True:
        try:
            currency_from, currency_to, amount_from = (
                input('The currency on hand: '),
                input('The currency to convert to : '),
                float(input('The amount of currency to convert: '))
                )
        except ValueError:
            print('ERROR: amount_from must be non-negative float (or int).\n')
        else:
            print(exchange(currency_from, currency_to, amount_from))    
            print()


##########################
# Above is the main program.
# Below is the test part.
##########################


def test_currency_response():
    """to test if the function currency_response can
    return right answers for different arguments"""

    data = {
        # valid queries
        ('USD', 'EUR', 2.5): '{ "from" : "2.5 United States Dollars", \
"to" : "2.1589225 Euros", "success" : true, "error" : "" }',
        ('CNY', 'JPY', 6.66): '{ "from" : "6.66 Chinese Yuan", \
"to" : "108.27590665635 Japanese Yen", "success" : true, "error" : "" }',
        ('RUB', 'BTC', 0.0): '{ "from" : "0 Russian Rubles", \
"to" : "0 Bitcoins", "success" : true, "error" : "" }',
        # invalid queries
        ('not', 'EUR', 2.5): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Source currency code is invalid." }',
        ('USD', 'not', 2.5): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Exchange currency code is invalid." }',
        ('USD', 'EUR', 'not'): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Currency amount is invalid." }',
        # if there're multiple kinds of error, only the first kind returned
        ('not', 'not', 2.5): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Source currency code is invalid." }',
        ('not', 'EUR', 'not'): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Source currency code is invalid." }',
        ('USD', 'not', 'not'): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Exchange currency code is invalid." }',
        ('not', 'not', 'not'): '{ "from" : "", "to" : "", \
"success" : false, "error" : "Source currency code is invalid." }',
    }

    for datum in data.keys():
        assert currency_response(*datum) == data[datum]


def test_get_to():
    """to test if the function get_to can
    return right answers for different arguments"""
    data = {
        # valid queries
        ('USD', 'EUR', 2.5): '2.1589225',
        ('CNY', 'JPY', 6.66): '108.27590665635',
        ('USD', 'CNY', 100.0): '685.21',
        ('KPW', 'KRW', 0.0): '0',  # be cautious that '0' != '0.0'
        # invalid queries
        ('not', 'EUR', 2.5): '',
        ('USD', 'not', 2.5): '',
        ('USD', 'EUR', 'not'): '',
        ('not', 'not', 2.5): '',
        ('USD', 'not', 'not'): '',
        ('not', 'EUR', 'not'): '',
        ('not', 'not', 'not'): ''
    }

    for datum in data.keys():
        json = currency_response(*datum)
        assert get_to(json) == data[datum]


def test_get_error():
    """to test if the function get_error can
    return right answers for different arguments"""

    data = {
        # valid queries
        ('USD', 'EUR', 2.5): '',
        ('CNY', 'JPY', 6.66): '',
        ('KPW', 'KRW', 0.0): '',
        # valid queries
        ('not', 'EUR', 2.5): 'Source currency code is invalid.',
        ('USD', 'not', 2.5): 'Exchange currency code is invalid.',
        ('USD', 'EUR', 'not'): 'Currency amount is invalid.',
        # if there're multiple kinds of error, only return the first kind
        ('not', 'not', 2.5): "Source currency code is invalid.",
        ('CNY', 'not', 'not'): "Exchange currency code is invalid.",
        ('not', 'USD', 'not'): "Source currency code is invalid.",
        ('not', 'not', 'not'): "Source currency code is invalid."
    }

    for datum in data.keys():
        json = currency_response(*datum)
        assert get_error(json) == data[datum]


def test_exchange():
    """to test if the function exchange can
    return right answers for different arguments"""

    data = {  # valid queries
        ('USD', 'EUR', 2.5): 2.1589225,
        ('CNY', 'JPY', 6.66): 108.27590665635,
        ('USD', 'CNY', 100.0): 685.21,
        ('BTC', 'RUB', 10): 5015146.3823642,
        ('KPW', 'KRW', 0.0): 0.0
    }

    for datum in data.keys():
        assert exchange(*datum) == data[datum]

    # float('nan') returned for any invalid query
    invalid_data = [
        # the followings are checked by the function
        ('none', 'EUR', 2.5),
        ('USD', 'none', 2.5),
        ('USD', 'EUR', 'not'),
        ('USD', 'EUR', -1.0),

        ('none', 'none', 2.5),
        ('none', 'EUR', 'not'),
        ('USD', 'none', 'not'),
        ('none', 'EUR', -1.0),
        ('USD', 'none', -1.0),

        ('none', 'none', 'none'),
        ('none', 'none', -1.0),
        # the followings are checked by the website
        ('not', 'EUR', 2.5),
        ('USD', 'not', 2.5)
    ]

    for invalid_datum in invalid_data:
        result = exchange(*invalid_datum)
        # a != a implies a == float('nan')
        assert result != result


def test_all():
    """test all functions"""

    test_currency_response()
    test_get_to()
    test_get_error()
    test_exchange()
    print('All tests passed.')


if __name__ == '__main__':
    test_all()
    main()
