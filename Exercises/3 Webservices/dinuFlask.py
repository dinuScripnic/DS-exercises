from flask import Flask
from flask_restx import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api(app)
pets = []
birds = {}

petparser = reqparse.RequestParser()
petparser.add_argument('name', type=str, required=True)

birdparser = reqparse.RequestParser()
birdparser.add_argument('name', type=str, required=True)
birdparser.add_argument('color', type=str, required=True)
birdparser.add_argument('species', type=str, required=True)


class PetResource(Resource):
    @api.doc(parser=petparser)
    def post(self):
        args = petparser.parse_args()
        name = args['name']
        # check if the pet already exists
        if name in pets:
            name = name + str(random.randint(1, 100))
        pets.append(name)
        return 'Pet added', 201
    
    @api.doc(parser=petparser)
    def delete(self):
        args = petparser.parse_args()
        name = args['name']
        if name in pets:
            pets.remove(name)
            return 'Pet deleted', 200
        else:
            return 'Pet not found', 404

class BirdResource(Resource):
    def get(self):
        return birds
    
    @api.doc(parser=birdparser)
    def post(self):
        args = birdparser.parse_args()
        name = args['name']
        # check if the pet already exists
        if name in birds:
            name = name + str(random.randint(1, 100))
        birds[name] = {'color': args['color'], 'species': args['species']}
        return 'Bird added', 201
    
    @api.doc(parser=petparser)
    def delete(self):
        args = petparser.parse_args()
        name = args['name']
        if name in birds:
            del birds[name]
            return 'Bird deleted', 200
        else:
            return 'Bird not found', 404
        

api.add_resource(PetResource, '/pet')
api.add_resource(BirdResource, '/bird')

if __name__ == '__main__':
    app.run(debug=True)