# -*- coding: utf-8 -*-
from back.model.product import Product
from back import db
from flask import current_app
import json

class ProductService:
    """
    Service responsavel pela logica de produtos com cache Redis
    """

    CACHE_KEY = 'products:all'
    CACHE_TTL = 300  # 5 minutos

    @staticmethod
    def get_all():
        """
        Lista todos os produtos (com cache Redis)

        Returns:
            List[Product]: Lista de produtos
        """
        try:
            # Tenta buscar do cache
            redis_client = current_app.redis
            cached = redis_client.get(ProductService.CACHE_KEY)

            if cached:
                # Cache hit - retorna do Redis
                print("Cache HIT - Produtos do Redis")
                product_ids = json.loads(cached)
                products = [Product.query.get(pid) for pid in product_ids]
                # Filtra None caso algum produto tenha sido deletado
                return [p for p in products if p is not None]

            # Cache miss - busca do banco
            print("Cache MISS - Buscando do banco")
            products = Product.query.order_by(Product.created_at.desc()).all()

            # Salva no cache (so os IDs para economizar memoria)
            product_ids = [p.id for p in products]
            redis_client.setex(
                ProductService.CACHE_KEY,
                ProductService.CACHE_TTL,
                json.dumps(product_ids)
            )

            return products

        except Exception as e:
            # Se Redis falhar, busca do banco normalmente
            print(f"Redis error: {e}")
            return Product.query.order_by(Product.created_at.desc()).all()

    @staticmethod
    def get_by_id(product_id):
        """
        Busca um produto por ID

        Args:
            product_id (int): ID do produto

        Returns:
            Product: Produto ou None
        """
        return Product.query.get(product_id)

    @staticmethod
    def create(nome, marca, valor):
        """
        Cria um novo produto

        Args:
            nome (str): Nome do produto
            marca (str): Marca do produto
            valor (float): Valor do produto

        Returns:
            Product: Produto criado
        """
        try:
            product = Product(
                nome=nome.strip(),
                marca=marca.strip(),
                valor=valor
            )

            db.session.add(product)
            db.session.commit()

            # Invalida o cache
            ProductService._clear_cache()

            return product

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(product_id, data):
        """
        Atualiza um produto existente

        Args:
            product_id (int): ID do produto
            data (dict): Dados para atualizar

        Returns:
            Product: Produto atualizado ou None se nao encontrado
        """
        try:
            product = Product.query.get(product_id)

            if not product:
                return None

            # Atualiza apenas os campos fornecidos
            if 'nome' in data:
                product.nome = data['nome'].strip()

            if 'marca' in data:
                product.marca = data['marca'].strip()

            if 'valor' in data:
                product.valor = data['valor']

            db.session.commit()

            # Invalida o cache
            ProductService._clear_cache()

            return product

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(product_id):
        """
        Deleta um produto

        Args:
            product_id (int): ID do produto

        Returns:
            bool: True se deletado, False se nao encontrado
        """
        try:
            product = Product.query.get(product_id)

            if not product:
                return False

            db.session.delete(product)
            db.session.commit()

            # Invalida o cache
            ProductService._clear_cache()

            return True

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def _clear_cache():
        """
        Limpa o cache de produtos no Redis
        """
        try:
            redis_client = current_app.redis
            redis_client.delete(ProductService.CACHE_KEY)
            print("Cache invalidado")
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
