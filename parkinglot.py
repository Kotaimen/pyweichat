# -*- coding: utf-8 -*-

'''
Created on Jun 24, 2013

@author: ray
'''

import requests
import json
import unittest
import collections
from xml.etree import ElementTree


from grub_jtcx import encode_lonlat, decode_lonlat, response2json, distance


class ParkingLot(collections.namedtuple('ParkingLot', 'name location address available total distance image_url timestamp')):
    pass


class ParkingInfoCenter(object):

    def __init__(self):
        self._parkinglot_pool = dict()

    def update(self):
        session = requests.Session()
        response = session.get("""http://www.jtcx.sh.cn/TravelServlet?type=allParkingSpace.xml""")
        xml = response.content.decode('gbk').replace('gbk', 'utf-8').encode('utf-8')
        tree = ElementTree.fromstring(xml)

        result = tree.findall('*/*/Row')

        pool = self._parkinglot_pool
        pool.clear()
        for row in result:
            generator = row.iterfind('Field')
            field_id = int(next(generator).attrib['Value'])
            field_timestamp = next(generator).attrib['Value']
            field_available = int(next(generator).attrib['Value'])
            field_total = int(next(generator).attrib['Value'])

            info = dict(extid=field_id,
                        timestamp=field_timestamp,
                        available=field_available,
                        total=field_total,
                        )
#             print info
            pool[field_id] = info
        
    def get_parking_info(self, parkinglot_id):
        parkinglot_info = self._parkinglot_pool[parkinglot_id]
        return parkinglot_info


class ParkingLotService(object):
    
    def __init__(self):
        with open('parkinglots.json', 'rb') as fp:
            data = json.load(fp)
            
        self._data = data

    def fetch(self, location):
        """ Parking space information

        Note the offical site don't use location based query but their Mapabc
        provider supports actually supports it...

        location_encode = (encode_lonlat(location[0]), encode_lonlat(location[1]))

        session = requests.Session()
        response = session.get('http://sis.jtcx.sh.cn/sisserver?highLight=false'\
                               '&srctype=USERPOI&eid=9070&extId=&agentId=&tempid=8&config=BESN'\
                               '&cityCode=021&cenName=&searchType=&number=10&batch=1'\
                               '&a_k=cb02363e90e02da4b5f3cc9dcc7f5cd0881012bd4ec0dbe0f2b5a87cea3602ad70431a4938633d15'\
                               '&resType=JSON&enc=utf-8&sr=0&range=800&naviflag=0'\
                               '&ctx=1&a_nocache=&cenX=%s&cenY=%s' \
                               % location_encode
                               )


        data = response2json(response.text)
        """
        parking_center = ParkingInfoCenter()
        parking_center.update()
        
        available = list()
        for poi in self._data.itervalues():
            try:
                info = parking_center.get_parking_info(poi['extid'])
            except KeyError:
                continue
            baidu_loc = poi['baidu_loc']
            parkinglot = ParkingLot(name=poi['name'],
                                    location=baidu_loc,
                                    address=poi['address'],
                                    available=info['available'],
                                    total=info['total'],
                                    distance=int(distance(location, poi['location'])),
                                    image_url='http://api.map.baidu.com/staticimage?width=320&height=240&center=%(lon)s,%(lat)s&scale=1&zoom=18&markers=%(lon)s,%(lat)s&markerStyles=l,P,0x00CCFF' \
                                        % dict(lon=baidu_loc[0], lat=baidu_loc[1]),
                                    timestamp=info['timestamp']
                                    )
            
            available.append(parkinglot)
        available.sort(key=lambda p:p.distance)
        ret = list()
        count = 0
        for r in available:
            if count > 10:
                break
            if r.available <= 1 or r.total == 0:
                continue
            ret.append(r)
            count += 1

        return ret


class TestParkingLotService(unittest.TestCase):

    def testFetch(self):
        service = ParkingLotService()
        for parkinglot in service.fetch((121.458989, 31.22085)):
            print parkinglot.name, parkinglot.total, parkinglot.available


if __name__ == '__main__':
    unittest.main()
