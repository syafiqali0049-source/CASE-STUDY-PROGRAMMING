from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geomatik_123'
# Database akan tercipta secara automatik dalam folder yang sama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab_geomatik.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Struktur Data (Table)
class LogPenggunaan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    id_pelajar = db.Column(db.String(20), nullable=False)
    no_komputer = db.Column(db.String(10), nullable=False)
    perisian = db.Column(db.String(50))
    masa = db.Column(db.DateTime, default=datetime.now)

# Bina database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            nama = request.form['nama']
            id_pelajar = request.form['id_pelajar']
            no_komputer = request.form['no_komputer']
            perisian = request.form['perisian']

            new_log = LogPenggunaan(nama=nama, id_pelajar=id_pelajar, no_komputer=no_komputer, perisian=perisian)
            db.session.add(new_log)
            db.session.commit()
            
            flash('Berjaya! Rekod anda telah disimpan.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ralat: {str(e)}', 'danger')
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
