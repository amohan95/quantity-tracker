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
	2350149011: 'MobileApps',
	2617941011: 'ArtsAndCrafts',
	2619525011: 'Appliances',
	2625373011: 'DVD',
	2972638011: 'LawnGarden',
	4991425011: 'Collectibles'
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

def explore_browse_sub_node(node, parent_id, root_id, sub_root_id):
	SUB_NODES[int(node.BrowseNodeId)] = (str(node.Name), parent_id, root_id, sub_root_id)
	if sub_root_id == 0:
		sub_root_id = int(node.BrowseNodeId)
	print ('Found Sub BrowseNode {0} with id {1} and parent {2}'.format(node.Name, node.BrowseNodeId, parent_id))
	try:
		for sub_node in node.BrowseNodes.BrowseNode.Children.BrowseNode:
			browse_node = api.browse_node_lookup(sub_node.BrowseNodeId)
			explore_browse_sub_node(sub_node, node.BrowseNodeId, root_id, sub_root_id)
	except AttributeError, e:
		print('Reached leaf node')

for id, name in BASE_NODES.items():
	browse_node_lookup = api.browse_node_lookup(id)
	BASE_NODES[int(browse_node_lookup.BrowseNodes.BrowseNode.BrowseNodeId)] = str(browse_node_lookup.BrowseNodes.BrowseNode.Name)
	print ('Found Base BrowseNode {0} with id {1}'.format(browse_node_lookup.BrowseNodes.BrowseNode.Name, browse_node_lookup.BrowseNodes.BrowseNode.BrowseNodeId))
	for browse_sub_node in browse_node_lookup.BrowseNodes.BrowseNode.Children.BrowseNode:
		explore_browse_sub_node(browse_sub_node, id, id, 0)

def sub_node_generator():
	for k, v in SUB_NODES.items():
		yield (k, v[0], v[1], v[2], v[3])

conn = sqlite3.connect('tracker.db')
print('Connected to tracker.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS categories (id, name, parent, root, sub_root)')
c.executemany('INSERT INTO categories (id, name) VALUES (?,?)', BASE_NODES.items())
c.executemany('INSERT INTO categories (id, name, parent, root, sub_root) VALUES (?, ?, ?, ?, ?)', sub_node_generator())
for node in BASE_NODES.items():
	print('INSERT INTO categories (id, name) VALUES ({0}, "{1}");'.format(int(node[0]), node[1]))
	c.execute('INSERT INTO categories (id, name) VALUES ({0}, "{1}")'.format(int(node[0]), node[1]))
for sub_node in sub_node_generator():
	print('INSERT INTO categories VALUES ({0},"{1}",{2}, {3}, {4});'.format(int(sub_node[0]), sub_node[1], int(sub_node[2]), int(sub_node[3]), int(sub_node[4])))
	c.execute('INSERT INTO categories VALUES ({0},"{1}",{2}, {3}, {4})'.format(int(sub_node[0]), sub_node[1], int(sub_node[2]), int(sub_node[3]), int(sub_node[4])))