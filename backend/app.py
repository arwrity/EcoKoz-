from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Report {self.id} - {self.category}>"


fake_districts = [
    {
        "name": "Свалка у реки",
        "latitude": 51.162,
        "longitude": 71.467,
        "description": "Горы мусора на берегу"
    },
    {
        "name": "Промышленный дым",
        "latitude": 51.155,
        "longitude": 71.480,
        "description": "Загрязнение воздуха от завода"
    },
    {
        "name": "Мало деревьев",
        "latitude": 51.159,
        "longitude": 71.472,
        "description": "Нехватка зелёных зон"
    }
]


@app.route('/')
def index():
    return render_template('index.html', districts=fake_districts)


@app.route('/district/<int:district_id>')
def district(district_id):
    return jsonify({"data": []})



@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description')
        latitude = float(request.form.get('latitude', 0))
        longitude = float(request.form.get('longitude', 0))

        new_report = Report(
            category=category,
            description=description,
            latitude=latitude,
            longitude=longitude
        )

        db.session.add(new_report)
        db.session.commit()

        return render_template('thanks.html')
    else:
        return render_template('report.html')



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'mkdb':
        with app.app_context():  
            db.create_all()
            print("📦 База данных создана!")
    else:
        app.run(debug=True)

