# Flask freight API

This is a basic freight API example using the python flask framework.

## Build Docker Image

From the base directory, build the `freight:latest` docker image.
```
bash% docker build -t freight:latest .
```
## Set Database Credentials
Place your database credentials in the `.env` file in the flask application directory.
```
MYSQL_ROOT_USER=root
MYSQL_ROOT_PASSWORD=yoursecretpassword
MYSQL_DATABASE=freight
MYSQL_HOST=db
```
## Run docker-compose Up

Start the flask application container along with a mysql container using `docker-compose`. The flask application will be exposed on port 5000 on localhost.
```
bash% docker-compose up
```
## Create Database Tables

The database tables must be manually created using flask shell on the running application container.
```
bash% IMAGE=$(docker ps | grep freight:latest | awk {'print $1'})
bash% docker exec -it $IMAGE /bin/bash
```
We need to set the `APP` environment variable to point to our flask application in order for flask shell to work.
```
root@24d659330ee0:/freight# APP=freight.py flask shell
Python 3.9.10 (main, Mar  2 2022, 04:23:34)
[GCC 10.2.1 20210110] on linux
App: freight [production]
Instance: /freight/instance
>>> from freight import db
>>> db.create_all()
```
## Populating The Database

In the `test` directory, there is a python utility to populate the database using a provided set of JSON payloads and the `/organization/id` and `/shipment/id` endpoints.
```
root@24d659330ee0:/freight/test# ./populate.py
```
## Organization Endpoint

- Organizations can be created or modified by posting valid JSON to the `/organizations/<id>` endpoint.
- Existing organizations can be viewed by accessing the `/organizations/<id>` endpoint.
```
bash% curl -S -s http://localhost:5000/organization/381f5cc5-dfe4-4f58-98ad-116666855ca3 | jq .
{
  "code": "SEA",
  "id": "381f5cc5-dfe4-4f58-98ad-116666855ca3"
}
```
## Shipment Endpoint

- Shipments can be created or modified by posting valid JSON to the `/shipments/<id>` endpoint.
- Existing shipments can be viewed by accessing the `/shipments/<id>` endpoint.
```
bash% curl -s -S http://localhost:5000/shipment/S00001175 | jq .
{
  "eta": "2020-11-20T00:00:00",
  "id": "S00001175",
  "org_id": [
    "381f5cc5-dfe4-4f58-98ad-116666855ca3"
  ],
  "unit": "KILOGRAMS",
  "weight": 3
}
```
## Grossweight Endpoint

- The `/grossweight/<unit>` endpoint will return the total weight of all shipments in the specified unit.
- Supported units are kilograms, pounds and ounces.
```
bash% curl -S -s http://localhost:5000/grossweight/pounds | jq .
{
  "unit": "pounds",
  "weight": 50112.511
}
```
## Running docker-compose Down

When finished, tear down the containers using `docker-compose`.
```
bash% docker-compose down -v
Stopping freight_app_1 ... done
Stopping freight_db_1  ... done
Removing freight_app_1 ... done
Removing freight_db_1  ... done
Removing network freight_default
```