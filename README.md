# Currency Conversion API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Welcome to the Currency Conversion API! This service provides a convenient way to obtain currency conversion rates and historical conversion data for multiple currencies. The API allows you to access real-time exchange rates and retrieve conversion history for a specified time period.

## Features
* Get real-time exchange rates for a variety of currencies.
* Convert an amount from one currency to another.
* Retrieve historical conversion rates for a specific time range.
* Support for multiple languages and frameworks.
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

## Getting Started

To get started with the Currency Conversion API, please follow these steps:

1- Review the API documentation for detailed information on each endpoint and their usage.

2- Choose the language version that suits your project requirements and access the corresponding repository.

3- Follow the installation instructions and integrate the service into your application.

4- Start making requests to the API endpoints using your API key.

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

## Support

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/FabboMaster)

If you have any questions, concerns, or need assistance, please don't hesitate to reach out. We are here to help you make the most of our Currency Conversion API.

Happy coding!