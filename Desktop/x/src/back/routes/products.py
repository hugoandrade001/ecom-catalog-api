# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from back.routes import products_bp
from back.services.product_service import ProductService

@products_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_products():
    """
    Lista todos os produtos
    GET /api/products/
    """
    try:
        products = ProductService.get_all()
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """
    Busca um produto por ID
    GET /api/products/<id>
    """
    try:
        product = ProductService.get_by_id(product_id)

        if not product:
            return jsonify({'error': 'Produto nao encontrado'}), 404

        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """
    Cria um novo produto
    POST /api/products/
    Body: {"nome": "...", "marca": "...", "valor": 99.99}
    """
    try:
        data = request.get_json()

        # Validacoes
        if not data:
            return jsonify({'error': 'Dados nao fornecidos'}), 400

        if not data.get('nome'):
            return jsonify({'error': 'Nome eh obrigatorio'}), 400

        if not data.get('marca'):
            return jsonify({'error': 'Marca eh obrigatoria'}), 400

        if not data.get('valor'):
            return jsonify({'error': 'Valor eh obrigatorio'}), 400

        try:
            valor = float(data['valor'])
            if valor <= 0:
                return jsonify({'error': 'Valor deve ser maior que zero'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Valor invalido'}), 400

        # Cria o produto
        product = ProductService.create(
            nome=data['nome'],
            marca=data['marca'],
            valor=valor
        )

        return jsonify(product.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """
    Atualiza um produto existente
    PUT /api/products/<id>
    Body: {"nome": "...", "marca": "...", "valor": 99.99}
    """
    try:
        data = request.get_json()

        # Validacoes
        if not data:
            return jsonify({'error': 'Dados nao fornecidos'}), 400

        # Valida valor se fornecido
        if 'valor' in data:
            try:
                valor = float(data['valor'])
                if valor <= 0:
                    return jsonify({'error': 'Valor deve ser maior que zero'}), 400
                data['valor'] = valor
            except (ValueError, TypeError):
                return jsonify({'error': 'Valor invalido'}), 400

        # Atualiza o produto
        product = ProductService.update(product_id, data)

        if not product:
            return jsonify({'error': 'Produto nao encontrado'}), 404

        return jsonify(product.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    Deleta um produto
    DELETE /api/products/<id>
    """
    try:
        success = ProductService.delete(product_id)

        if not success:
            return jsonify({'error': 'Produto nao encontrado'}), 404

        return jsonify({'message': 'Produto deletado com sucesso'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
