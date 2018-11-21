'''currency.py: Module for currency exchange

This module provides several string parsing functions to implement a
simple currency exchange routine using an online currency service.
The primary function in this module is exchange

programming using the function eval to make the logic very simple
__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
'''

from urllib.request import urlopen


def exchange(currency_from, currency_to, amount_from):
    """Returns: amount of currency received in the given exchange.

    In this exchange, the user is changing amount_from money in
    currency currency_from to the currency currency_to. The value
    returned represents the amount in currency currency_to.

    The value returned has type float.

    Parameter currency_from: the currency on hand
    Precondition: currency_from is a string for a valid currency code

    Parameter currency_to: the currency to convert to
    Precondition: currency_to is a string for a valid currency code

    Parameter amount_from: amount of currency to convert
    Precondition: amount_from is a float"""

    data = {'currency_from': currency_from,
            'currency_to': currency_to,
            'amount_from': amount_from}
    doc = urlopen('http://cs1110.cs.cornell.edu/2016fa/a1server.php?' +
      'from={currency_from}&to={currency_to}&amt={amount_from}'.format(**data))
    docstr = doc.read()
    doc.close()
    jstr = docstr.decode()

    jstr = jstr.replace('true', 'True')
    jstr = jstr.replace('false', 'False')
    jdict = eval(jstr)  # convert the str into dict

    amount_to = jdict['to']
    if amount_to:   # valid query
        return float(amount_to.split()[0])
    # invalid query
    if __name__ != '__main__':
        # provide this notice to users,
        # but won't print anything when testing the module
        print('ERROR:', jdict['error'])
    return float('nan')


############################
# Above is the main program.
# Below is the test part.
############################


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


if __name__ == '__main__':
    test_exchange()
    print('Test passed.')
