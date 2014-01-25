from amazonproduct import API
api = API(locale='us')
items = api.item_search('Books', Publisher="O'Reilly")