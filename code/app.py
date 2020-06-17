from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Resource are concerned with entities eg Student. They are mapped with db

app = Flask(__name__)
app.secret_key = 'adil'
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates /auth end point

items = []

class Item(Resource): # inherits Resource

    # first user reqoarse to check if the keys exist as per requirement
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
        

    def get(self, name):
        filterObj = filter(lambda x: x['name'] == name, items)  #   filter returns a filter object and not an object
        item = next(filterObj, None)     #   next returns first item in a list, To avoid break if filter returns no item use None as default
        return {'item' : item}, 200 if item else 404                             #   not found

    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            return {'message': "An Item with name '{}' already exists".format(name)}, 400 #Bad request

        data = Item.parser.parse_args()
        # data=request.get_json(force=True) #force=True doesnt look for contect Type header
        # data=request.get_json(silent==True) #silent=True doesnt give an error, just returns None
        data = request.get_json()
        item = {'name' : name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args() # anyother requirements besides price will not be considered
        item = next(
            filter(lambda x: x['name'] == name, items)
            , None)
        if item is None:
            # create a new item
            item = {'name' : name, 'price' : data['price'] }
            items.append(item)
        else:
            # item exists, then update
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items') 

app.run(port = 5000, debug = True)