import pprint
import pymongo

from ebaysdk import merchandising, trading, shopping

DBHOST = 'localhost'
DBPORT = 27017
DBNAME = 'Tracker'

client = pymongo.MongoClient(DBHOST, DBPORT)
db = client[DBNAME]

def get_product(p_id, api):
	api.execute('FindProduct')

def get_product_items(p_id, api):
	api.execute('FindProducts', {
			'AvailableItemsOnly' : True,
			'ProductID' : {
				'@attrs': {'type': 'Reference'},
                '#text': p_id
			},
			'IncludeSelector' : 'Items'
		})
	return api.response_dict()

def get_most_watched_items(c_id, api):
	api.execute('getMostWatchedItems', {
			'categoryId' : c_id
		})
	return api.response_dict()

def get_multiple_items(item_ids, api):
	api.execute('GetMultipleItems', {
			'IncludeSelector' : 'Details',
			'ItemID' : ','.join(item_ids)
		})
	return api.response_dict()

def get_single_item(item_id, api):
	api.execute('GetSingleItem',{
			'IncludeSelector' : 'Details',
			'ItemID' : item_id
		})
	return api.response_dict()

def get_categories(api):
	api.execute('GetCategories', {'LevelLimit' : 1, 'DetailLevel' : 'ReturnAll'})
	return api.response_dict()

def get_sub_category(parent_c_id, api):
	pass

def get_top_selling_products(c_id, api):
	api.execute('getTopSellingProducts', {'categoryId' : c_id})
	return api.response_dict()



trade = trading(domain='api.sandbox.ebay.com',
			    appid="MatthewB-33a9-4d50-b56e-4398cece88d6",
			    devid="41d63e06-0775-4692-b656-896a9a4b39d8",
			    certid="5707a4f4-912d-4154-ac6e-d59ec72d3e75",
			    token="AgAAAA**AQAAAA**aAAAAA**wtLjUg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhC5iCowudj6x9nY+seQ**a4ECAA**AAMAAA**bz7sLZhXIMpFSPQQ/Jjkj8XQLJ5IeP/mLRf5oCVeXBmeX91trkLKBR9adYukIDIBwqpT+RxJwGBcdY8DiOu2Va3CWquDpDcGr32NrjS3tlDJp4z09e5vvJChiWD4jAlVgu0NVZKKOSMO/Uc5rYuZQQO0JPdTGbg+r4Lut7JwVJL5IthVTTv7Ec/53E0CAbjVGFBcWvquyeLJ4GUH5sNJM7a0yeNLIv8k4O8x+Aas3igY4LfLaDAOwziFrO83+7UHU9cyf4juHhxPTPvRhGvMdBwFJihLosQ7OPh8HNOecRnnm1cK5cziwjQCqGSJJpK9fB/7EtpKOK015Et2tHF18TWyYkSrbq7TPNoGVE7kAOLK8Q/dEEdlTyJrSq4gM/aBKKHzMwkTyYfzY0Fn+/wRTz6IlExWt6NLjJf6ByzZzk7jgh98VxQMgnYxaPyZ1sNlCuLaTbt2Ui866kIZsSJr7beY2cn6+58/cZuLaJgJoaYAtW526VUGSIHB1RE88cuXfafBgeviqjC6TDUVu1w9KGdGlQFPj38RFXXDbCriIe6P1jDtdl4vt02w9uVPWBDqxnVB+7q+N6sYSrMymhMHKXNr47y06drZdAqw3/ZCx2UMdMGYjyNjbZCg7LJUx5ZRCUPgJSPFSyaTv6c8viu8LLYwaH/QSKGpC8gFkGPqbvC1zUoq5E8H26NyKAO4+9ZqFnTqZxFAv82Ik94ybqGUYkC6TSBqvEBV/OC435/sVZZ+4+/GGCfCMPCuM2AlcvqM")

merch = merchandising(domain='svcs.sandbox.ebay.com',
					  appid='MatthewB-33a9-4d50-b56e-4398cece88d6')

shop = shopping(domain='open.api.sandbox.ebay.com',
				appid='MatthewB-33a9-4d50-b56e-4398cece88d6')

for product in get_top_selling_products(267, merch).productRecommendations.product:
	item_ids = []
	product_items = get_product_items(product.productId.value, shop)
	if product_items and product_items.ItemArray:	
		for item in product_items.ItemArray.Item:
			if not isinstance(item, basestring):
				db.items.save(get_single_item(item.ItemID, shop).Item)
		#	pprint.pprint(item)
		#	item_ids.append(item.ItemID)
		#for item in get_multiple_items(item_ids, shop):
		#	pprint.pprint(item)
		#	print('\n\n')

