"""Ranking de bairros pelo volume de denúncias registradas."""

from models.denuncias import formatar_bairro
from utils.validacoes import normalizar_texto


def criterio_ordenacao(resumo: dict) -> tuple:
    """Define a ordem do ranking e o desempate alfabético.

    Parâmetros: resumo, dicionário com bairro e total de denúncias.
    Retorno: tupla com total negativo e nome normalizado do bairro.
    """
    return -resumo["total"], normalizar_texto(resumo["bairro"])


def gerar_ranking(denuncias: list[dict]) -> list[dict]:
    """Agrupa os bairros e conta as denúncias de cada situação.

    Parâmetros: denuncias, lista de dicionários com os registros atuais.
    Retorno: nova lista ordenada por total decrescente e nome alfabético.
        Inclui denúncias resolvidas e não modifica os registros recebidos.
    """
    # O set reúne cada bairro uma única vez, ignorando acentos e caixa.
    bairros = set()
    for denuncia in denuncias:
        bairros.add(normalizar_texto(denuncia["bairro"]))

    ranking = []
    for bairro in bairros:
        resumo = {
            "bairro": "", "total": 0, "abertas": 0,
            "em_andamento": 0, "resolvidas": 0,
        }
        for denuncia in denuncias:
            if normalizar_texto(denuncia["bairro"]) != bairro:
                continue
            if resumo["bairro"] == "":
                resumo["bairro"] = formatar_bairro(denuncia["bairro"])
            resumo["total"] += 1
            if denuncia["situacao"] == "Aberta":
                resumo["abertas"] += 1
            elif denuncia["situacao"] == "Em andamento":
                resumo["em_andamento"] += 1
            else:
                resumo["resolvidas"] += 1
        ranking.append(resumo)
    return sorted(ranking, key=criterio_ordenacao)


def resumir_ranking(ranking: list[dict]) -> dict:
    """Soma os totais de todos os bairros do ranking.

    Parâmetros: ranking, lista retornada por gerar_ranking.
    Retorno: dicionário com total de denúncias, bairros e contagens por situação.
        Retorna contagens zeradas para uma lista vazia e não altera a lista.
    """
    resumo = {
        "total": 0, "bairros": len(ranking), "abertas": 0,
        "em_andamento": 0, "resolvidas": 0,
    }
    for bairro in ranking:
        resumo["total"] += bairro["total"]
        resumo["abertas"] += bairro["abertas"]
        resumo["em_andamento"] += bairro["em_andamento"]
        resumo["resolvidas"] += bairro["resolvidas"]
    return resumo
