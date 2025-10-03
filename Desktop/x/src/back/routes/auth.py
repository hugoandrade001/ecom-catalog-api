from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from back.routes import auth_bp
from back.services.auth_service import AuthService

@auth_bp.route('/login', methods=['POST'])
def login():
  
    try:
        data = request.get_json()

        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username e password s�o obrigat�rios'}), 400

        user = AuthService.authenticate(data['username'], data['password'])

        if not user:
            return jsonify({'error': 'Credenciais invalidas'}), 401

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
  
    try:
        current_user_id = get_jwt_identity()
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
   
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(int(current_user_id))

        if not user:
            return jsonify({'error': 'Usu�rio n�o encontrado'}), 404

        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
