# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from util.parseYaml import conf


def make_session():
    db_connect_string = "mysql://%s:%s@%s:%d/%s?charset=utf8" % (
        conf['db']['user'], conf['db']['passwd'], conf['db']['host'],
        conf['db']['port'], conf['db']['name'])

    # pool_size 连接池个数， pool_recycle 空闲连接超时释放
    engine = create_engine(db_connect_string, encoding="utf-8", echo=False,
                           pool_size=10, pool_recycle=3600)
    sessions = scoped_session(sessionmaker(bind=engine))()
    return sessions


sessions = make_session()
