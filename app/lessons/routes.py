from flask import request, jsonify
from flask_login import login_required, current_user
from app.models import Lesson, UserProgress, User
from app import db
from app.lessons import lessons_bp
import datetime

@lessons_bp.route('/', methods=['GET'])
@login_required
def get_lessons():
    lessons = Lesson.query.order_by(Lesson.order_index).all()
    lessons_data = []
    for lesson in lessons:
        progress = UserProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
        is_completed = progress.is_completed if progress else False

        lessons_data.append({
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "challenge_question": lesson.challenge_question,
            "options": {
                "a": lesson.option_a,
                "b": lesson.option_b,
                "c": lesson.option_c,
                "d": lesson.option_d
            },
            "explanation": lesson.explanation,
            "points_awarded": lesson.points_awarded,
            "is_completed": is_completed
        })
    return jsonify(lessons_data), 200

@lessons_bp.route('/<int:lesson_id>', methods=['GET'])
@login_required
def get_lesson_detail(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"message": "Lesson not found"}), 404

    progress = UserProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
    is_completed = progress.is_completed if progress else False

    return jsonify({
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "challenge_question": lesson.challenge_question,
        "options": {
            "a": lesson.option_a,
            "b": lesson.option_b,
            "c": lesson.option_c,
            "d": lesson.option_d
        },
        "explanation": lesson.explanation,
        "points_awarded": lesson.points_awarded,
        "is_completed": is_completed
    }), 200

@lessons_bp.route('/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    data = request.get_json()
    user_answer = data.get('answer', '').strip().lower()

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"message": "Lesson not found"}), 404

    progress = UserProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
    if progress and progress.is_completed:
        return jsonify({"message": "Lesson already completed"}), 400

    # Verificar se a resposta está correta (comparar com correct_option)
    is_correct = user_answer == lesson.correct_option.lower()
    
    if is_correct:
        if not progress:
            progress = UserProgress(user_id=current_user.id, lesson_id=lesson.id)
        progress.is_completed = True
        progress.completed_at = datetime.datetime.utcnow()
        db.session.add(progress)

        current_user.points += lesson.points_awarded
        db.session.add(current_user)
        db.session.commit()

        return jsonify({
            "message": "Parabéns! Resposta correta!",
            "points_awarded": lesson.points_awarded,
            "user_total_points": current_user.points,
            "correct": True,
            "explanation": lesson.explanation
        }), 200
    else:
        return jsonify({
            "message": "Resposta incorreta. Tente novamente!",
            "correct": False,
            "correct_answer": lesson.correct_option.upper(),
            "explanation": lesson.explanation
        }), 200

@lessons_bp.route('/current_user_progress', methods=['GET'])
@login_required
def get_user_progress():
    user_progresses = UserProgress.query.filter_by(user_id=current_user.id, is_completed=True).all()
    completed_lesson_ids = [p.lesson_id for p in user_progresses]

    all_lessons = Lesson.query.order_by(Lesson.order_index).all()
    next_lesson = None
    for lesson in all_lessons:
        if lesson.id not in completed_lesson_ids:
            next_lesson = {
                "id": lesson.id,
                "title": lesson.title,
                "content": lesson.content,
                "challenge_question": lesson.challenge_question,
                "points_awarded": lesson.points_awarded
            }
            break

    return jsonify({
        "total_points": current_user.points,
        "completed_lessons_count": len(completed_lesson_ids),
        "next_lesson": next_lesson,
        "completed_lesson_ids": completed_lesson_ids
    }), 200
    
@lessons_bp.route('/', methods=['POST'])
@login_required
def create_lesson():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    challenge_question = data.get('challenge_question')
    option_a = data.get('option_a')
    option_b = data.get('option_b')
    option_c = data.get('option_c')
    option_d = data.get('option_d')
    correct_option = data.get('correct_option', '').lower()
    explanation = data.get('explanation', '')
    points_awarded = data.get('points_awarded', 10)
    order_index = data.get('order_index')

    if not all([title, content, challenge_question, option_a, option_b, option_c, option_d, correct_option, order_index is not None]):
        return jsonify({"message": "Todos os campos obrigatórios são necessários."}), 400

    if correct_option not in ['a', 'b', 'c', 'd']:
        return jsonify({"message": "correct_option deve ser 'a', 'b', 'c' ou 'd'"}), 400

    if Lesson.query.filter_by(order_index=order_index).first():
        return jsonify({"message": f"Já existe uma lição com o índice de ordem {order_index}. Escolha outro."}), 409

    try:
        new_lesson = Lesson(
            title=title,
            content=content,
            challenge_question=challenge_question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
            explanation=explanation,
            points_awarded=points_awarded,
            order_index=order_index
        )
        db.session.add(new_lesson)
        db.session.commit()

        return jsonify({
            "message": "Lição criada com sucesso!",
            "lesson": {
                "id": new_lesson.id,
                "title": new_lesson.title,
                "order_index": new_lesson.order_index
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar lição: {str(e)}"}), 500
