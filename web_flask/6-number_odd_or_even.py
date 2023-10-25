#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """ Returns a string at the root route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Returns a string at the route /hbnb"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """ Returns a string at the route /c/<text>"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def p_route(text='is cool'):
    """ Method that returns Python followed by the value """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def n_route(n):
    """ Method that returns n is a number only if n is an integer """
    return '{:d} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def n_template(n):
    """ Method that returns a HTML page only if n is an integer """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def even_odd_temp(n):
    """ Method that returns a HTML page only if n is an integer """
    return render_template('6-number_odd_or_even.html', n=n)

if __name__ == '__main__':
    """Main function"""
    app.run(host='0.0.0.0', port=5000)
