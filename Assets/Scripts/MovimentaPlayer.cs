using UnityEngine;

public class MovimentaPlayer : MonoBehaviour
{
    public float velocidadeDoJogador;
    public Rigidbody body;
    private float movimentoX;

    private float minYPosition = -2f;
    private bool isGameOver = false;

    /*
    void Update()
    {
        if (!isGameOver)
        {
            MovimentarBola();

            if (body.transform.position.y < minYPosition)
            {
                EndGame();
            }
        }
    }

    private void MovimentarBola()
    {
        movimentoX = 0f;

        // Verifica se o broker foi inicializado
        if (MqttBrokerBehaviour.instance != null)
        {
            int estado = MqttBrokerBehaviour.instance.HandState;

            if (estado == -1)
                movimentoX = -1f;
            else if (estado == 1)
                movimentoX = 1f;
            else
                movimentoX = 0f;
        }

        body.AddForce(new Vector3(movimentoX * velocidadeDoJogador, 0f, 0f), ForceMode.VelocityChange);
        StabilizeZ();
    }*/

    private void StabilizeZ()
    {
        Vector3 velocity = body.linearVelocity;
        velocity.z = Mathf.Lerp(velocity.z, 0f, Time.deltaTime * 5f);
        body.linearVelocity = velocity;
    }

    private void EndGame()
    {
        if (!isGameOver)
        {
            isGameOver = true;
            FindObjectOfType<GameManager>().GameOver();
        }
    }
}
