using System.Collections;
using UnityEngine;

public class GripSpawner : MonoBehaviour
{
    [Header("Spawn settings")]
    public GameObject[] objects;
    public Transform objectParent;
    public float spawnIntervalMin = 3f;
    public float spawnIntervalMax = 5f;
    public float objectSpeed = 8f;

    private void Start()
    {
        StartCoroutine(SpawnObjectLoop());
    }

    private IEnumerator SpawnObjectLoop()
    {
        while (true)
        {
            // Espera um tempo aleatório definido pelo usuário dentro da Unity
            float spawnDelay = Random.Range(spawnIntervalMin, spawnIntervalMax);

            SpawnCenteredObject();

            yield return new WaitForSeconds(spawnDelay);
        }
    }

    private void SpawnCenteredObject()
    {
        if (objects.Length == 0) return;

        // Escolhe um objeto aleatório do array
        int randomIndex = Random.Range(0, objects.Length);
        GameObject selectedObject = objects[randomIndex];

        // Instancia o objeto na posição do spawner
        GameObject gameObject = Instantiate(selectedObject, transform.position, Quaternion.identity, objectParent);
        gameObject.transform.position = new Vector3(transform.position.x, transform.position.y, transform.position.z);

        // Adiciona o script de movimento, se houver
        GripMove gripMove = gameObject.AddComponent<GripMove>();
        gripMove.Initialize(objectSpeed);
    }
}
