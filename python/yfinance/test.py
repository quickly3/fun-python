
from pandas_datareader import data as pdr
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from string import Template

import yfinance as yf
import os
import numpy as np

MY_DATABASE = 'execsearch'
MY_USERNAME = 'root'
MY_PASSWORD = 'root'

PG_HOST = '35.169.147.220'
PG_PORT = '5432'
PG_DATABASE = 'ciq_target'
PG_USERNAME = 'postgres'
PG_PASSWORD = 'Titan1qaz2wsx'


def pg_session():
    engine = create_engine("postgresql+psycopg2://"+PG_USERNAME+":"+PG_PASSWORD +
                           "@"+PG_HOST+"/"+PG_DATABASE, encoding='utf-8', echo=False)

    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    return session


def mysql_session():
    engine = create_engine("mysql+pymysql://"+MY_USERNAME+":"+MY_PASSWORD +
                           "@localhost/"+MY_DATABASE+"?charset=utf8", encoding='utf-8', echo=False)

    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    return session


def init_base_ticker():
    pg_s = pg_session()
    my_s = mysql_session()

    sql = """\
        SELECT c.companyid,re.exchangesymbol,ti.tickersymbol
        FROM ciqcompany as c
        JOIN ciqsecurity as s ON c.companyid = s.companyid
        JOIN ciqtradingitem as ti ON s.securityid = ti.securityid
        JOIN refexchange as re ON re.exchangeid = ti.exchangeid
        WHERE re.exchangeid in (104, 106,173,458)
        AND ti.tradingitemstatusid = 15
        AND ti.primaryflag = 1
        AND s.primaryflag = 1
       """

    try:
        resultproxy = pg_s.execute(
            text(sql)
        )
    except Exception as e:
        print(e)
        results = []
    else:
        results = resultproxy.fetchall()

    for item in results:
        sql_tpl = Template(
            "insert into ciq_exchange_ticker values(0,'${ciqid}','${exchange}','${ticker}','${ticker_adj}',0)")

        if item[2]:
            ticker_adj = item[2].replace(".", "")
            sql = sql_tpl.substitute(
                ciqid=item[0], exchange=item[1], ticker=item[2], ticker_adj=ticker_adj)

            my_s.execute(sql)
            my_s.commit()


def updateState(id, state):

    sql_tpl = Template(
        "update ciq_exchange_ticker set state=${state} where id=${id}")
    sql = sql_tpl.substitute(
        state=state, id=id)

    my_s.execute(sql)
    my_s.commit()


def ticker_count():
    sql = """\
        SELECT count(1)
        FROM ciq_exchange_ticker
        where state = 0
       """
    try:
        resultproxy = my_s.execute(
            text(sql)
        )
    except Exception as e:
        print(e)
        results = []
    else:
        results = resultproxy.fetchall()

    count = results[0][0]

    return count


def test():
    yf.pdr_override()  # <== that's all it takes :-)

    # download dataframe
    resp = pdr.get_data_yahoo(
        "GOOGL", start="2000-01-01", end="2019-12-15")

    if resp.empty == True:
        updateState(1990, 2)
    else:
        insert_stock_price(resp, "GOOGL")
        updateState(1990, 1)


def insert_stock_price(df, ticker_adj):

    datas = []

    for index, row in df.iterrows():
        data = [0, ticker_adj, row['Open'], row['High'], row['Low'],
                row['Close'], row['Adj Close'], row['Volume'], index]
        datas.append(data)

    datas_chunk = chunks(datas, 500)

    for chunk_datas in datas_chunk:
        sql = "insert into yf_ticker_price values"
        values_arr = []

        for item in chunk_datas:
            item_str = ('"'+item1+'"' for item1 in map(str, item))
            values_arr.append("("+",".join(item_str)+")")

        chunk_sql = sql+",".join(values_arr)

        my_s.execute(chunk_sql)
        my_s.commit()

    # print(datas)
    # print(datas)

    # val_tpl = Template(
    #     "(0,'${ciqid}','${exchange}','${ticker}','${ticker_adj}',0)")

    # if item[2]:
    #     ticker_adj = item[2].replace(".", "")
    #     sql = sql_tpl.substitute(
    #         ciqid=item[0], exchange=item[1], ticker=item[2], ticker_adj=ticker_adj)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def crawl_stock_price():

    count = ticker_count()
    current = 0
    sql = """\
        SELECT id,ticker
        FROM ciq_exchange_ticker where state = 0
       """
    try:
        resultproxy = my_s.execute(
            text(sql)
        )
    except Exception as e:
        print(e)
        results = []
    else:
        results = resultproxy.fetchall()

    for item in results:
        ticker = item[1]
        ticker_adj = ticker.replace(".", "")
        current += 1
        print(str(current)+"/"+str(count))
        print("Downloading:"+ticker_adj)

        id = item[0]

        yf.pdr_override()  # <== that's all it takes :-)

        # download dataframe
        resp = pdr.get_data_yahoo(
            ticker_adj, start="2000-01-01", end="2019-12-15")

        if resp.empty == True:
            updateState(id, 2)
        else:
            insert_stock_price(resp, ticker_adj)
            updateState(id, 1)


my_s = mysql_session()
crawl_stock_price()
