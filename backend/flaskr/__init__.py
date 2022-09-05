import os
from sre_constants import SUCCESS
from unicodedata import category
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# ---------------------------
# Define question paginating
# ---------------------------


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

# ---------------------------
# Setup app
# ---------------------------


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS setup
    CORS(app)

    # CORS headers set access control to allows
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    # ---------------------------------------------
    # endpoint handle GET requests /all categories
    # ---------------------------------------------

    @app.route('/categories')
    def getall_categories():
        try:
            # by Default GET Method request

            # get all categories
            categories = Category.query.order_by(Category.id).all()

            # dictionary to hold retrieved categories
            categoryDict = {cat.id: cat.type for cat in categories}

            # abort if no category found
            if len(categoryDict) == 0:
                abort(404)
        except:
            abort(404)

        # return success message
        return jsonify(
            success=True,
            categories=categoryDict,
            total_categories=len(Category.query.all())
        )

    # -------------------------------------------------------------
    # endpoint handle GET requests /all questions + pagination(10)
    # -------------------------------------------------------------

    @ app.route('/questions')
    def getall_questions():
        try:
            # by Default GET Method request

            # get all questions respect to pagination aspect of 10
            selection = Question.query.order_by(Question.id).all()

            # pagination
            selected_questions = paginate_questions(request, selection)

            # get all categories
            categories = Category.query.order_by(Category.id).all()

            # dictionary to hold categories
            categoryDict = {cat.id: cat.type for cat in categories}

            # Abort if no questions found
            if len(selected_questions) == 0:
                abort(404)
        except:
            abort(404)
        # return success message
        return jsonify(
            success=True,
            questions=selected_questions,
            total_questions=len(selection),
            categories=categoryDict,
            current_category='all available'
        )

    # -------------------------------------------------
    # endpoint handle DELETE request using question_ID
    # -------------------------------------------------

    @ app.route("/questions/<int:id>", methods=['DELETE'])
    def remove_question(id):

        # Get question filter by id
        question = Question.query.filter_by(id=id).one_or_none()

        try:
            # delete that question
            question.delete()

        except:
            # Abort for no question found
            if question is None:
                abort(422)

        # return success message
        return jsonify(
            success=True,
            deleted_question=question.format(),
            remaining_questions=len(Question.query.all())
        )

    # ---------------------------------------------
    # endpoint handle POST requests /questions
    # ---------------------------------------------

    @ app.route("/questions", methods=['POST'])
    def new_question():
        try:
            # Requesting data
            body = request.get_json()

            # Abort no data found
            if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
                abort(406)

            # Adding ...
            add_question = body.get('question', '')
            add_answer = body.get('answer', '')
            add_difficulty = body.get('difficulty', '')
            add_category = body.get('category', '')

            # if not storing empty question continue...
            # raise error alert in frontend
            if not ((add_question == '') or (add_answer == '') or (add_difficulty == '') or (add_category == '')):

                # Inserting ...
                question = Question(
                    question=add_question,
                    answer=add_answer,
                    difficulty=add_difficulty,
                    category=add_category
                )

                # Storing ...
                question.insert()
        except:
            abort(404)
        # return a success message
        return jsonify(
            success=True,
            created_question=question.format(),
            total_questions=len(Question.query.all())
        )

    # -----------------------------------------------------------------
    # endpoint handle POST requests get questions based on search Term
    # -----------------------------------------------------------------

    @ app.route('/questions/search', methods=['POST'])
    def find_questions():
        try:
            # Requesting data
            body = request.get_json()
            search_Term = Question.query.filter(
                Question.question.ilike('%{}%'.format(body.get('searchTerm')))
            ).all()

            if not body.get('searchTerm'):
                # abort when nothing inserted
                abort(404)

            # else paginate if exceed above 10
            searched_questions = paginate_questions(request, search_Term)
        except:
            abort(404)
        # return success message
        return jsonify(
            success=True,
            questions=searched_questions,
            total_questions=len(search_Term),
            current_category='any'
        )
    # -------------------------------------------------------------
    # endpoint handle GET requests get question based on category
    # -------------------------------------------------------------

    @ app.route('/categories/<int:cat_id>/questions')
    def get_questions_by_category(cat_id):
        try:
            # By Default GET Method request
            # Filter Question with the given Category id
            all_questions = Question.query.filter_by(
                category=cat_id
            ).all()

            # pagination
            selected_questions = paginate_questions(request, all_questions)

            # abort when no questions found
            if len(selected_questions) == 0:
                abort(404)

            # variable to hold formated question
            questions = [qts.format() for qts in all_questions]
        except:
            abort(404)
        # return a success message
        return jsonify(
            success=True,
            current_category=cat_id,
            questions=questions,
            total_questions=len(all_questions)

        )
    # ----------------------------------------------------------------------------------
    # endpoint handle POST requests to get questions to play with respect to categories
    # ----------------------------------------------------------------------------------

    @ app.route('/quizzes', methods=['POST'])
    def start_quiz():
        try:
            # requesting data
            body = request.get_json()

            # abort when no data found
            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            # adding into variables
            quiz_cat = body.get('quiz_category')
            last_questions = body.get('previous_questions')

            # category not mention filter all questions
            question = Question.query.filter(
                Question.id.notin_(last_questions)).all() if not quiz_cat['id'] else ''

            # filter questions by category
            if quiz_cat['id']:
                question = Question.query.filter(
                    Question.category == quiz_cat['id'], Question.id.notin_(last_questions)).all()

            # random question
            new_question = random.choice(
                question).format() if len(question) > 0 else 'no questions found!'
        except:
            abort(404)
        return jsonify(
            success=True,
            question=new_question,
            current_category=quiz_cat['id'],
            remaining_question=len(question)
        )

    # ----------------------------------------------------------------
    # Expected error handlers includes [422, 404, 400, 405, 500, 406]
    # ----------------------------------------------------------------

    @ app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify(
            success=False,
            error=422,
            message='Unprocessable resources'
        ), 422

    @ app.errorhandler(404)
    def no_page_found(error):
        return jsonify(
            success=False,
            error=404,
            message='Page not found'
        ), 404

    @ app.errorhandler(400)
    def wrong_request(error):
        return jsonify(
            success=False,
            error=400,
            message='Bad request'
        ), 400

    @ app.errorhandler(405)
    def wrong_method(error):
        return jsonify(
            success=False,
            error=405,
            message='Invalid method!'
        ), 405

    @ app.errorhandler(500)
    def internal_server_error(error):
        return jsonify(
            success=False,
            error=500,
            message='Internal server error'
        ), 500

    @ app.errorhandler(406)
    def notAcceptable_error(error):
        return jsonify(
            success=False,
            error=406,
            message='Not Acceptable'
        ), 406

    return app
