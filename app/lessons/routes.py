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

    if user_answer == lesson.challenge_answer.strip().lower():
        if not progress:
            progress = UserProgress(user_id=current_user.id, lesson_id=lesson.id)
        progress.is_completed = True
        progress.completed_at = datetime.datetime.utcnow()
        db.session.add(progress)

        current_user.points += lesson.points_awarded
        db.session.add(current_user)
        db.session.commit()

        return jsonify({
            "message": "Lesson completed successfully!",
            "points_awarded": lesson.points_awarded,
            "user_total_points": current_user.points,
            "correct": True
        }), 200
    else:
        return jsonify({"message": "Incorrect answer. Try again!", "correct": False}), 200

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