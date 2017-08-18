from collections import namedtuple

from pyairports import airports
import os
import io
import csv

other = namedtuple('other', ['iata', 'name', 'country', 'subdiv', 'type', 'lat', 'lon'])


def is_port(f):
    # 1 = port, as defined in Rec. 16
    # 2 = rail terminal
    # 3 = road terminal
    # 4 = airport
    # 5 = postal exchange office
    # [6 = reserved for multimodal functions, ICD's, etc.]
    # [7 = reserved for fixed transport functions (e.g. oil platform)]
    # B = border crossing
    # 0 = function not known, to be specified

    if len(f) < 4:
        return None

    t = []

    if f[0] == '1':
        t.append('Port')

    if f[1] == '2':
        t.append('Rail Terminal')

    if f[2] == '3':
        t.append('Road Terminal')

    if f[3] == '4':
        t.append('Airport')

    return t


def parse_subloc(s):
    if not s:
        return None, None

    lat, lon = s.split(' ')

    lat_d = int(lat[:2])
    lat_m = int(lat[2:-1])

    if lat[-1] == 'S':
        lat_d = -lat_d

    lon_d = int(lon[:3])
    lon_m = int(lon[3:-1])

    if lon[-1] == 'W':
        lon_d = -lon_d

    return '{}.{}'.format(lat_d, lat_m), '{}.{}'.format(lon_d, lon_m)


def read_locode_csv(path):
    with io.open(path, 'rb') as inf:
        r = csv.reader(inf, delimiter=',', quotechar='"')
        for line in r:
            changed, locode_country, locode_location, name, clean_name, subdiv, func, status, date, iata, subloc, codes = line
            lat, lon = parse_subloc(subloc)

            if iata:
                if iata != locode_location:
                    print 'iata {} != locode {}. Using {}'.format(iata, locode_location, iata)
            if is_port(func):
                yield dict(
                    country=locode_country,
                    iata=locode_location if not iata else iata,
                    # name=name,
                    type=', '.join(sorted(is_port(func))),
                    name=clean_name,
                    subdiv=subdiv,
                    lat=lat,
                    lon=lon
                )


def main():
    alook = airports.Airports()

    results = []

    for dirpath, dirnames, filenames in os.walk('UN LOCODE'):
        for fn in filenames:
            if 'UNLOCODE' in fn and fn.endswith('csv'):
                for port in read_locode_csv(os.path.join(dirpath, fn)):

                    if 'Airport' not in port['type']:
                        continue

                    iata = port['iata']
                    if not iata:
                        continue

                    try:
                        existing = alook.airport_iata(iata)
                    except KeyError:
                        continue

                    results.append(other(**port))

    with open('./pyairports/data/other_list.py', 'wb') as outf:
        outf.write("""\
#Other location types - from the UN LOCODE database

OTHER_LIST = [""")

        for r in results[:-1]:
            outf.write(str(list(r)) + ',\n')
        outf.write(str(list(results[-1])) + '\n]\n')

    print('wrote to ./pyairports/data/other_list.py')

if __name__ == '__main__':
    assert False, "When next using, update to write to data/<list>.json please!"
    main()
