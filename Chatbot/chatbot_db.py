import sqlite3
import json
from datetime import datetime
from pprint import pprint

timeframe = '2011-04'
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

def drop_table():
    c.execute(''' DROP TABLE parent_reply; ''')

def create_table():
    c.execute(''' CREATE TABLE IF NOT EXISTS parent_reply
            (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, 
            parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT) ''')

def format_data(data):
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")
    return data

def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1 ".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        # print("find_parent", e)
        return False


def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1 ".format(pid)
        # print(sql)
        c.execute(sql)
        result = c.fetchone()
        
        if result != None:
            return result[0]
        else:
            # print('No result find_existing_score')
            return False
    except Exception as e:
        # print("find_existing_score", e)
        return False

def acceptable(data):
    # pprint('acceptable ->' + data)
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == ['deleted'] or data == ['removed']:
        return False
    else:
        return True


def sql_insert_replace_comment(commentid, parentid, parent, comment, subreddit, time, score):
    try:
        sql = ''' UPDATE parent_reply SET parent_id = "{}", comment_id = "{}", parent = "{}", comment = "{}", subreddit = "{}", unix="{}", score = "{}" ; '''.format(parentid,commentid,parent, comment, subreddit, time, score)
        transaction_bldr(sql)
    except Exception as e:
        # print('sql_insert_replace_comment ', str(e))
        pass


def sql_insert_has_parent(commentid, parentid, parent, comment, subreddit, time, score):
    # if parent:
    #     print(commentid, parentid, '<>' + parent + '<>', comment, subreddit, time, score)
    # exit()
    try:
        sql = ''' INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}", "{}", "{}", "{}", "{}", "{}","{}");'''.format(parentid,commentid,parent, comment, subreddit, time, score)
        transaction_bldr(sql)
    except Exception as e:
        # print('sql_insert_has_parent ', str(e))
        pass

def sql_insert_no_parent(commentid, parentid, comment, subreddit, time, score):
    try:
        sql = ''' INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}", "{}", "{}", "{}", "{}","{}");'''.format(parentid,commentid, comment, subreddit, time, score)
        # print(sql)
        transaction_bldr(sql)
    except Exception as e:
        # print('sql_insert_no_parent ', str(e))
        pass
        # exit()

def transaction_bldr(sql):
    # print('transaction_bldr')
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 2000:
        # print('transaction_bldr IF....')
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
                # print('transaction executed successfully.....')
            except Exception as e:
                print(e)
            connection.commit()
            sql_transaction = []
    # else:
    #     print('seems there is some issue..')



if __name__ == "__main__":
    try:
        # drop_table()
        print('Table dropped...')
    except:
        print('Nothing to drop...')
        pass
    create_table()
    print('Table created...')

    row_counter = 0
    paired_rows = 0

    with open('/Users/rohitkhandale/ML/Chatbot/RC_2011-04', buffering=1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            comment_id = row['name']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            # print(row)
            parent_data = find_parent(parent_id)
            # print(row_counter, score, parent_data)
            # exit()

            if score >= 2 and acceptable(body):
                
                existing_comment_score = find_existing_score(parent_id)
                # exit()
                if existing_comment_score:
                    if score > existing_comment_score:
                        sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                        # exit()
                else:
                    if parent_data:
                        sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                        paired_rows += 1
                        # exit()
                    else:
                        # print('no parent...')
                        sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)
                        # exit()

            if row_counter % 100000 == 0:
                print('Total rows read: {}, paired rows: {}, time:{}'.format(row_counter, paired_rows, str(datetime.now())))
