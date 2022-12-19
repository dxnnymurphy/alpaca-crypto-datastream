# datastream
This is a data pipeline that can be used to query REST APIs for financial data which is then stored in Kafka topics. The data was used for vizualising in a Grafana dashboard through Materialize DB (shown in another repo), and for testing of reinforcement models.

## Structure:
This is a program that uses a Golang Proxy to provide a REST endpoint with grpcui and swagger support, which interacts via grpc with a python service which retrieves data from various endpoints.

## Initial Support:
The first endpoint chosen was the Alpaca market data API, specifically the crypto market due to it's 24/7 availability as the Wall St market data didn't work well due to the time difference with the UK.

Other endpoints are easily added due to the factory design principle.