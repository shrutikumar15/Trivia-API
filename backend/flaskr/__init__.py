from sqlalchemy.exc import SQLAlchemyError
from models import setup_db, Question, Category
import random
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
import os
import sys
sys.path.append('../')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    app.config['DEBUG'] = True
    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/*": {"origins": "*"}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    QUESTIONS_PER_PAGE = 10

    def paginate_questions(page, selection):
        start = (page-1)*QUESTIONS_PER_PAGE
        end = (page+1)*QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.route('/categories')
    def get_categories():
        categories = []
        results = Category.query.order_by(Category.type).all()
        #results = []
        print(results)
        if len(results) == 0:
            abort(404)
        for category in results:
            categories.append(category.type)
        return jsonify({
            'categories': categories,
            'success': True
        }), 200

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        page = request.args.get('page', 1, type=int)
        print(page)
        current_questions = paginate_questions(page, selection)
        categories = Category.query.order_by(Category.type).all()
        if(len(current_questions)) == 0:
            abort(404)
        return jsonify({
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': None,
            'success': True
        }), 200
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.filter_by(id=question_id).first()
            print(question)
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(Question.query.all())
            }), 200
        except:
            abort(422)
        # question

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def addQuestion():
        body = request.get_json()
        print(body)
        try:
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')
            print(question)
            print(answer)
            print(category)
            print(difficulty)
            if question=='' or answer =='' or category=='' or difficulty=='':
              abort(422)
        except:
            abort(422)
        try:
            new_question = Question(question=question, answer=answer,
                                    category=category, difficulty=difficulty)
            print(new_question)
            new_question.insert()
            # id = Question.query.filter_by(Question.question=question).first()
            new_quest = (new_question.format())
            id = new_quest.get("id", "")
            print(id)
            return jsonify({
                'success': True,
                'created': id,
                'total_questions': len(Question.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()
            result = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': result,
                'total_questions': len(result),
                'current_category': Category.query.filter(Category.id == category_id).first().type
            }), 200
        except:
            abort(404)
    ''' 
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            req = request.get_json('searchTerm')
            if req.get("searchTerm", "") == '':
              abort(404)
            searchStr = '%'+req.get("searchTerm", "")+'%'
            print(searchStr)
            questions = Question.query.filter(
                Question.question.like(searchStr)).all()
            result = [question.format() for question in questions]
            categories = [question.category for question in questions]
            return jsonify({
                'success': True,
                'questions': result,
                'total_questions': len(result),
                'current_category': categories
            }), 200
        except:
            abort(404)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/quizzes', methods=['GET', 'POST'])
    def play_quiz():
        try:
            req = request.get_json()
            print(req)
            previous_questions = req.get("previous_questions", "")
            quiz_category = req.get("quiz_category", "")
            category = quiz_category.get("id", "")
            if previous_questions =='' or quiz_category.get("id","")=='' or quiz_category.get("type","")=='':
              abort(422)
            print(previous_questions)
            print(category)
            if category == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter_by(category=category).filter(
                    Question.id.notin_(previous_questions)).all()

            print(questions)
            result = questions[random.randrange(0, len(questions))].format() if len(
                questions) > 0 else None
            print(result)
            return jsonify({
                'success': True,
                'question': result
            }), 200
        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
    return app
