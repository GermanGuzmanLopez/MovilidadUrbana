using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
    public List<GameObject> buildingPrefabs;
    public List<GameObject> parkPrefabs;
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] GameObject fountain;
    [SerializeField] int tileSize;

    private int randomBuilding;
    private int randomPark;
    private int randomAngle;
    private int[] angles = {0, 90,180,270};

    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length -1;
        Debug.Log(y);

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } 
            else if (tiles[i] == 'S') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                // tile = Instantiate(semaphorePrefab, position, Quaternion.identity);
                // tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 's') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                // tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                // tile.transform.parent = transform;
                x += 1;
            } 
            else if (tiles[i] == 'D') {
                randomBuilding=Random.Range(0,buildingPrefabs.Count());
                randomAngle=Random.Range(0,angles.Count());
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefabs[randomBuilding], position, Quaternion.Euler(0,angles[randomAngle], 0));
                tile.GetComponent<Renderer>().materials[0].color = Color.red;
                tile.transform.localScale = new Vector3(.1f, Random.Range(0.1f, 0.15f), .1f);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                randomBuilding=Random.Range(0,buildingPrefabs.Count());
                randomAngle=Random.Range(0,angles.Count());
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefabs[randomBuilding], position, Quaternion.Euler(0,angles[randomAngle], 0));
                tile.transform.localScale = new Vector3(.1f, Random.Range(0.1f, 0.15f), .1f);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'G') {
                randomPark=Random.Range(0,parkPrefabs.Count());
                randomAngle=Random.Range(0,angles.Count());
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(parkPrefabs[randomPark], position, Quaternion.Euler(0,angles[randomAngle], 0));
                tile.transform.parent = transform;
                x += 1;
            }else if (tiles[i] == 'F') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(fountain, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            }else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
