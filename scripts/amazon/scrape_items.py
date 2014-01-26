import pprint
import datetime
import math
import json
import sqlite3
import random

from amazonproduct import API
from amazonproduct.errors import *

from urllib2 import urlopen, HTTPError
from bs4 import BeautifulSoup


HTML_PRICE_CLASS = 'olpOfferPrice'

def get_api():
	return API(access_key_id='AKIAJFHSIA6LLFV26CHA', 
	      secret_access_key='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', 
	      associate_tag='6185-7386-2972',
	      locale='us')

api = get_api()

class Item:
	def __str__(self):
		return var_print(self)

class ItemListing:
	def __str__(self):
		return var_print(self)

class BrowseNode:
	def __str__(self):
		return var_print(self)

def var_print(o):
	return pprint.pformat(vars(o))

def aggregate_browse_node(id, sub_node=False):
	response_group = 'TopSellers' if sub_node else None
	result = api.browse_node_lookup(id, response_group=response_group)
	browse_node = BrowseNode()
	browse_node.id = id
	browse_node.name = result.BrowseNodes.BrowseNode.Name
	print('Found browse node {0}'.format(browse_node))
	if sub_node:
		items = []
		rank = 1
		for item in result.BrowseNodes.BrowseNode.TopItemSet.TopItem:
			i = aggregate_item(str(item.ASIN), rank)
			if i:
				items.append(i)
			rank += 1
		return {'browse_node' : browse_node, 'items' : items}
	else:
		browse_nodes = []
		for browse_sub_node in result.BrowseNodes.BrowseNode.Children.BrowseNode:
			browse_nodes.append(aggregate_browse_node( browse_sub_node.BrowseNodeId, True))
		return {'parent' : browse_node, 'sub_nodes' : browse_nodes}

def aggregate_item( asin, rank):
	result = api.item_lookup(asin, IdType='ASIN', ResponseGroup='Large,Offers,BrowseNodes')
	item_attributes = result.Items.Item.ItemAttributes
	item = Item()
	item.name = str(item_attributes.Title)
	item.asin = str(asin)
	item.rank = rank
	item.category = int(result.Items.Item.BrowseNodes.BrowseNode.BrowseNodeId)
	try:
		item.price = int(result.Items.Item.Offers.Offer.OfferListing.Price.Amount)
		try:
			listings = aggregate_item_listings( result.Items.Item.Offers.MoreOffersUrl)	
			print('Found item {0}'.format(item))
			return {'item' : item, 'listings' : listings}
		except AttributeError, e:
			print('Item "{0}" ({1}) has no 3rd party sellers'.format(item.name, item.asin))
			raise
	except AttributeError, e:
		print('Item "{0}" ({1}) has no offer'.format(item.name, item.asin))
		raise
	print('Found item {0}'.format(item))
	return {'item' : item, 'listings' : {}}

def aggregate_item_listings(base_url):
	url = str(base_url)
	html = ''
	while True:
		try:
			f = urlopen(url, timeout=30)
			html = f.read()
			break
		except HTTPError, e:
			if e.code == 503:
				pprint.pprint(e.msg)
			else:
				raise
	return parse_listings(BeautifulSoup(html))

def scrape_current_stock(listing):
	try:
		add_result = cart_create( {listing.offer_listing_id : 1})
		cart_id = add_result.Cart.CartId
		hmac = add_result.Cart.HMAC
		result = api.cart_modify(cart_id, hmac, {add_result.Cart.CartItems.CartItem[0].CartItemId : 999})
		listing.current_stock = result.Cart.CartItems.CartItem.Quantity
		listing.date_time = datetime.datetime.today()
		print(var_print(api.cart_clear(cart_id, hmac).Cart.CartItems))
	except AWSError, e:
			print(e)	
		

def scrape_listings(items):
	listings = []
	for l in items['listings']:
		#scrape_current_stock(items[j]['listings'][i])
		a = 10000/(l.price)
		l.date_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		t = datetime.datetime.today()
		u = t.hour * 3600 + t.minute * 60 + t.second
		l.current_stock = int(round(a*math.sin(86400/6.28*u)+1.5*a)) + random.randint(-10, 10)
		if l.current_stock < 0:
			l.current_stock *= -1
		l.item = items['item'].__dict__
		listings.append(l)
	return listings

def parse_listings(soup, listings=[]):
	for offer in soup.find(id='olpTabContent').select('.olpOffer'):
		il = ItemListing()
		il.offer_listing_id = offer.find(lambda tag: tag.name == 'input' and tag.has_attr('name') and tag['name'] == 'offeringID.1')['value']
		il.price = formatted_dollars_to_cents(str(offer.find('span', {'class' : HTML_PRICE_CLASS}).string).strip())
		shipping = offer.find('span', {'class' : 'olpShippingPrice'})
		if shipping:
			il.shipping = formatted_dollars_to_cents(str(shipping.string.strip()))		
		else:
			il.shipping = 0		
		listings.append(il)
	return listings

def formatted_dollars_to_cents(s):
	d, c = s.strip('$').split('.', 2)
	return int(d) * 100 + int(c)

def cart_create( items, **params):
        try:
            params.update(api._convert_cart_items(items, key='OfferListingId'))
            return api.call(Operation='CartCreate', **params)
        except AWSError, e:

            if e.code == 'AWS.MissingParameters':
                raise ValueError(e.msg)

            if e.code == 'AWS.ParameterOutOfRange':
                raise ValueError(e.msg)

            if e.code == 'AWS.ECommerceService.ItemNotEligibleForCart':
                raise InvalidCartItem(e.msg)

            # otherwise re-raise exception
            raise  # pragma: no cover

def splice_sequence(seq, n):
	sequences = []
	for i in range(0, len(seq), n):
		sequences.append(seq[i:min(i+n,len(seq))])
	return sequences

def save_mysql(listing):
	conn = sqlite3.connect('tracker.db')
	print('Connected to tracker.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS listings
             (current_stock, price, shipping, date_time, offer_listing_id, item) ''')
	c.execute('''CREATE TABLE IF NOT EXISTS items
             (asin, category, name, rank, price) ''')
	c.execute('SELECT rowid FROM items WHERE asin=?', (listing.item['asin'],))
	item_id = c.fetchone()
	if not item_id:
		c.execute('''INSERT INTO items
             	  	 VALUES (?, ?, ?, ?, ?)''', (listing.item['asin'], listing.item['category'], listing.item['name'], listing.item['rank'], listing.item['price']))
		item_id = c.lastrowid
	else:
		item_id = item_id[0]
	c.execute('''INSERT INTO listings
           	  	 VALUES (?, ?, ?, ?, ?, ?)''', (listing.current_stock, listing.price, listing.shipping, listing.date_time, listing.offer_listing_id, item_id))
	conn.commit()
	conn.close()

browse_node = aggregate_browse_node(165793011, True)
for i in browse_node['items']:
		for l in scrape_listings(i):
			save_mysql(l)




