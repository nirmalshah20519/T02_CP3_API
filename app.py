from flask import Flask, jsonify, request
from PrepareInput import create_normal_input, create_training_input, Teams, Grounds
from PrepareModel import model
from PrepareOutput import format_output
app = Flask(__name__)


# Route to create a new task
@app.route('/data', methods=['POST'])
def create_task():
    if not request.json or 'team1' not in request.json:
        return jsonify({'error': 'Team1 not provided'}), 400
    
    if request.json['team1'] not in Teams:
        return jsonify({'error': 'Team1 not valid'}), 400
    
    if not request.json or 'team2' not in request.json:
        return jsonify({'error': 'Team2 not provided'}), 400
    
    if request.json['team2'] not in Teams:
        return jsonify({'error': 'Team2 not valid'}), 400
    
    if not request.json or 'ground' not in request.json:
        return jsonify({'error': 'Ground not provided'}), 400
    
    if request.json['ground'] not in Grounds:
        return jsonify({'error': 'Ground not valid'}), 400
    
    team1 = request.json['team1']
    team2 = request.json['team2']
    ground = request.json['ground']
    normal = create_normal_input(team1, team2, ground)
    X = create_training_input(normal)
    y = model.predict(X)[0][0]
    response = format_output(y, team1, team2)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
