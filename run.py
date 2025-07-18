# run.py
from app import create_app, db

app = create_app()

# Para criar as tabelas ao iniciar o app (uma vez)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)