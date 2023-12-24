# Currency Conversion API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Welcome to the Currency Conversion API! This service provides a convenient way to obtain currency conversion rates and historical conversion data for multiple currencies. The API allows you to access real-time exchange rates and retrieve conversion history for a specified time period.

## Features

* Get real-time exchange rates for a variety of currencies.
* Convert an amount from one currency to another.
* Retrieve historical conversion rates for a specific time range.
* Easy integration into your applications and systems.
* API Endpoints
* Get Latest Exchange Rates
* Internationalization, message support in English, Spanish and French.

## API Endpoints

### Get Currency info

~~~
GET /api/v1/currency
~~~

This endpoint returns all available currencies.

### Get Latest Exchange Rates

~~~
GET /api/v1/conversion/<CURRENCY>
~~~

This endpoint returns the latest exchange rates for an specific currency.

### Get Latest Exchange Rates

~~~
GET /api/v1/conversion/days/<DAYS>
~~~

This endpoint returns all stored currency cunversions for a number of days (maximum 30).

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

## Useful commands

* Create API key:

~~~bash
python manage.py apikey --username <USERNAME> --usage <USAGE>
~~~

* Execute migrations with docker compose

~~~bash
docker-compose run --entrypoint "sh" currency-conversion-api -c "python manage.py migrate"
~~~

## Support

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/FabboMaster)

If you have any questions, concerns, or need assistance, please don't hesitate to reach out. We are here to help you make the most of our Currency Conversion API.

Happy coding!
