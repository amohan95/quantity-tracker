import sqlite3
import pprint

from amazonproduct import API

BASE_NODES = {
	130: 'Video',
	1000: 'Books',
	172282: 'Electronics',
	228239: 'Industrial',
	284507: 'Kitchen',
	301668: 'Classical',
	409488: 'Software',
	468240: 'Tools',
	468642: 'VideoGames',
	502394: 'Photo',
	541966: 'PCHardware',
	599872: 'Magazines',
	1036592: 'Apparel',
	1084128: 'OfficeProducts',
	3375251: 'SportingGoods',
	3760931: 'HealthPersonalCare',
	3880591: 'Jewelry',
	11055981: 'Beauty',
	11091801: 'MusicalInstruments',
	13900851: 'WirelessAccessories',
	15690151: 'Automotive',
	16310101: 'Grocery',
	133141011: 'KindleStore',
	165793011: 'Toys',
	165796011: 'Baby',
	377110011: 'Watches',
	2350149011L: 'MobileApps',
	2617941011L: 'ArtsAndCrafts',
	2619525011L: 'Appliances',
	2625373011L: 'DVD',
	2972638011L: 'LawnGarden',
	4991425011L: 'Collectibles'
}
 #'DigitalMusic':	195208011,
 #'GourmetFood':	3580501,
 #'HomeGarden':	285080,
 #'Miscellaneous':	10304191,
 #'MP3Downloads'	:195211011,
 #'OutdoorLiving'	:286168,
 #'PetSupplies':	12923371,
 #'VHS':	404272,
 #'Wireless':	508494,

SUB_NODES = {}

api = API(access_key_id='AKIAJFHSIA6LLFV26CHA', 
	      secret_access_key='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', 
	      associate_tag='6185-7386-2972',
	      locale='us')

for id, name in BASE_NODES.items():
	browse_node_lookup = api.browse_node_lookup(id)
	BASE_NODES[int(browse_node_lookup.BrowseNodes.BrowseNode.BrowseNodeId)] = str(browse_node_lookup.BrowseNodes.BrowseNode.Name)
	print ('Found Base BrowseNode {0} with id {1}'.format(browse_node_lookup.BrowseNodes.BrowseNode.Name, browse_node_lookup.BrowseNodes.BrowseNode.BrowseNodeId))
	for browse_sub_node in browse_node_lookup.BrowseNodes.BrowseNode.Children.BrowseNode:
		SUB_NODES[int(browse_sub_node.BrowseNodeId)] = (str(browse_sub_node.Name), id)
		print ('	Found Sub BrowseNode {0} with id {1}'.format(browse_sub_node.Name, browse_sub_node.BrowseNodeId))

def sub_node_generator():
	for k, v in SUB_NODES.items():
		yield (k, v[0], v[1])

conn = sqlite3.connect('tracker.db')
print('Connected to tracker.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS categories (id, name)')
c.executemany('INSERT INTO categories VALUES (?,?)', BASE_NODES.items())
c.execute('CREATE TABLE IF NOT EXISTS subcategories (id, name, parent)')
for sub_node in sub_node_generator():
	print('INSERT INTO subcategories VALUES ({0},"{1}",{2});'.format(sub_node[0], sub_node[1], str(sub_node[2])))