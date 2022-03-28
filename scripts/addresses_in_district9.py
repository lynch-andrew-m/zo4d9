import geopandas as gpd
from geopandas.tools import geocode
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import sys
from shapely.geometry import Polygon, Point

UT_TOWER_ADDRESS = '110 Inner Campus Drive, Austin, TX 78705'
THE_DOMAIN = '11410 Century Oaks Terrace, Austin, TX 78758'

def is_in_district9(address, shp_file='data/Council_Districts_Fill/geo_export_028df154-48b2-4b4d-89e4-313dedbcd12b.shp'):
    geolocator = Nominatim(user_agent='Zo4D9')
    try:
        location = geolocator.geocode(address)
        if location is None:
            raise ValueError('Address was not found')
    except GeocoderTimedOut as e:
        raise ValueError('Address was not found')
    data = gpd.read_file(shp_file)
    point = Point(location.longitude, location.latitude)
    poly = Polygon(data.loc[data["council_di"] == 9]["geometry"][0])
    return point.within(poly)


def main(argv):
    if is_in_district9(UT_TOWER_ADDRESS): print("UT Tower is in D9!")
    if not is_in_district9(THE_DOMAIN):   print("The Domain is NOT in D9!")

if __name__ == "__main__":
    main(sys.argv[1:])
