# -*- coding: utf-8 -*-
'''数据库调用'''
import sys

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy as SQLAlchemyOriginal


class SQLAlchemy(SQLAlchemyOriginal):
    def apply_driver_hacks(self, app, info, options):
        # refer: https://dev.mysql.com/doc/connector-python/
        if info.drivername in ['mysql+mysqlconnector', 'mysql+pymysql']:
            options['connect_args'] = {'time_zone': 'Asia/Shanghai'}
        elif info.database == ':memory:':
            if 'sqlite3' not in globals():
                import sqlite3
            sqlite_uri = 'file::memory:?cache=shared'
            sqlite_params = {
                'check_same_thread': False
            }
            if sys.version_info.major == 3:
                sqlite_params['uri'] = True
            options['creator'] = lambda: sqlite3.connect(sqlite_uri, **sqlite_params)
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
