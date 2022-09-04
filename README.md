# FSND/Udacity-API Development and Documentation Project

## Udacitriavia App

> _Quick link to navigate_:
>
> - [Frontend](./README.md#frontend---udacitrivia)
> - [Backend](./README.md#backend---udacitrivia)
> - [API Reference](./README.md#api-reference)
> - [Testing](./README.md#testing-1)

Users of this Udacitrivia Project can compete against friends or test their general knowledge by playing a trivia game. The project's objective was to develop an API and unittests for the application's implementation, enabling it to do the following:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

### Frontend - Udacitrivia

> _tip_: Since this frontend relies on a Flask-based backend to function, it will not load properly if the backend is down or disconnected. It is advised that the backend be set up first, followed by testing using Postman or curl, updating the frontend's endpoints, and then a seamless frontend integration.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

Wait till finish the installation

> _tip_: `npm i`is shorthand for `npm install`

### Running your Frontedn in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.

Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

```
npm start
```

> _Quick link to navigate_:
>
> - [Frontend](./README.md#frontend---udacitrivia)
> - [Backend](./README.md#backend---udacitrivia)
> - [API Reference](./README.md#api-reference)
> - [Testing](./README.md#testing-1)

## Backend - Udacitrivia

> _tip_:Prerequesites Dependencies: Python3, PIP3, node and npm installed with postgres

    - Python 3.7 or later will work fine on local

    - Using virtual environment you will need to install / upgrade / downgrade Python 3.7

### Installing Dependencies

### Virtual Environment

> _tip_: When using Python for projects, we advise working in a virtual environment. This keeps the dependencies you have for each project organized and separate. This site contains instructions for creating a virtual environment for your platform.

### PIP Dependencies

After your virtual environment is up and running, by going to the 'backend' Directory, install dependencies using this command:

```bash
pip install -r requirements.txt
```

After installing all required packages, list them to check using this command:

```bash
pip list
```

All dependencies located in the file requirements.txt should be successful installed

### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

> _Quick link to navigate_:
>
> - [Frontend](./README.md#frontend---udacitrivia)
> - [Backend](./README.md#backend---udacitrivia)
> - [API Reference](./README.md#api-reference)
> - [Testing](./README.md#testing-1)

## API Reference

### Getting Started

> _tip_:Authentication: This version of the application does not require authentication or API keys.

### This app Meet This Requirements

1. The Use Flask-CORS to enable cross-domain requests and set response headers.
2. An endpoint that handle:

- `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
- `GET` requests for all available categories.
- `DELETE` a question using a question `ID`.
- `POST` a new question, which will require the question and answer text, category, and difficulty score.
- `POST` request to get questions based on category.
- `POST` request to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
- `POST` request to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

3. Error handlers for all expected errors including 400, 404, 422, and 500. etc

> _tip_:Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
> Authentication: This version does not require authentication or API keys.

## Endpoints Documenting

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

There are six types of errors this API will return;

- 400 - bad request
- 404 - page not found
- 422 - unprocessable resources
- 405 - Invalid method!
- 500 - Internal server error
- 406 - Not Acceptable

Documentation of API endpoints including the URL, request parameters with sampled example;

### Endpoints Example

`GET 'categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- `curl http://127.0.0.1:5000/categories`

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "total_categories": 6
}
```

`GET '/questions'`

- Returns a list of questions
- Includes a list of categories
- Paginated in groups of 10
- `curl http://127.0.0.1:5000/questions`

```json
{
  "success": true,
  "questions": [
    {
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4
    },
    {
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4
    },
    {
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2
    },
    {
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?",
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1
    },
    {
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3
    },
    {
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4
    },
    {
      "id": 12,
      "question": "Who invented Peanut Butter?",
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2
    },
    {
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2
    },
    {
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3
    },
    {
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?",
      "answer": "Agra",
      "category": 3,
      "difficulty": 2
    }
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "all available"
}
```

DELETE '/questions/<int:id>'

- Deletes a question by id using url parameters
- Returns id of deleted questions if successful
- `curl -X DELETE http://127.0.0.1:5000/questions/22`

```json
{
  "success": true,
  "deleted_question": {
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?",
    "answer": "Blood",
    "category": 1,
    "difficulty": 4
  },
  "remaining_questions": 18
}
```

POST'/questions'

- Creates a new question using JSON request parameters in the database
- `curl -X POST -H "Content-Type: application/json" -d '{"question": "What is your name?", "answer": "You", "difficulty": 1, "category": "1" }' http://127.0.0.1:5000/questions`

```json
{
  "success": true,
  "created_question": {
    "id": 56,
    "question": "What is your name?",
    "answer": "You",
    "category": 2,
    "difficulty": 1
  },
  "total_questions": 19
}
```

POST'/questions/search'

- Searches for questions using a search term
- `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "country"}' http://127.0.0.1:5000/questions/search`

```json
{
  "success": true,
  "questions": [
    {
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4
    }
  ],
  "total_questions": 1,
  "current_category": "any"
}
```

## Testing

### Error Handling

Success and error behavior of each endpoint using the unittest library.

First deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

This API passed all 13 test

> _Quick link to navigate_:
>
> - [Frontend](./README.md#frontend---udacitrivia)
> - [Backend](./README.md#backend---udacitrivia)
> - [API Reference](./README.md#api-reference)
> - [Testing](./README.md#testing-1)
