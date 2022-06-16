#!/usr/bin/env python

from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
api = Api(app)

## database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freight.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## models
class Orgs(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.String, primary_key=True)
    code = db.Column(db.String, unique=True)
    shipment = db.relationship('Shipments', backref='orgs')

    def __repr__(self):
        return f"{self.id}"


class Shipments(db.Model):
    __tablename__ = 'shipments'
    id = db.Column(db.String, primary_key=True)
    eta = db.Column(db.String, nullable=True)
    org_id = db.Column(db.String, db.ForeignKey('organizations.id'))
    weight = db.Column(db.Integer, nullable=True, default=None)
    unit = db.Column(db.String, nullable=True, default=None)

    def __repr__(self):
        return f"{self.id}"


## routes
class Organization(Resource):
    def get(self, id):
        org = Orgs.query.get(id)
        return jsonify(id=org.id, code=org.code) if org else abort(404, message=f"{id} not found.")


    def post(self):
        data = json.loads(request.get_json())
        id, code = data['id'], data['code']

        ## debugging
        app.logger.debug(f"{data} {type(data)} --> post payload")

        ## insert if org exists, else update
        org = Orgs.query.get(id)
        if org is None:
            app.logger.info(f"org {id} does not exist")
            new_org = Orgs(id=id, code=code)
            db.session.add(new_org)
        else:
            app.logger.info(f"org {id} exists")
            org.id = id
            org.code = code
            db.session.add(org)

        db.session.commit()
        return jsonify(data)


class Shipment(Resource):

    def get(self, id):
        ship = Shipments.query.get(id)
        return jsonify(id=ship.id, eta=ship.eta, org_id=eval(ship.org_id), weight=ship.weight, unit=ship.unit) if ship else abort(404, message=f"{id} not found.")


    def post(self):
        data = json.loads(request.get_json())
        id = data['referenceId']

        ## substitute list of org codes with list of org ids
        org_id = repr([str(Orgs.query.filter_by(code=org).first()) for org in data['organizations']])

        ## debugging
        app.logger.debug(f"{data} {type(data)} --> post payload")

        ## some shipments will not have an eta
        eta = data.get('estimatedTimeArrival', None)

        ## some shipments will have no transport packs
        weight, unit = None, None
        if data['transportPacks']['nodes']:
            weight = int(data['transportPacks']['nodes'][0]['totalWeight']['weight'])
            unit = data['transportPacks']['nodes'][0]['totalWeight']['unit']

        ## check for existing shipment
        shipment = Shipments.query.get(id)
        if shipment is None:
            new_shipment = Shipments(id=id, eta=eta, org_id=org_id, weight=weight, unit=unit)
            db.session.add(new_shipment)
        else:
            shipment.id = id
            shipment.eta = eta
            shipment.org_id = org_id
            shipment.weight = weight
            shipment.unit = unit
            db.session.add(shipment)

        db.session.commit()
        return jsonify(data)


api.add_resource(Organization, '/organization', '/organization/<string:id>')
api.add_resource(Shipment, '/shipment/<string:id>', '/shipment')

if __name__ == '__main__':
    app.run(debug=True)
