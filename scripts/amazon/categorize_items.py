import sqlite3

conn = sqlite3.connect('tracker.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('SELECT *, rowid FROM items')
for row in c.fetchall():
	c.execute('SELECT name FROM product_groups WHERE name = ?', (row['product_group'],))
	result = c.fetchone()
	if not result:
		c.execute('INSERT INTO product_groups (name) VALUES (?)', (row['product_group'],))
conn.commit()
conn.close()