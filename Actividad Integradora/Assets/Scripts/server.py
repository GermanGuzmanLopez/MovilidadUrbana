# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from robot_agents import *

# Size of the board:
number_agents = 5
number_boxes = 30
width = 10
height = 10
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents, number_boxes, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        number_boxes = int(request.form.get('KCajas'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 2

        print(request.form)
        print(number_agents, width, height)
        randomModel = robot_model(number_agents, number_boxes, width, height)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = []
        for i in randomModel.schedule.agents:
            agentPositions.append({"id": str(i.unique_id), "x": i.pos[0], "y": 1, "z": i.pos[1]})
        return jsonify({'positions':agentPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global randomModel

    if request.method == 'GET':
        carPositions = []
        for i in randomModel.bschedule.agents:
            carPositions.append({"id": str(i.unique_id), "x": i.pos[0], "y": 0.35, "z": i.pos[1]})

        return jsonify({'positions':carPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)