from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:228322zt@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

#分页获取用户列表
@app.route('/get_user_list', methods=['GET'])
def get_user_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users_query = User.query.paginate(page=page, per_page=per_page, error_out=False)
    users = users_query.items
    total = users_query.total
    return jsonify({
        'total': total,
        'list': [{'id': user.id, 'name': user.name, 'gender': user.gender} for user in users]
    })

#新增用户
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], gender=data['gender'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'success'}), 200

#编辑用户
@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data['name']
    user.gender = data['gender']
    db.session.commit()
    return jsonify({'message': 'success'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=5174,debug=False)
