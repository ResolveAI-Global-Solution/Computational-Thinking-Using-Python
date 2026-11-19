"""Persistência das denúncias em JSON, sem dependências externas."""

import json
import os

from models.denuncias import CATEGORIAS, SITUACOES
from utils.validacoes import validar_texto

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DADOS = os.path.join(PASTA_PROJETO, "dados", "denuncias.json")


def validar_base(dados: dict) -> None:
    """Verifica a estrutura da base antes de usar ou gravar os dados.

    Parâmetros: dados, dicionário com proximo_id e uma lista de denuncias.
    Retorno: None; lança ValueError se houver conteúdo inválido.
        Não modifica a base recebida.
    """
    if not isinstance(dados, dict):
        raise ValueError("A base precisa ser um dicionário.")
    proximo_id = dados.get("proximo_id")
    if type(proximo_id) is not int or proximo_id < 1:
        raise ValueError("O próximo ID precisa ser um inteiro positivo.")
    if not isinstance(dados.get("denuncias"), list):
        raise ValueError("O campo denuncias precisa ser uma lista.")
    ids = set()
    for denuncia in dados["denuncias"]:
        if not isinstance(denuncia, dict):
            raise ValueError("Cada denúncia precisa ser um dicionário.")
        identificador = denuncia.get("id")
        if type(identificador) is not int or not 1 <= identificador < proximo_id:
            raise ValueError("ID inválido ou próximo ID já utilizado.")
        if identificador in ids:
            raise ValueError("Existem denúncias com IDs repetidos.")
        ids.add(identificador)
        if denuncia.get("categoria") not in CATEGORIAS:
            raise ValueError(f"Categoria inválida na denúncia #{identificador}.")
        if denuncia.get("situacao") not in SITUACOES:
            raise ValueError(f"Situação inválida na denúncia #{identificador}.")
        campos = (("bairro", 2, 80), ("endereco", 5, 160), ("descricao", 10, 500))
        for campo, minimo, maximo in campos:
            valido, mensagem = validar_texto(denuncia.get(campo), campo, minimo, maximo)
            if not valido:
                raise ValueError(f"Denúncia #{identificador}: {mensagem}")


def carregar_dados(caminho: str = CAMINHO_DADOS) -> dict:
    """Carrega a base ou cria uma vazia se o arquivo ainda não existir.

    Parâmetros: caminho, texto com o local do JSON; usa dados/denuncias.json.
    Retorno: dicionário validado com os registros e o próximo ID.
    Efeitos: cria o arquivo apenas se ausente; erros de conteúdo ou acesso
        são propagados sem substituir um arquivo existente.
    """
    if not os.path.exists(caminho):
        dados = {"proximo_id": 1, "denuncias": []}
        salvar_dados(dados, caminho)
        return dados
    try:
        with open(caminho, "r", encoding="utf-8-sig") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, UnicodeError) as erro:
        raise ValueError("O arquivo JSON está inválido e foi preservado.") from erro
    validar_base(dados)
    return dados


def salvar_dados(dados: dict, caminho: str = CAMINHO_DADOS) -> None:
    """Grava uma base validada antes de substituir o arquivo anterior.

    Parâmetros:
        dados: dicionário completo a gravar.
        caminho: texto com o local do JSON; usa dados/denuncias.json.
    Retorno: None; lança ValueError para dados inválidos ou OSError no acesso.
    Efeitos: cria a pasta necessária e substitui o JSON após gravar o temporário.
        Não modifica o dicionário recebido.
    """
    validar_base(dados)
    caminho = os.path.abspath(caminho)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    temporario = f"{caminho}.tmp"
    try:
        with open(temporario, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            arquivo.write("\n")
        os.replace(temporario, caminho)
    finally:
        if os.path.exists(temporario):
            os.remove(temporario)
