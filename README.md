# Foodgram Project

## Table of Contents
* [Description](#description)
* [Technologies](#technologies)
* [Installation](#installation)
* [Usage](#usage)
* [API Documentation](#api-documentation)
* [Contributing](#contributing)
* [License](#license)

## Description
Foodgram is a web application that allows users to create, share, and browse recipes. Users can also add ingredients to a shopping list and print the list out for use at the grocery store. The project was created for the Yandex.Practicum Python Developer course and is based on the Django framework.

## Technologies
* Django
* Django REST Framework
* PostgreSQL
* Nginx
* Gunicorn
* Docker
* JavaScript
* React

## Installation
To run this project, you will need to install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/). Once these are installed, follow these steps:

1. Clone this repository to your local machine.
2. In the root directory, create a file called `.env` and set the following environment variables:
3. Run the following command in the root directory to start the containers:
```bash
docker-compose up
```
4. Once the containers are running, open your browser and go to `http://localhost`.

## Usage
After following the installation steps, you can use the application to:

* Create an account
* Browse recipes
* Create, edit, and delete your own recipes
* Add ingredients to your shopping list
* Print your shopping list

## API Documentation
The Foodgram API documentation is available at `http://localhost/api/docs/` once the containers are running.

## Contributing
Contributions to this project are welcome! If you find a bug or would like to suggest a new feature, please open an issue. Pull requests are also welcome.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
