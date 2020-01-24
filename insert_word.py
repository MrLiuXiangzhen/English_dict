import pymysql
import re

f = open('dict.txt')

db = pymysql.connect('0.0.0.0', 'root', 'Root@123', 'dict')

cur = db.cursor()
sql = 'insert into words (word,mean) values (%s,%s)'

for line in f:
    # 获取匹配内容元组（Word，mean)
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]
    try:
        cur.execute(sql, tup)
        db.commit()
    except Exception as e:
        db.rollback()
        print("Error:", e)

f.close()
cur.close()
db.close()
