from faker import Faker
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' \
                                        'p1uK1:pN7NzP8OeVlTrp18flF4nzKihwYP8Ihn@' \
                                        'mydbinstance.czjuslhhuw2w.us-east-1.rds.amazonaws.com:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Rep(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    set_id = db.Column(db.Integer, db.ForeignKey("set.id"), nullable=False)
    balance_rating = db.Column(db.Integer)
    rep_duration = db.Column(db.Float)

    def __init__(self, set_id, balance_rating, rep_duration):
        self.set_id = set_id
        self.balance_rating = balance_rating
        self.rep_duration = rep_duration

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.before_first_request
def setup():
    db.Model.metadata.create_all(bind=db.engine)
    db.session.commit()


@app.route('/api/get-all')
def get_all():
    return jsonify({
        "reps": [r.as_dict() for r in Rep.query.all()],
        "sets": [s.as_dict() for s in Set.query.all()]
    })


@app.route('/api/get-set/<int:set_id>')
def get_reps(set_id):
    results = Rep.query.filter(Rep.set_id == set_id).all()
    return jsonify(results)


@app.route('/api/add-fake-data')
def add_fake_data():
    fake = Faker()
    sets = []
    for _ in range(0, 10):
        current_set = Set()
        db.session.add(current_set)
        sets.append(current_set)
    db.session.commit()

    for current_set in sets:
        for _ in range(0, 10):
            rep = Rep(set_id=current_set.id,
                      balance_rating=fake.random.randint(-1, 1),
                      rep_duration=fake.random.uniform(5, 10))
            db.session.add(rep)
    db.session.commit()

    return get_all()


@app.route('/')
def root():
    sets = {}

    for rep in Rep.query.all():
        if rep.set_id not in sets:
            sets[rep.set_id] = []

        sets[rep.set_id].append(rep)

    set_list = []
    for set_id, reps in sets.items():
        balances = [rep.balance_rating for rep in reps]
        average_balance = sum(balances) / len(balances)
        if abs(average_balance) < 0.2:  # good enough lol
            average_balance = 0

        set_list.append({
            "id": set_id,
            "average_balance": average_balance,
            "plot_data": {
                "x_axis_title": "Rep #",
                "y_axis_title": "Time to Completion (s)",
                "data_x": list(range(1, len(reps) + 1)),
                "data_y": [rep.rep_duration for rep in reps]
            }
        })

    return render_template("template.html", sets=set_list)


if __name__ == '__main__':
    app.run()
