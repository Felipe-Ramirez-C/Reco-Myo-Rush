using System.Collections;
using UnityEngine;

public class CheckCollider : MonoBehaviour
{
    public GripSpawner spawner;        // arraste no inspetor
    public float penaltyTime = 2f;     // tempo de bloqueio do spawn
    public float pushBackForce = 20f;  // velocidade negativa quando erra

    private bool blocked = false;      // evita ativar penalidade 2x

    private void OnTriggerEnter(Collider other)
    {
        string tag = other.tag;

        int planoID = (tag == "Grip1") ? 1 : (tag == "Grip2" ? 2 : 0);
        if (planoID == 0) return;

        Debug.Log("Plano detectado: " + planoID);

        // Verifica contra o valor do Python (via MQTT)
        if (planoID == GripInput.gripAtual)
        {
            Debug.Log("✔ ACERTOU o Grip " + planoID);
        }
        else
        {
            Debug.Log("❌ ERROU! Grip esperado: " + GripInput.gripAtual);

            if (!blocked)
            {
                StartCoroutine(Penalidade());
            }
        }
    }

    IEnumerator Penalidade()
    {
        blocked = true;

        // desativa o spawner
        spawner.StopSpawn();

        // empurra todos que estão no cenário
        foreach (GripMove gm in FindObjectsOfType<GripMove>())
        {
            gm.PushBack(pushBackForce, 0.5f);  // <<< DURAÇÃO ADICIONADA
        }

        yield return new WaitForSeconds(penaltyTime);

        spawner.StartSpawn();
        blocked = false;
    }
}
