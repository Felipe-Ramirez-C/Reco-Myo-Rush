using UnityEngine;

public class Scroll3D : MonoBehaviour
{
    [SerializeField] private float scrollSpeed = 8f; // Velocidade do movimento
    [SerializeField] private Vector3 direction = Vector3.back; // Direcao padrao (Z negativo)
    [SerializeField] private Space movementSpace = Space.World; // Espaco de movimento (Global ou Local)

    void Update()
    {
        // Move o objeto na direcao definida, considerando o espaco (global/local)
        transform.Translate(direction.normalized * scrollSpeed * Time.deltaTime, movementSpace);

        // Log para verificar se o script esta funcionando
        Debug.Log($"Movendo {gameObject.name} na direcao {direction} com velocidade {scrollSpeed}");
    }
}