"""Regras do cadastro, consulta, edição e exclusão de denúncias."""

from models.denuncias import CATEGORIAS, SITUACOES, criar_denuncia
from utils.validacoes import limpar_texto, normalizar_texto, validar_texto


def buscar_denuncia(dados: dict, identificador: int) -> dict | None:
    """Procura uma denúncia pelo ID.

    Parâmetros: dados, dicionário da base; identificador, inteiro positivo.
    Retorno: dicionário encontrado ou None; não modifica a base.
    """
    if type(identificador) is not int or identificador < 1:
        return None
    for denuncia in dados["denuncias"]:
        if denuncia["id"] == identificador:
            return denuncia
    return None


def consultar_por_bairro(dados: dict, bairro: str) -> list[dict]:
    """Seleciona as denúncias de um bairro, sem alterar a base.

    Parâmetros:
        dados: dicionário com a lista de denúncias cadastradas.
        bairro: texto com o bairro escolhido no menu.
    Retorno: nova lista dos registros encontrados; vazia se não houver dados.
        A comparação ignora diferenças de acentos, espaços e maiúsculas.
    """
    resultado = []
    bairro = normalizar_texto(bairro)
    for denuncia in dados["denuncias"]:
        if normalizar_texto(denuncia["bairro"]) == bairro:
            resultado.append(denuncia)
    return resultado


def validar_campos(
    categoria: str, bairro: str, endereco: str, descricao: str, situacao: str
) -> tuple[bool, str]:
    """Valida todos os campos antes de modificar uma denúncia.

    Parâmetros:
        categoria: texto de CATEGORIAS.
        bairro: texto entre 2 e 80 caracteres.
        endereco: texto entre 5 e 160 caracteres.
        descricao: texto entre 10 e 500 caracteres.
        situacao: texto de SITUACOES.
    Retorno: tupla (válido, mensagem de erro); não modifica os argumentos.
    """
    if categoria not in CATEGORIAS or situacao not in SITUACOES:
        return False, "Escolha uma categoria e uma situação disponíveis."
    campos = (
        (bairro, "bairro", 2, 80),
        (endereco, "endereço", 5, 160),
        (descricao, "descrição", 10, 500),
    )
    for texto, nome, minimo, maximo in campos:
        valido, mensagem = validar_texto(texto, nome, minimo, maximo)
        if not valido:
            return False, mensagem
    return True, ""


def cadastrar_denuncia(
    dados: dict, categoria: str, bairro: str, endereco: str, descricao: str
) -> tuple[bool, str]:
    """Cadastra uma denúncia aberta depois de validar os campos.

    Parâmetros:
        dados: dicionário da base que receberá o registro.
        categoria: texto com a categoria escolhida.
        bairro: texto com o bairro afetado.
        endereco: texto com endereço ou referência.
        descricao: texto com a explicação do problema.
    Retorno: tupla (sucesso, mensagem).
    Efeitos: no sucesso, acrescenta o registro e incrementa proximo_id.
    """
    valido, mensagem = validar_campos(categoria, bairro, endereco, descricao, "Aberta")
    if not valido:
        return False, mensagem
    identificador = dados["proximo_id"]
    denuncia = criar_denuncia(
        identificador, categoria, limpar_texto(bairro),
        limpar_texto(endereco), limpar_texto(descricao),
    )
    dados["denuncias"].append(denuncia)
    dados["proximo_id"] += 1
    return True, f"Denúncia #{identificador} cadastrada com situação Aberta."


def editar_denuncia(
    dados: dict, identificador: int, categoria: str, bairro: str,
    endereco: str, descricao: str, situacao: str
) -> tuple[bool, str]:
    """Atualiza os campos de uma denúncia existente.

    Parâmetros:
        dados: dicionário da base que será alterada.
        identificador: inteiro positivo do registro.
        categoria: novo texto com a categoria.
        bairro: novo texto com o bairro.
        endereco: novo texto com endereço ou referência.
        descricao: novo texto com a descrição.
        situacao: Aberta, Em andamento ou Resolvida.
    Retorno: tupla (sucesso, mensagem).
    Efeitos: altera o registro apenas se todos os campos forem válidos.
    """
    denuncia = buscar_denuncia(dados, identificador)
    if denuncia is None:
        return False, f"Denúncia #{identificador} não encontrada."
    valido, mensagem = validar_campos(categoria, bairro, endereco, descricao, situacao)
    if not valido:
        return False, mensagem
    novos_campos = {
        "categoria": categoria,
        "bairro": limpar_texto(bairro),
        "endereco": limpar_texto(endereco),
        "descricao": limpar_texto(descricao),
        "situacao": situacao,
    }
    alterou = False
    for campo, valor in novos_campos.items():
        if denuncia[campo] != valor:
            alterou = True
    if not alterou:
        return False, "Nenhum campo foi alterado."
    denuncia.update(novos_campos)
    return True, f"Denúncia #{identificador} atualizada."


def excluir_denuncia(dados: dict, identificador: int) -> tuple[bool, str]:
    """Remove definitivamente uma denúncia da lista.

    Parâmetros: dados, dicionário da base; identificador, inteiro do registro.
    Retorno: tupla (sucesso, mensagem).
    Efeitos: remove o registro encontrado sem reduzir proximo_id.
    """
    denuncia = buscar_denuncia(dados, identificador)
    if denuncia is None:
        return False, f"Denúncia #{identificador} não encontrada."
    dados["denuncias"].remove(denuncia)
    return True, f"Denúncia #{identificador} excluída."
