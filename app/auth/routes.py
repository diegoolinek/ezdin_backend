from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from app.auth import auth_bp
import datetime


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    bio = data.get('bio')
    avatar_url = data.get('avatar_url')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409

    new_user = User(username=username, name=name, bio=bio, avatar_url=avatar_url)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "id": new_user.id,
        "username": new_user.username,
        "name": new_user.name,
        "bio": new_user.bio,
        "joined_date": new_user.joined_date.isoformat(), # Converter para string ISO 8601
        "avatar_url": new_user.avatar_url
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401

    login_user(user)

    session.permanent = True

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "points": user.points,
            "name": user.name,
            "bio": user.bio,
            "joined_date": user.joined_date.isoformat(),
            "avatar_url": user.avatar_url,
            "is_admin": user.is_admin
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route('/status', methods=['GET'])
def get_user_status():
    if current_user.is_authenticated:
        return jsonify({
            "is_authenticated": True,
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "points": current_user.points,
                # >>> Novos campos aqui <<<
                "name": current_user.name,
                "bio": current_user.bio,
                "joined_date": current_user.joined_date.isoformat(), # Converter para string ISO 8601
                "avatar_url": current_user.avatar_url,
                "is_admin": current_user.is_admin
            }
        }), 200
    else:
        return jsonify({"is_authenticated": False}), 200


@auth_bp.route('/profile', methods=['PUT'])
@login_required 
def update_profile():
    data = request.get_json()

    name = data.get('name')
    bio = data.get('bio')
    avatar_url = data.get('avatar_url')
    # O username e a senha geralmente não são atualizados nesta rota de perfil
    # mas poderiam ser adicionados com validação extra se necessário.

    user = current_user # Acessa o usuário logado

    try:
        if name is not None: # Apenas atualiza se o campo foi fornecido
            user.name = name
        if bio is not None:
            user.bio = bio
        if avatar_url is not None:
            user.avatar_url = avatar_url

        # Você pode adicionar um campo 'updated_at' no modelo User
        # para registrar a última atualização se quiser.
        # Por exemplo: user.updated_at = datetime.datetime.utcnow()

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "Perfil atualizado com sucesso!",
            "user": {
                "id": user.id,
                "username": user.username,
                "points": user.points,
                "name": user.name,
                "bio": user.bio,
                "joined_date": user.joined_date.isoformat(),
                "avatar_url": user.avatar_url,
                "is_admin": user.is_admin
            }
        }), 200

    except Exception as e:
        db.session.rollback() # Desfaz a transação em caso de erro
        return jsonify({"message": f"Erro ao atualizar perfil: {str(e)}"}), 500


# === ROTAS ADMINISTRATIVAS ===

@auth_bp.route('/admin/users', methods=['GET'])
@login_required
def get_all_users():
    """Rota para admins listarem todos os usuários"""
    if not current_user.is_admin:
        return jsonify({"message": "Acesso negado. Apenas administradores."}), 403
    
    users = User.query.all()
    users_data = []
    
    for user in users:
        users_data.append({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "points": user.points,
            "is_admin": user.is_admin,
            "joined_date": user.joined_date.isoformat(),
            "bio": user.bio
        })
    
    return jsonify({"users": users_data}), 200


@auth_bp.route('/admin/users/<int:user_id>/promote', methods=['PUT'])
@login_required
def promote_user_to_admin(user_id):
    """Rota para promover um usuário a administrador"""
    if not current_user.is_admin:
        return jsonify({"message": "Acesso negado. Apenas administradores."}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    try:
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": f"Usuário {user.username} promovido a administrador com sucesso!",
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "is_admin": user.is_admin
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao promover usuário: {str(e)}"}), 500


@auth_bp.route('/admin/users/<int:user_id>/demote', methods=['PUT'])
@login_required
def demote_user_from_admin(user_id):
    """Rota para remover privilégios de administrador de um usuário"""
    if not current_user.is_admin:
        return jsonify({"message": "Acesso negado. Apenas administradores."}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    # Prevenir que um admin se remova (opcional)
    if user.id == current_user.id:
        return jsonify({"message": "Você não pode remover seus próprios privilégios de administrador"}), 400
    
    try:
        user.is_admin = False
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": f"Privilégios de administrador removidos de {user.username}",
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "is_admin": user.is_admin
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao remover privilégios: {str(e)}"}), 500


@auth_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Rota para deletar um usuário (apenas para casos extremos)"""
    if not current_user.is_admin:
        return jsonify({"message": "Acesso negado. Apenas administradores."}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    # Prevenir que um admin se delete
    if user.id == current_user.id:
        return jsonify({"message": "Você não pode deletar sua própria conta"}), 400
    
    try:
        # Deletar progresses do usuário primeiro (devido à foreign key)
        from app.models import UserProgress
        UserProgress.query.filter_by(user_id=user.id).delete()
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message": f"Usuário {username} deletado com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao deletar usuário: {str(e)}"}), 500
