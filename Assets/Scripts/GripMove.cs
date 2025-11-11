using UnityEngine;

public class GripMove : MonoBehaviour
{
    private float speed;

    public void Initialize(float moveSpeed)
    {
        speed = moveSpeed;
    }

    void Update()
    {
        // Move o obstaculo na direcao do jogador (eixo Z negativo)
        transform.Translate(Vector3.back * speed * Time.deltaTime);

        // Destroi o obstaculo ao sair do campo de visao
        if (transform.position.z < -720f)
        {
            Destroy(gameObject);
        }
    }
}
