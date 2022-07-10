import requests
import json


NOVA_POSHTA_API_KEY = "dfdfsdfs"
HEADERS = {'Content-Type': 'application/json'}


class NovaPoshtaAPI:
    """API of Nova Poshta delivery."""
    def __init__(self, API_key:str, headers:dict):
        self.API_key = API_key
        self.headers = headers
        self.urls = {
            'settlements': 'http://testapi.novaposhta.ua/v2.0/json/Address/searchSettlements/',
            'streets': 'http://testapi.novaposhta.ua/v2.0/json/Address/searchSettlementStreets/',
            'postal_office': 'http://testapi.novaposhta.ua/v2.0/json/AddressGeneral/getWarehouses',
        }
    
    def get_city(self, city:str, limit:int):
        """Searching for settlements in Nova Poshta. API key not required."""
        data_settlements = {
        "apiKey": self.API_key,
        "modelName": "Address",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName": city,
                "Limit": limit
            }
        }
        # correct request for json data
        res = requests.post(url=self.urls['settlements'], headers=self.headers, data=json.dumps(data_settlements))
        if 'data' in res.json().keys():
            cities_quantity = res.json()['data'][0]['TotalCount']
            addresses = res.json()['data'][0]['Addresses']
            return addresses, cities_quantity
        return 'Not correct request or no conn to server.'
    
    # def find_delivery_city(self, city:str, limit:int):
    #     """Preprocessing rough data. Getting names and refs of cities and total quantity 
    #     of cities, where Nova Poshta working. Returning tuple of 2 values."""
    #     res = self.rough_settlements_searching(city, limit)
    #     city_names_refs = []
    #     city_quantity = res.json()['data'][0]['TotalCount']
    #     for item in res.json()['data'][0]['Addresses']:
    #         city_names_refs.append({'city': item['Present'], 'ref': item['Ref']})
    #     return city_names_refs, city_quantity

    def get_street(self, street:str, settlement_ref:str,  limit:int):
        """Searching for streets in Nova Poshta. API key required."""
        data_streets = {
        "apiKey": self.API_key,
        "modelName": "Address",
            "calledMethod": "searchSettlementStreets",
            "methodProperties": {
                "StreetName": street,
                "SettlementRef": settlement_ref,
                "Limit": limit
            }
        }
        res = requests.post(url=self.urls['streets'], headers=self.headers, data=json.dumps(data_streets))
        return res
    
    def get_postal_office(self, city:str, postal_office:str):
        data_postal_office = {
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityName": city,
                "FindByString": "Відділення №{}".format(postal_office)
                },
            "apiKey": self.API_key
            }
        res = requests.post(url=self.urls['postal_office'], headers=self.headers, data=json.dumps(data_postal_office))
        # post_offices = []
        # for item in res.json()['data']:
        #     post_offices.append({'name': item['DescriptionRu'],'ident_num': item['Ref'], 'address': item['ShortAddressRu']})
        post_offices = res.json()['data']
        return post_offices
    
    def get_postal_offices_fm_city(self, city:str):
        try:
            city_list, quant = self.get_city(city, 20)
            print(city_list[0]['Present'])
            city_ref = city_list[0]['Ref']
            data = {
                "modelName": "AddressGeneral",
                "calledMethod": "getWarehouses",
                "methodProperties": {
                    "SettlementRef": city_ref
                    },
                "apiKey": self.API_key
                }
            res = requests.post(url=self.urls['postal_office'], headers=self.headers, data=json.dumps(data))
            return res
        except ValueError as e:
            return "No city list. Get_city method not working."

   

new_con = NovaPoshtaAPI(API_key=NOVA_POSHTA_API_KEY, headers=HEADERS)
res = new_con.get_postal_offices_fm_city('одеса')
print('++++++++++++++++++++++++++++++++++++++++++++++++++')
print(res.json())
# res = new_con.get_postal_office('одеса', '24')
# print(res.json())
# cities, total = new_con.get_city('ник', 10)
# print(cities, total)



#Working XML example!!!!!!!!!!!!!!!
# url2 = 'http://testapi.novaposhta.ua/v2.0/xml/Address/searchSettlements/'
# headers2 = {'Content-Type': 'text/xml; charset=UTF-8'}
# data2 = """<?xml version="1.0" encoding="UTF-8"?>
# <file>
# <apiKey>[ВАШ КЛЮЧ]</apiKey>
# <modelName>Address</modelName>
# <calledMethod>searchSettlements</calledMethod>
# <methodProperties>
# <CityName>київ</CityName>
# <Limit>5</Limit>
# </methodProperties>
# </file>""".encode('utf-8')

# res2 = requests.post(url=url2, headers=headers2, data=data2)

# print(res2.content.decode('utf-8'))