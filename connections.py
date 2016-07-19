conn = psycopg2.connect(connection)
cursor = conn.cursor()
items = item_scraper.load(open(item_scraper,"rb"))

for item in items:
    city = item[0]
    price = item[1]
    info = item[2]

    query =  "INSERT INTO items (info, city, price) VALUES (%s, %s, %s);"
    data = (info, city, price)

    cursor.execute(query, data)

def store(data):
	conn = psycopg2.connect()

	for x in range(len(data)):
		d = data.pop()
		try:
			cur = conn.cursor()
			cur.execute('INSERT INTO items(auction_id, item_id, item_name, auction_price, value_price, win_time, url, winner, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', (d[0], d[2], d[3], d[4], d[5], d[6], d[1]))
		except psycopg2.DatabaseError, e:
			print 'Error %s' % e
			sys.exit(1)

	conn.commit()
	conn.close()