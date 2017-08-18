from nose.tools import *

from pyairports.airports import Airports, AirportNotFoundException

airports = Airports()


def test_nones():
    assert_raises_regexp(ValueError, "iata must be a string", airports.airport_iata, None)
    assert_raises_regexp(ValueError, "iata must be a string", airports.other_iata, None)
    assert_raises_regexp(ValueError, "iata must be a string", airports.lookup, None)


def test_regular():
    assert_true(airports.is_valid('GKA'))
    assert_true(airports.is_valid('OLT'))
    assert_equals(airports.airport_iata('GKA').name, "Goroka")
    assert_equals(airports.airport_iata('OLT').country, "United States")


def test_other():
    assert_true(airports.is_valid('AUH'))
    assert_true(airports.is_valid('VFA'))
    assert_equals(airports.other_iata('AUH').name, "Abu Dhabi")
    assert_equals(airports.other_iata('VFA').country, "ZW")


def test_both():
    assert_equals(airports.lookup('GKA').name, "Goroka")
    assert_equals(airports.lookup('VFA').name, "Victoria Falls Intl")


def test_unicode():
    assert_equals(airports.lookup(u'GKA').name, "Goroka")
    assert_equals(airports.lookup(u'VFA').name, "Victoria Falls Intl")


def test_neither():
    assert_raises(AirportNotFoundException, airports.lookup, 'AAB')
    assert_false(airports.is_valid('AAB'))


def test_specific():
    assert_equals(airports.lookup('RIR', airports.airports).name, 'Flabob Airport')
    assert_raises(AirportNotFoundException, airports.lookup, 'RIR', airports.other)


def test_none():
    assert_raises_regexp(ValueError, "iata must be three characters", airports.airport_iata, "")
    assert_raises_regexp(ValueError, "iata must be three characters", airports.airport_iata, "A")
    assert_raises_regexp(ValueError, "iata must be three characters", airports.airport_iata, "AAAA")


def test_nonstring():
    assert_raises_regexp(ValueError, "iata must be a string", airports.airport_iata, -1)
    assert_raises_regexp(ValueError, "iata must be a string", airports.airport_iata, airports)
    assert_raises_regexp(ValueError, "iata must be a string", airports.airport_iata, str)
    assert_raises_regexp(ValueError, "iata must be a string", airports.airport_iata, 1.0)
    assert_raises_regexp(ValueError, "iata must be a string", airports.airport_iata, {})
