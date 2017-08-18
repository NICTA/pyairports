# pyairports

pyairports is a package which enables airport lookup by 3-letter IATA code.

# Usage

The package can be used in two different ways

## import

To use the package in python code, import and create a local instance of the Airports object.

```python
from pyairports.airports import Airports
airports = Airports()
airports.airport_iata(iata) # namedtuple(airport, [name, city, country, iata, icao, lat, lon, alt, tz, dst, tzdb]) or AirportNotFoundException
airports.other_iata(iata)   # namedtuple(other, [iata, name, country, subdiv, type, lat, lon]) or AirportNotFoundException
airports.lookup(iata)       # namedtuple(airport) or namedtuple(other) or AirportNotFoundException
```

## command line

An entrypoint is created for command line querying:

```
[username@hostname ~]$ pyairports aaa
airport(name='Anaa', city='Anaa', country='French Polynesia', iata='AAA', icao='NTGA', lat='-17.352606', lon='-145.509956', alt='10', tz='-10', dst='U', tzdb='Pacific/Tahiti')
```
