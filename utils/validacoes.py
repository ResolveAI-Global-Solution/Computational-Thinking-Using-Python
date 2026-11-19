"""Validações e leitura de entradas no terminal."""

import unicodedata


def limpar_texto(texto: str) -> str:
    """Padroniza os espaços de um texto.

    Parâmetros: texto, string recebida do usuário.
    Retorno: nova string sem espaços repetidos ou nas extremidades.
    """
    return " ".join(texto.split())


def normalizar_texto(texto: str) -> str:
    """Prepara um texto para comparar bairros sem acentos ou caixa.

    Parâmetros: texto, string a comparar.
    Retorno: nova string com espaços padronizados, sem acentos e em minúsculas.
    """
    resultado = ""
    for caractere in unicodedata.normalize("NFKD", limpar_texto(texto)):
        if not unicodedata.combining(caractere):
            resultado += caractere
    return resultado.casefold()


def validar_texto(
    texto: str, nome: str, minimo: int, maximo: int
) -> tuple[bool, str]:
    """Verifica o tipo e o tamanho de um campo textual.

    Parâmetros:
        texto: valor a validar; deve ser uma string.
        nome: nome do campo usado na mensagem.
        minimo: quantidade mínima de caracteres.
        maximo: quantidade máxima de caracteres.
    Retorno: tupla (válido, mensagem de erro), sem alterar o valor.
    """
    if not isinstance(texto, str):
        return False, f"O campo {nome} deve ser um texto."
    tamanho = len(limpar_texto(texto))
    if tamanho < minimo:
        return False, f"O campo {nome} precisa ter pelo menos {minimo} caracteres."
    elif tamanho > maximo:
        return False, f"O campo {nome} deve ter no máximo {maximo} caracteres."
    else:
        return True, ""


def ler_inteiro(mensagem: str, minimo: int = 0, maximo: int | None = None) -> int:
    """Repete a leitura até receber um inteiro dentro do intervalo.

    Parâmetros:
        mensagem: texto exibido antes da entrada.
        minimo: menor inteiro permitido.
        maximo: maior inteiro permitido, ou None para não limitar.
    Retorno: inteiro válido; lê e escreve no terminal.
    """
    while True:
        try:
            numero = int(input(mensagem).strip())
        except ValueError:
            print("Digite um número inteiro válido.")
            continue
        if numero < minimo:
            print(f"Digite um número maior ou igual a {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"Digite um número menor ou igual a {maximo}.")
        else:
            return numero


def ler_texto(
    mensagem: str, minimo: int, maximo: int, valor_atual: str | None = None
) -> str:
    """Lê um texto válido e permite manter o valor atual na edição.

    Parâmetros:
        mensagem: texto apresentado antes da entrada.
        minimo: quantidade mínima de caracteres.
        maximo: quantidade máxima de caracteres.
        valor_atual: texto mantido com ENTER, ou None para novos campos.
    Retorno: string válida; lê e escreve no terminal.
    """
    while True:
        texto = limpar_texto(input(mensagem))
        if texto == "" and valor_atual is not None:
            return valor_atual
        valido, mensagem_erro = validar_texto(texto, "informado", minimo, maximo)
        if valido:
            return texto
        print(f"{mensagem_erro}")


def escolher_opcao(
    titulo: str, opcoes: tuple, valor_atual: str | None = None
) -> str | None:
    """Mostra opções numeradas, permitindo cancelar ou manter o valor atual.

    Parâmetros:
        titulo: texto que identifica a escolha.
        opcoes: tupla de textos disponíveis.
        valor_atual: opção mantida com ENTER, ou None em novos cadastros.
    Retorno: string escolhida ou None ao digitar 0; usa o terminal.
    """
    print(f"\n{titulo}")
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"{numero} - {opcao}")
    print("0 - Cancelar")
    if valor_atual is not None:
        valor_exibido = valor_atual
        for opcao in opcoes:
            if normalizar_texto(opcao) == normalizar_texto(valor_atual):
                valor_exibido = opcao
                break
        print(f"Atual: {valor_exibido}. ENTER mantém esse valor.")
    while True:
        entrada = input("Escolha: ").strip()
        if entrada == "" and valor_atual is not None:
            return valor_atual
        try:
            numero = int(entrada)
        except ValueError:
            print("Digite o número de uma opção válida.")
            continue
        if numero == 0:
            return None
        if 1 <= numero <= len(opcoes):
            return opcoes[numero - 1]
        print(f"Escolha um número entre 0 e {len(opcoes)}.")


def confirmar(mensagem: str) -> bool:
    """Solicita confirmação antes de uma exclusão.

    Parâmetros: mensagem, texto que explica a ação.
    Retorno: True para S e False para N; repete outras respostas no terminal.
    """
    while True:
        resposta = input(f"{mensagem} [S/N]: ").strip().casefold()
        if resposta == "s":
            return True
        elif resposta == "n":
            return False
        else:
            print("Responda com S para sim ou N para não.")


def pausar() -> None:
    """Aguarda a leitura da mensagem anterior antes de voltar ao menu.

    Parâmetros: nenhum.
    Retorno: None; lê ENTER no terminal.
    """
    input("\nPressione ENTER para continuar...")
