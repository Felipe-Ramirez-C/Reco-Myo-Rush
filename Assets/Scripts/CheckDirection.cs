using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckDirection : MonoBehaviour
{
    public enum Direcao
    {
        Neutro,
        Direita,
        Esquerda
    }

    [Header("Flags de Direção (apenas leitura)")]
    [SerializeField] private bool isNeutro = true;
    [SerializeField] private bool isDireita = false;
    [SerializeField] private bool isEsquerda = false;

    private Direcao ultimaDirecao = Direcao.Neutro;

    /*void Update()
    {
        if (Leitor.Instance == null) return;

        bool? direcaoAtual = Leitor.Instance.move;

        Direcao novaDirecao = Direcao.Neutro;
        if (direcaoAtual == true)
        {
            novaDirecao = Direcao.Direita;
        }
        else if (direcaoAtual == false)
        {
            novaDirecao = Direcao.Esquerda;
        }
        else {
            novaDirecao = Direcao.Neutro;
        }

        if (novaDirecao != ultimaDirecao)
        {
            ultimaDirecao = novaDirecao;
            AtualizarCheckboxes();
        }
    }*/

    private void AtualizarCheckboxes()
    {
        isNeutro = ultimaDirecao == Direcao.Neutro;
        isDireita = ultimaDirecao == Direcao.Direita;
        isEsquerda = ultimaDirecao == Direcao.Esquerda;
    }
}
