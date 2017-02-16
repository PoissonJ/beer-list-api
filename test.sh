docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up -d
docker logs -f beerlistapi_web_1
docker wait beerlistapi_web_1