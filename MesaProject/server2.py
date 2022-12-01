# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from agents import *
from model import RandomModel
# Size of the board:
number_agents = 10
trafficModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, trafficModel, number_agents

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        currentStep = 0

        print(request.form)
        trafficModel = RandomModel(number_agents)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global trafficModel
    
    if request.method == 'GET':
        carPositions = []
        for i in trafficModel.schedule.agents:
            carPositions.append({"id": str(i.unique_id), "x": i.pos[0], "y": 0, "z": i.pos[1]})
        return jsonify({'positions':carPositions})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, trafficModel
    if request.method == 'GET':
        trafficModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)