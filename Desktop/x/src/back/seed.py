# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com dados iniciais
Cria um usuario admin padrao e alguns produtos de exemplo
"""

from back import create_app, db
from back.model.user import User
from back.model.product import Product

def seed_database():
    """
    Popula o banco com dados iniciais
    """
    app = create_app()

    with app.app_context():
        print("Iniciando seed do banco de dados...")

        # Cria as tabelas se nao existirem
        print("Criando tabelas...")
        db.create_all()

        # Limpa dados existentes (cuidado em producao!)
        print("Limpando dados antigos...")
        Product.query.delete()
        User.query.delete()
        db.session.commit()

        # Cria usuario admin
        print("Criando usuario admin...")
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Cria usuario de teste
        print("Criando usuario teste...")
        teste = User(
            username='teste',
            email='teste@example.com'
        )
        teste.set_password('teste123')
        db.session.add(teste)

        # Cria produtos de exemplo
        print("Criando produtos de exemplo...")

        produtos = [
            {
                'nome': 'iPhone 15 Pro',
                'marca': 'Apple',
                'valor': 7999.00
            },
            {
                'nome': 'Galaxy S24 Ultra',
                'marca': 'Samsung',
                'valor': 6999.00
            },
            {
                'nome': 'MacBook Pro M3',
                'marca': 'Apple',
                'valor': 15999.00
            },
            {
                'nome': 'Dell XPS 15',
                'marca': 'Dell',
                'valor': 8999.00
            },
            {
                'nome': 'AirPods Pro',
                'marca': 'Apple',
                'valor': 1999.00
            },
            {
                'nome': 'Galaxy Buds Pro',
                'marca': 'Samsung',
                'valor': 899.00
            }
        ]

        for prod in produtos:
            product = Product(
                nome=prod['nome'],
                marca=prod['marca'],
                valor=prod['valor']
            )
            db.session.add(product)

        # Salva tudo
        db.session.commit()

        print("\nSeed concluido com sucesso!")
        print("\nUsuarios criados:")
        print("   - Username: admin | Senha: admin123")
        print("   - Username: teste | Senha: teste123")
        print(f"\n{len(produtos)} produtos criados")

if __name__ == '__main__':
    seed_database()
