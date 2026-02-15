from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'class_routine.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classes', methods=['GET'])
def get_classes():
    data = load_data()
    day_filter = request.args.get('day', '').strip()
    if day_filter:
        data = [cls for cls in data if cls['day'].lower() == day_filter.lower()]
    return jsonify(data)

@app.route('/api/classes', methods=['POST'])
def add_class():
    new_class = request.json
    data = load_data()
    new_class['id'] = len(data) + 1
    data.append(new_class)
    save_data(data)
    return jsonify({'message': 'Class added successfully!'}), 201

@app.route('/api/classes/<int:cls_id>', methods=['PUT'])
def update_class(cls_id):
    data = load_data()
    for cls in data:
        if cls['id'] == cls_id:
            cls.update(request.json)
            save_data(data)
            return jsonify({'message': 'Class updated successfully!'})
    return jsonify({'error': 'Class not found'}), 404

@app.route('/api/classes/<int:cls_id>', methods=['DELETE'])
def delete_class(cls_id):
    data = load_data()
    data = [cls for cls in data if cls['id'] != cls_id]
    save_data(data)
    return jsonify({'message': 'Class deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)