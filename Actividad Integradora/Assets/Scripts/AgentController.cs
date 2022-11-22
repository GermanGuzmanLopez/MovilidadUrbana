// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;

    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]

public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getObstaclesEndpoint = "/getObstacles";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData, obstacleData;
    Dictionary<string, GameObject> agents;
    Dictionary<string, GameObject> boxes;

    Dictionary<string, Vector3> prevPositionsAgents, currPositionsAgents, prevPositionsBoxes, currPositionsBoxes;

    bool updatedAgent = false, startedAgent = false, updatedBox = false, startedBox = false;

    public GameObject agentPrefab, obstaclePrefab, floor;
    public int NAgents, KCajas, width, height;
    public float timeToUpdate;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        obstacleData = new AgentsData();

        prevPositionsAgents = new Dictionary<string, Vector3>();
        currPositionsAgents = new Dictionary<string, Vector3>();
        prevPositionsBoxes = new Dictionary<string, Vector3>();
        currPositionsBoxes = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        boxes = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updatedAgent = false;
            updatedBox = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updatedAgent & updatedBox)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositionsAgents)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositionsAgents[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero)
                {
                    agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);

                    //agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
                }
                   
            }
            foreach (var box in currPositionsBoxes)
            {
                Vector3 currentPosition = box.Value;
                Vector3 previousPosition = prevPositionsBoxes[box.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                boxes[box.Key].transform.localPosition = interpolated;
                if (direction != Vector3.zero) boxes[box.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetObstacleData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("KCajas", KCajas.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetObstacleData());
            StartCoroutine(GetAgentsData());
        }
    }

    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach (AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);

                    if(!startedAgent)
                    {
                        prevPositionsAgents[agent.id] = newAgentPosition;
                        agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositionsAgents.TryGetValue(agent.id, out currentPosition))
                            prevPositionsAgents[agent.id] = currentPosition;
                        currPositionsAgents[agent.id] = newAgentPosition;
                    }
            }

            updatedAgent = true;
            if(!startedAgent) startedAgent = true;
        }
    }

    IEnumerator GetObstacleData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);
            /*Debug.Log(obstacleData.positions);*/

            foreach(AgentData obstacle in obstacleData.positions)
            {
                Vector3 newAgentPosition = new Vector3(obstacle.x, obstacle.y, obstacle.z);

                if (!startedBox)
                {
                    prevPositionsBoxes[obstacle.id] = newAgentPosition;
                    boxes[obstacle.id] = Instantiate(obstaclePrefab, newAgentPosition, Quaternion.identity);
                }
                else
                {
                    Vector3 currentPosition = new Vector3();
                    if (currPositionsBoxes.TryGetValue(obstacle.id, out currentPosition))
                        prevPositionsBoxes[obstacle.id] = currentPosition;
                    currPositionsBoxes[obstacle.id] = newAgentPosition;
                }
            }
            updatedBox = true;
            if (!startedBox) startedBox = true;
        }
    }
}
