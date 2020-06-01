# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 
 
## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
```bash
npm install
```
```bash
npm start
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

<img width="959" alt="2020-06-02 01_30_39-Mail" src="https://user-images.githubusercontent.com/41858958/83449321-09bf1980-a471-11ea-879e-089797ff3561.png">
<img width="947" alt="2020-06-02 01_31_33-Mail" src="https://user-images.githubusercontent.com/41858958/83449323-0a57b000-a471-11ea-8540-780f5a4ee064.png">
<img width="946" alt="2020-06-02 01_29_39-Mail" src="https://user-images.githubusercontent.com/41858958/83449326-0af04680-a471-11ea-9041-41662b9baf64.png">
<img width="958" alt="2020-06-02 01_30_27-Mail" src="https://user-images.githubusercontent.com/41858958/83449329-0af04680-a471-11ea-973f-309a493a13b7.png">

```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions?page=<page_number>'
- Fetches a dictionary of questions with each question having id, question, answer, category and difficulty
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Fetches questions only belonging to the page_number
- Fetches a key total_questions with value as the total number of questions
- Returns: An object with a four keys, 
                    1) categories, that contains a object of id: category_string key:value pairs.
                    2) current_category, that contains value current_category_id.
                    3) questions, that contains objects of id, question, answer, category and difficulty.
                    4) total_questions, that contains a key with total number of questions as value.
- Pagination : 10
- Request Arguments(optional): page_number

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    .
    .
    .
    ],
  "success": true,
  "total_questions": 19
}

DELETE '/questions/<question_id>'
- Fetches a key deleted with question_id as the value
- Fetches a key total_questions with value as the total number of questions
- Request Argument: question_id
{
  "deleted": 15,
  "success": true,
  "total_questions": 18
}

POST '/questions'
- Fetches a key craeted with id of the created question as the value
- Fetches a key total_questions with value as the total number of questions
- Sample Request json: 
{
	"question": "question",
	"answer": "answer",
	"category": 1,
	"difficulty": 1
}

{
  "created": 24, 
  "success": true, 
  "total_questions": 20
}

POST '/questions/search'
- Fetches a list of categories with the category id as elements
- Fetches a dictionary of questions with each question having id, question, answer, category and difficulty
- Fetches a key total_questions with value as the total number of questions
- Sample Request json:
{searchTerm: "what"}
- question is fetched if it contains searchTerm as a substring 
{
  "current_category": [
    2, 
    1
  ], 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}

POST '/quizzes'
- Fetches a dictionary of questions with each question having id, question, answer, category and difficulty
- Fetches questions only with category from the request json data
- Sample Request json:
{
  previous_questions: [], 
  quiz_category: {type: "Geography", id: "2"}
}

{
  "question": {
    "answer": "Jackson Pollock", 
    "category": 2, 
    "difficulty": 2, 
    "id": 19, 
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  }, 
  "success": true
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

