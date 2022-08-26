import os
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
        # By Default GET Method request
        # get all categories
        categories = Category.query.order_by(Category.id).all()

        # Dictionary to hold retrieved categories
        cat_dict = {}
        for cat in categories:
            cat_dict[cat.id] = cat.type

        # Abort if no category found
        if len(categories) == 0:
            abort(404)

        return jsonify(success=True, categories=cat_dict, total_categories=len(Category.query.all()))

    # -------------------------------------------------------------
    # endpoint handle GET requests /all questions + pagination(10)
    # -------------------------------------------------------------

    @ app.route('/questions')
    def getall_questions():
        # By Default GET Method request
        # get all questions respect to pagination aspect of 10
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        # Dictionary to hold categories
        categories = Category.query.order_by(Category.type).all()
        cat_dict = {}
        for cat in categories:
            cat_dict[cat.id] = cat.type

        # Abort if no questions found
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            success=True,
            questions=current_questions,
            total_questions=len(selection),
            current_category={},
            categories=cat_dict
        )

    # -------------------------------------------------
    # endpoint handle DELETE request using question_ID
    # -------------------------------------------------

    @ app.route("/questions/<int:id>", methods=['DELETE'])
    def remove_question(id):
        # Get question filter by id
        try:
            question = Question.query.filter_by(id=id).one_or_none()

            # Abort is no question found by id
            if question is None:
                abort(404)

            # Else delete that question and return success message
            question.delete()

            return jsonify(
                success=True,
                deleted=id,
                total_qts=len(Question.query.all())
            )
        except:
            # Abort for no success delete
            abort(422)

    # ---------------------------------------------
    # endpoint handle POST requests /questions
    # ---------------------------------------------

    @ app.route("/questions", methods=['POST'])
    def new_question():
        # Requesting data
        body = request.get_json()

        # Abort no data found
        if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
            abort(405)

        # Adding ...
        add_question = body.get('question', '')
        add_answer = body.get('answer', '')
        add_difficulty = body.get('difficulty', '')
        add_category = body.get('category', '')

        # Abort for storing empty question
        if ((add_question == '') or (add_answer == '') or (add_difficulty == '') or (add_category == '')):
            abort(405)
        try:
            # Inserting ...
            question = Question(
                question=add_question,
                answer=add_answer,
                difficulty=add_difficulty,
                category=add_category
            )
            # Storing ...
            question.insert()

            # return a success message
            return jsonify(
                success=True,
                created=question.id,
                new_question=question.question,
                tot_questions=len(Question.query.all())
            )

        except:
            # Error in creating a question, Abort!
            abort(405)

    # -----------------------------------------------------------------
    # endpoint handle POST requests get questions based on search Term
    # -----------------------------------------------------------------

    @ app.route('/questions/search', methods=['POST'])
    def find_questions():
        # Requesting data
        body = request.get_json()
        search = body.get('searchTerm', None)

        # filter search with the given search Term
        if search:
            search_Term = Question.query.filter(
                Question.question.ilike(f'%{search}%')).all()

            # return a success message
            return jsonify(
                success=True,
                questions=[question.format() for question in search_Term],
                total_questions=len(search_Term),
                current_category=None
            )
        # else Abort!
        abort(404)
    # -------------------------------------------------------------
    # endpoint handle GET requests get question based on category
    # -------------------------------------------------------------

    @ app.route('/categories/<int:cat_id>/questions')
    def get_questions_by_category(cat_id):
        # By Default GET Method request
        # Filter Question with the given Category id
        try:
            all_questions = Question.query.filter(
                Question.category == str(cat_id)
            ).all()

            current_question = paginate_questions(request, all_questions)

            if len(current_question) == 0:
                abort(400)
            # return a success message
            return jsonify(
                success=True,
                questions=[qts.format() for qts in all_questions],
                total_questions=len(all_questions),
                current_category=cat_id
            )
        except:
            # else Abort when not found!
            abort(404)
    # ----------------------------------------------------------------------------------
    # endpoint handle POST requests to get questions to play with respect to categories
    # ----------------------------------------------------------------------------------

    @ app.route('/quizzes', methods=['POST'])
    def start_quiz():
        body = request.get_json()

        if not ('quiz_category' in body and 'previous_questions' in body):
            abort(422)

        quiz_cat = body.get('quiz_category')
        prev_questions = body.get('previous_questions')

        try:
            if quiz_cat['type'] == 'click':
                untaken_questions = Question.query.filter(
                    Question.id.notin_((prev_questions))).all()
            else:
                untaken_questions = Question.query.filter_by(
                    category=quiz_cat['id']).filter(Question.id.notin_((prev_questions))).all()

            question = untaken_questions[
                random.randrange(0, len(untaken_questions))
            ].format() if len(untaken_questions) > 0 else None

            return jsonify(
                success=True,
                question=question
            )
        except:
            abort(422)

    # -------------------------------------------------------------
    # Expected error handlers
    # -------------------------------------------------------------

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

    return app
