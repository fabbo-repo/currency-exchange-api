# API (Python)

## Installation and Usage

To quickly set up and test the Currency Conversion API, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone the repository from GitHub.

3. Navigate to the project directory.

4. Create **currency_conversion_api.env** file with appropriate environment variables.

5. Build and run the Docker containers using the following command:

~~~
docker-compose up -d
~~~

or use a custom docker-compose file:

~~~
version: '3'

services:

  api:
    image: fabbo/currency-conversion-api-djangorest:latest
    container_name: currency-conversion-api
    env_file:
      - ./currency_conversion_api.env
    volumes:
      - ./logs:/var/log/api
      #- ./certs:/certs:ro  # Uncomment for HTTPS
    depends_on:
      - db
    ports:
      - "18070:80"
      #- "18071:443"  # Uncomment for HTTPS
    restart: unless-stopped
    networks:
      - currency_conversion_api_net

networks:
  currency_conversion_api_net:
    ipam:
      driver: default
~~~

6. Once the containers are up and running, you can access the API at http://localhost:18070/api/v1/currency.

7. Refer to the API documentation at API Documentation for detailed information on available endpoints and their usage.

## Documentation

For detailed documentation, including information on environment variables, error codes, and useful commands, please refer to our [API Documentation](./api/README.md).