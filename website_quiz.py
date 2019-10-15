import requests
import sqlite3
from pprint import pprint
import pandas
import matplotlib as plt

token = "pk_9619ca5e25cb4466880b7b1b6a68cfaa"

iex_base = "https://cloud.iexapis.com/stable"

quote_endpoint = iex_base + "/stock/{}/quote?token="

response1 = requests.get(quote_endpoint.format("fb") + token)
response2 = requests.get(quote_endpoint.format("ibm") + token)
            # requests.push(quote_endpoint.format("ibm"), content)

quote_data1 = response1.json() 
quote_data2 = response2.json() 

ds = [quote_data1, quote_data2]
# print(ds)
d = {}
for k in quote_data1.keys():
  d[k] = tuple(d[k] for d in ds)
# print(d)  # combined two dictionaries into d, printed {'symbol': ('FB', 'IBM')], ....,....}
#print(quote_data)  # its a dictionary

dictlist = [] #convert the dictionary into a list [symbol,(FB,IBM),CompanyName,(facebook, international bus.    )]
temp = []
for key, value in d.items():
    temp = [key,value]
    dictlist.append(temp)
# print(dictlist)

# for i in dictlist:
#   print(i)

def create_table(dbname="website.db"):
    with sqlite3.connect(dbname) as conn:

        cur = conn.cursor()
        SQL = """DROP TABLE IF EXISTS website; """

        cur.execute(SQL)
        cur = conn.cursor()

lines = [[i] for i in dictlist] 
    # lines = lines.split(',')
    #print(lines)
columns = lines[0]
body = lines[1:]


    # columns = columns.split(',')
conn = sqlite3.connect("website.db")
cur = conn.cursor()      

SQL = """CREATE TABLE quote ("""
for column in columns:
    # print(column)
    # column = column[0].split(",")
    # print(type(column))
    SQL = SQL + column
    # print(type(SQL))
    # print(SQL)
    SQL = SQL + "); "
    # print(SQL)
cur.execute(SQL)
conn.commit()

for line in body:
    line = line[0].split(',')
        
  
    SQL ="INSERT INTO quote VALUES (" 
#         # for i, val in enumerate(list(line)):
    for val in line:
            SQL += val + " " 
    SQL += ");"
    # print(SQL)
cur.execute(SQL)

def SELECT():
    SQL = "SELECT * FROM quote WHERE symbol ='FB';"
    cursor.execute(SQL)
    pprint(cursor.fetchall())

def DELETE_WHERE():
    SQL = "DELETE FROM FROM quote WHERE symbol ='IBM';"
    cursor.execute(SQL)

df = pd.DataFrame(d)

def clean_data(df):
    for i in df:
        all_types = {}
        for i in df[i]:
            if type(i) in all_types:  #check for type errors by filter for the most appeared type
                all_types[type(i)] += 1
            else:
                all_types[type(i)] = 1

        max_val = max(all_types.values())

        for i in all_types:
            if all_types[i] == max_val:
                max_key = i

        for index in range(len(df[i])):
            if not(isinstance(df[i][index], max_key)) and len(all_types) > 1:
                df[i][index] = None
    return df

df = clean_data(df)
#line graph to show the distance and direction between the week52Low price to latestPrice
x1 = (quote_data1['week52Low'], quote_data1['latestPrice']) 
x2 = (quote_data2['week52Low'], quote_data2['latestPrice'])
y1 = (range(1,13)) #represents 12 months
y2 = (range(1,13)) 
plt.plot(x2, y2, label = "line 2")
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Two or more lines on same plot with suitable legends ')
plt.legend()
plt.show()