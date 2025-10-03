from back import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco
        print("Banco de dados inicializado!")

    app.run(debug=True, host='0.0.0.0', port=5001)
