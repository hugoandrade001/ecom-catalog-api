from back import db
from datetime import datetime

class Product(db.Model):
      __tablename__ = 'products'

      id = db.Column(db.Integer, primary_key=True)
      nome = db.Column(db.String(200), nullable=False)         
      marca = db.Column(db.String(100), nullable=False)        
      valor = db.Column(db.Numeric(10, 2), nullable=False)     
      created_at = db.Column(db.DateTime, default=datetime.utcnow)  

      def to_dict(self):
        return {
              'id': self.id,
              'nome': self.nome,
              'marca': self.marca,
              'valor': float(self.valor),
              'created_at': self.created_at.isoformat()
          }

      def __repr__(self):
        return f'<Product {self.nome}>'