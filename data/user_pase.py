from flask_restful import reqparse
import sqlalchemy

parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)