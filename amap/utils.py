import requests
import json
import time
import csv
from pandas.io.json import json_normalize  # package for flattening json in pandas df
import pandas as pd
import os

k = open("../amap_key.txt", "r")
amap_key = k.read()

def getPOI(poi_code=110202, ad_code=310000, amap_key=amap_key):
    url = 'https://restapi.amap.com/v3/place/text?types={}&city={}&offset=20&page={}&key={}&extensions=all'.format(
        poi_code, ad_code, 1, amap_key)
    res = requests.get(url)
    json_data = json.loads(res.text)
    count = json_data['count']
    print("Rows: {}".format(count))

    if int(count) > 0:

        f_name = '1_ad{}_poi{}.csv'.format(ad_code, poi_code)
        if os.path.exists(f_name):
            os.remove(f_name)
        f = open(f_name, 'a+', encoding='utf-8', newline='')
        writer = csv.writer(f)
        writer.writerow(
            ['poi_id', 'parent', 'name', 'typ', 'typ1', 'typ2', 'typ3', 'business_type', 'address', 'lon', 'lat', 'tel',
             'postcode',
             'website', 'pcode', 'pname', 'citycode', 'cityname', 'adcode', 'adname', 'entr_location', 'exit_location',
             'alias', 'parking_type', 'tag', 'business_area', 'rating', 'cost'])

        pois = json_data['pois']

        for poi in pois:
            poi_id = poi['id']
            parent = poi['parent']
            name = poi['name']
            typ = poi['type']
            typ1 = typ.split(';')[0]
            typ2 = typ.split(';')[1]
            typ3 = typ.split(';')[2]
            business_type = poi['biz_type']
            address = poi['address']
            location = poi['location']
            lon = location.split(',')[0]
            lat = location.split(',')[1]
            tel = poi['tel']
            postcode = poi['postcode']
            website = poi['website']
            pcode = poi['pcode']
            pname = poi['pname']
            citycode = poi['citycode']
            cityname = poi['cityname']
            adcode = poi['adcode']
            adname = poi['adname']
            entr_location = poi['entr_location']
            exit_location = poi['exit_location']
            alias = poi['alias']
            parking_type = poi['parking_type'] if 'parking_type' in poi else ''
            tag = poi['tag']
            business_area = poi['business_area']
            rating = poi['biz_ext']['rating']
            cost = poi['biz_ext']['cost']

            # print(poi_id, parent, name, typ, typ1, typ2, typ3, business_type, address, lon, lat, tel, postcode,
            #       website, pcode, pname, citycode, cityname, adcode, adname, entr_location, exit_location,
            #       alias, parking_type, tag, business_area, rating, cost)
            writer.writerow(
                [poi_id, parent, name, typ, typ1, typ2, typ3, business_type, address, lon, lat, tel, postcode,
                 website, pcode, pname, citycode, cityname, adcode, adname, entr_location, exit_location,
                 alias, parking_type, tag, business_area, rating, cost
                 ])

        f.close()
        f_dat = pd.read_csv(f_name)
        return (f_dat)
