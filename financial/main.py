from cgitb import reset
from typing import Union
import sqlite3
from fastapi import FastAPI
from math import *
from datetime import datetime,date

app = FastAPI()
con = sqlite3.connect("../schema.sql", check_same_thread=False)
cur = con.cursor()  


@app.get("/api/financial_data")
async def read_item(  start_date: Union[date, None] = None, 
                end_date: Union[date, None] = None,
                symbol: Union[str, None] = None,
                limit:Union[str, None] = 5,
                page: Union[int, None] = None):

    answer = {
        "data" : [],
        "pagination" : {},
        "info": {'error': ''}
    }

    if not start_date and not end_date:
        answer["info"] = {'error': 'Start date and End date is needed'}
        return answer

    if not start_date:
        answer["info"] = {'error': 'Start date is needed'}
        return answer

    if not end_date:
        answer["info"] = {'error': 'End date is needed'}
        return answer

    # Making the query
    query = '''SELECT * FROM financial_data 
                        WHERE date BETWEEN "{}" AND "{}"'''.format(end_date,start_date)
    if symbol: 
        query += '''AND symbol= "{}" '''.format(symbol)
    count_query = cur.execute(query)
    count = len(count_query.fetchall())
    query +='''LIMIT {}'''.format(limit)
    if page:
        offset = (page - 1) * limit
        query +=' OFFSET {}'.format(offset)

    res = cur.execute(query).fetchall()

    # Formating the dict to return
    #data
    for row in res:
        answer["data"].append({
            "symbol": row[0],
            "date": row[1],
            "open_price": row[2],
            "close_price": row[3],
            "volume": row[4],
        })

    #pagination

    answer["pagination"] = {
        "count": count,
        "page": page,
        "limit": limit,
        "pages": ceil(count/limit)
    }

    #info
    if len(res) == 0:
        answer["info"] = {'error': 'No data available'}
        return answer

    return answer


@app.get("/api/statistics") 
async def read_item(  start_date: Union[date, None] = None, 
                end_date: Union[date, None] = None,
                symbol: Union[str, None] = None):

    answer = {
        "data" : {},
        "info": {'error': ''}
    }

    if not start_date and not end_date:
        answer["info"] = {'error': 'Start date and End date is needed'}
        return answer

    if not start_date:
        answer["info"] = {'error': 'Start date is needed'}
        return answer

    if not end_date:
        answer["info"] = {'error': 'End date is needed'}
        return answer


    # Making the query
    query = '''SELECT 
                avg(open_price),
                avg(close_price),
                avg(volume)
                FROM financial_data 
                WHERE date BETWEEN "{}" AND "{}"'''.format(end_date,start_date)
    
    if symbol: 
        query += '''AND symbol= "{}"'''.format(symbol)

    res = cur.execute(query).fetchall()
    try:
        for row in res:
            answer["data"] = {
                "start_date": start_date,
                "end_date": end_date,
                "symbol": symbol,
                "average_daily_open_price": "%.2f" % row[0],
                "average_daily_close_price": "%.2f" % row[1],
                "average_daily_volume": int(row[2]),
            }
    except TypeError:
        answer["info"] = {'error': 'No data available'}
        return answer
    return answer