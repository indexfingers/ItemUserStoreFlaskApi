from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# every resource has to be a class - here we have class student which inherits
# from Resource. Student essentially becomes a copy of the Resource class, but wiht a couple of things changed
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = 'this field cannot be left blank'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help = 'every item needs a store id'
    )

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'},404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        # item  = ItemModel(name, data['price'], data['store_id'])
        item  = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred inserting the item'}, 500 # internal server error

        return item.json(), 201


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()



class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        itemsJson = [item.json() for item in items]
        # alternatively:
        # itemsJson = list(map(lambda x: x.json(), ItemModel.query.all()))

        return {'items':itemsJson}
