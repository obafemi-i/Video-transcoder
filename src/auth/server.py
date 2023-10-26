from flask import Flask, request
from flask_mysqldb import MySQL
import jwt
import datetime
from dotenv import dotenv_values

config = dotenv_values()

server = Flask(__name__)

mysql = MySQL()
mysql.init_app(server)

server.config['MYSQL_HOST'] = config['MYSQL_HOST']

print(server.config['MYSQL_HOST'])