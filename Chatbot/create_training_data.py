import sqlite3
import pandas as pd

timeframes = ['2011-04']

for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor() ## what does cursor do?
    limit = 5000
    last_unix = 0
    cur_length = limit
    counter = 0
    test_done = False
    while cur_length == limit:
        sql = "SELECT * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix, limit)
        # print(sql)
        df = pd.read_sql(sql, connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)
        print(cur_length, limit)
        if not test_done: ## if false
            with open("test.from", 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')
            with open("test.to",'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(str(content)+'\n')
            
            test_done = True
        else:
            with open("train.from", 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')
            with open("train.to",'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(str(content)+'\n')            
        
        counter += 1
        # if counter % 2 == 0:
        print(counter, counter*limit, 'rows completed so far')








