# API

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

  currency-conversion-api:
    image: fabbo/currency-conversion-api:latest
    container_name: currency-conversion-api
    env_file:
      - ./currency_conversion_api.env
    volumes:
      - ./logs:/var/log/api
      #- ./certs:/certs:ro  # Uncomment for HTTPS
    ports:
      - "18070:80"
      #- "18071:443"  # Uncomment for HTTPS
    restart: unless-stopped
    networks:
      - currency-conversion-api-net

networks:
  currency-conversion-api-net:
~~~

6. Once the containers are up and running, you can access the API at http://localhost:18070/api/v1/currency.

7. Refer to the API documentation at API Documentation for detailed information on available endpoints and their usage.

## Environment Variables

| NAME                | DESCRIPTION                                                      |
| ------------------- | ---------------------------------------------------------------- |
| ALLOWED_HOSTS       | List of strings representing the allowed host/domain names       |
| CORS_HOSTS          | CORS allowed hosts (url format)                                  |
| CSRF_HOSTS          | CSRF allowed hosts (url format)                                  |
| RUN_JOBS            | Enable jobs execution (true or false). Default: ***false***      |
| USE_HTTPS           | Enable HTTPS (true or false). Default: ***false***               |
| DATABASE_URL        | Databse url                                                      |
| CURRENCY_CODES      | Currency codes allowed (they have to be valid)                   |
| MAX_STORED_DAYS     | Max number of days without removing conversions. Default: 20     |
| MAX_NO_UPDATED_MINS | Max number of minutes without saving new conversions. Default: 5 |

## Error Codes

| CODE | DEFINITION                         | ENDPOINT                |
| ---- | ---------------------------------- | ----------------------- |
| 1    | Currency code not supported        | /conversion/{code}      |
| 2    | Too many days to fetch conversions | /conversion/days/{days} |

## Documentation

For detailed documentation about development, please refer to our [Code Documentation](./src/README.md).
