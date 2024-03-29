from flask import g
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor

# def connect_db():
# 	sql=sqlite3.connect('/home/ffulan/Dev/Flask/UltimateFlask/qANDaApp/questions.db')
# 	sql.row_factory=sqlite3.Row
# 	return sql

# def get_db():
# 	if not hasattr(g,'sqlite_db'):
# 		g.sqlite_db=connect_db()
# 	return g.sqlite_db


def connect_db():
	conn=psycopg2.connect("postgres://jalhhvfwrsghwr:d3e0d0862f1a2dd18baf9d568eac247777bb0fc9b70b7bcbc5f9d0704873a584@ec2-54-221-214-3.compute-1.amazonaws.com:5432/dehgtt3ca1orsr",\
		cursor_factory=DictCursor)
	conn.autocommit=True
	sql=conn.cursor()
	return conn,sql

def get_db():
	db=connect_db()

	if not hasattr(g,'postgres_db_conn'):
		g.postgres_db_conn=db[0]

	if not hasattr(g,'postgres_db_cur'):
		g.postgres_db_cur=db[1]

	return g.postgres_db_cur


def init_db():
	db=connect_db()

	db[1].execute(open('schema.sql','r').read())
	db[1].close()
	db[0].close()




def init_admin():

	db=connect_db()

	db[1].execute("update users set admin=True where name=%s",('admin',))
	db[1].close()
	db[0].close()

