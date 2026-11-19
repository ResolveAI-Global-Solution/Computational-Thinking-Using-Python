"""Categorias, situações e estrutura de uma denúncia urbana."""

from utils.validacoes import normalizar_texto

CATEGORIAS = (
    "Buraco na via",
    "Iluminação pública",
    "Descarte irregular de lixo",
    "Calçada danificada",
    "Alagamento",
)
SITUACOES = ("Aberta", "Em andamento", "Resolvida")
BAIRROS = ("Bela Vista", "Centro", "Jardim Paulista", "Suburbano", "Vila Nova")


def formatar_bairro(bairro: str) -> str:
    """Obtém o nome padrão de um bairro para exibição.

    Parâmetros: bairro, texto armazenado na denúncia.
    Retorno: nome de BAIRROS quando houver correspondência; caso contrário,
        o texto original. Não modifica o registro nem o arquivo de dados.
    """
    for nome in BAIRROS:
        if normalizar_texto(nome) == normalizar_texto(bairro):
            return nome
    return bairro


def criar_denuncia(
    identificador: int, categoria: str, bairro: str, endereco: str, descricao: str
) -> dict:
    """Monta uma denúncia com situação inicial Aberta.

    Parâmetros:
        identificador: inteiro positivo que identifica o registro.
        categoria: texto com uma das cinco categorias permitidas.
        bairro: texto com o bairro afetado.
        endereco: texto com endereço ou ponto de referência.
        descricao: texto que explica o problema urbano.
    Retorno: novo dicionário com os dados recebidos; não altera a base.
    """
    return {
        "id": identificador,
        "categoria": categoria,
        "bairro": bairro,
        "endereco": endereco,
        "descricao": descricao,
        "situacao": "Aberta",
    }
