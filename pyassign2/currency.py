"""currency.py: Module for currency exchange

This module provides one function to implement a simple 
currency exchange routine using an online currency service;
as well as its test function and a driving funtion named 'main'.

__author__ = 'Li Hongyu'
__pkuid__ = '1700017785'
__email__ = 'hongyuli@pku.edu.cn'
The primary function named 'exchange' will take a tentive check on the
arguments, while the other checks depend on the website completely."""

from urllib.request import urlopen


def exchange(currency_from, currency_to, amount_from):
    """changing amount_from money in currency currency_from to currency
    currency_to. Then return the amount in currency currency_to.

    Return the amount of currency received in the given exchange (as float).
    For invalid query, print error information and return float('nan')
    to avoid exception when using this function to calculate.

    currency_from: the currency on hand (a valid currency code as str)
    currency_to: the currency converted to (a valid currency code as str)
    amount_from: amount of currency to convert (non-negative float/int)"""

    # check the input tentively
    if type(currency_from) != str or len(currency_from) != 3 \
            or type(currency_to) != str or len(currency_to) != 3 \
            or type(amount_from) not in (float, int) or amount_from < 0:
        print('ERROR: please check your arguments.')
        return float('nan')

    # access the url and get amount_to
    data = {'from': currency_from,
            'to': currency_to,
            'amt': amount_from}
    doc = urlopen('http://cs1110.cs.cornell.edu/2016fa/a1server.php?' +
                  'from={from}&to={to}&amt={amt}'.format(**data))
    docstr = doc.read()
    doc.close()
    jstr = docstr.decode()

    jstr = jstr.replace('true', 'True')
    jstr = jstr.replace('false', 'False')
    jdict = eval(jstr)  # convert the str into dict
    amount_to = jdict['to']

    # return proper value according to the situation
    if amount_to:   # valid queries
        return float(amount_to.split()[0])
    # other invalid queries which cannot be checked out by the function
    print('ERROR:', jdict['error'])
    return float('nan')


def main():
    """enable that the user can input arguments endlessly to call 'exchange'
    use 'ctrl+c' to stop"""

    print('Congratulations! The script is in working order.')
    print('*******Now you can do anything you want!*******\n')
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


############################
# Above is the main program.
# Below is the test part.
############################


def test_exchange():
    """to test if the function exchange can
    return right answers for different arguments"""

    # valid queries
    data = {
        ('USD', 'EUR', 2.5): 2.1589225,
        ('CNY', 'JPY', 6.66): 108.27590665635,
        ('USD', 'CNY', 100): 685.21,
        ('KPW', 'KRW', 0.0): 0.0
    }

    for datum in data.keys():
        assert exchange(*datum) == data[datum]

    invalid_data = [
        # test the tentive check done by 'exchange'
        ('none', 'EUR', 2.5),
        ('USD', 'none', 2.5),
        ('USD', 'EUR', 'not'),
        ('USD', 'EUR', -1.0),

        ('none', 'none', 2.5),
        ('none', 'EUR', 'not'),
        ('USD', 'none', 'not'),
        ('none', 'none', 'not'),
        ('none', 'EUR', -1.0),
        ('USD', 'none', -1.0),
        ('none', 'none', -1.0),
        # test the check done by the website
        ('not', 'EUR', 2.5),
        ('USD', 'not', 2.5),
        ('not', 'not', 2.5),
    ]

    for invalid_datum in invalid_data:
        result = exchange(*invalid_datum)
        # a != a implies a == float('nan')
        assert result != result

    print('Test passed.\n')


if __name__ == '__main__':
    test_exchange()
    main()
