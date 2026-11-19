"""ResolveAI: denúncias urbanas e ranking de bairros para CitizenTech.

Execute com Python 3.10 ou superior: python main.py
Usa somente a biblioteca padrão e salva os dados em dados/denuncias.json.
"""

import sys
from copy import deepcopy

from models.denuncias import BAIRROS, CATEGORIAS, SITUACOES, formatar_bairro
from services.denuncias import (
    buscar_denuncia, cadastrar_denuncia, consultar_por_bairro,
    editar_denuncia, excluir_denuncia,
)
from services.ranking import gerar_ranking, resumir_ranking
from utils.arquivos import CAMINHO_DADOS, carregar_dados, salvar_dados
from utils.validacoes import (
    confirmar, escolher_opcao, ler_inteiro, ler_texto, pausar,
)


def mostrar_denuncia(denuncia: dict) -> None:
    """Apresenta todos os campos de uma denúncia.

    Parâmetros: denuncia, dicionário com o registro a mostrar.
    Retorno: None; escreve no terminal sem modificar o registro.
    """
    print(f"\nID: {denuncia['id']} | Situação: {denuncia['situacao']}")
    print(f"Categoria: {denuncia['categoria']}")
    print(f"Bairro: {formatar_bairro(denuncia['bairro'])}")
    print(f"Endereço: {denuncia['endereco']}")
    print(f"Descrição: {denuncia['descricao']}")


def mostrar_resumo_denuncia(denuncia: dict) -> None:
    """Apresenta uma linha curta para facilitar a leitura das listagens.

    Parâmetros: denuncia, dicionário com o registro a mostrar.
    Retorno: None; escreve ID, bairro, categoria e situação sem alterar dados.
    """
    print(
        f"ID: {denuncia['id']} | {formatar_bairro(denuncia['bairro'])} "
        f"| {denuncia['categoria']} | {denuncia['situacao']}"
    )


def tela_cadastrar(dados: dict) -> tuple[bool, str]:
    """Recebe os campos de uma nova denúncia urbana.

    Parâmetros: dados, cópia da base que receberá o cadastro.
    Retorno: tupla (sucesso, mensagem); lê o terminal e altera a cópia no sucesso.
    """
    categoria = escolher_opcao("Categoria do problema", CATEGORIAS)
    if categoria is None:
        return False, "Cadastro cancelado."
    bairro = escolher_opcao("Bairro", BAIRROS)
    if bairro is None:
        return False, "Cadastro cancelado."
    endereco = ler_texto("Endereço ou referência: ", 5, 160)
    descricao = ler_texto("Descreva o problema: ", 10, 500)
    return cadastrar_denuncia(dados, categoria, bairro, endereco, descricao)


def tela_listar(dados: dict) -> None:
    """Lista todas as denúncias atuais em formato resumido.

    Parâmetros: dados, dicionário da base carregada.
    Retorno: None; escreve no terminal sem alterar os dados.
    """
    if not dados["denuncias"]:
        print("Nenhuma denúncia cadastrada.")
        return
    print(f"\nDenúncias cadastradas: {len(dados['denuncias'])}")
    for denuncia in dados["denuncias"]:
        mostrar_resumo_denuncia(denuncia)
    print("\nUse Consultar por ID para ver endereço e descrição.")


def tela_consultar(dados: dict) -> None:
    """Consulta e apresenta uma denúncia pelo ID.

    Parâmetros: dados, dicionário da base carregada.
    Retorno: None; recebe o ID pelo terminal, sem modificar a base.
    """
    identificador = ler_inteiro("ID da denúncia: ", minimo=1)
    denuncia = buscar_denuncia(dados, identificador)
    if denuncia is None:
        print(f"Denúncia #{identificador} não encontrada.")
    else:
        mostrar_denuncia(denuncia)


def tela_consultar_bairro(dados: dict) -> None:
    """Permite escolher um bairro e apresenta suas denúncias resumidas.

    Parâmetros: dados, dicionário da base carregada.
    Retorno: None; lê e escreve no terminal sem modificar a base.
    """
    bairro = escolher_opcao("Bairro para consultar", BAIRROS)
    if bairro is None:
        print("Consulta cancelada.")
        return
    denuncias = consultar_por_bairro(dados, bairro)
    if not denuncias:
        print(f"Nenhuma denúncia cadastrada em {bairro}.")
        return
    print(f"\nDenúncias em {bairro}: {len(denuncias)}")
    for denuncia in denuncias:
        mostrar_resumo_denuncia(denuncia)
    print("\nUse Consultar por ID para ver endereço e descrição.")


def tela_editar(dados: dict) -> tuple[bool, str]:
    """Recebe alterações de campos e situação de uma denúncia.

    Parâmetros: dados, cópia da base que receberá a edição.
    Retorno: tupla (sucesso, mensagem); lê o terminal e altera a cópia no sucesso.
    """
    identificador = ler_inteiro("ID da denúncia para editar: ", minimo=1)
    denuncia = buscar_denuncia(dados, identificador)
    if denuncia is None:
        return False, f"Denúncia #{identificador} não encontrada."
    mostrar_denuncia(denuncia)
    print("\nENTER mantém o valor atual de cada campo.")
    categoria = escolher_opcao("Categoria", CATEGORIAS, denuncia["categoria"])
    if categoria is None:
        return False, "Edição cancelada."
    bairro = escolher_opcao("Bairro", BAIRROS, denuncia["bairro"])
    if bairro is None:
        return False, "Edição cancelada."
    endereco = ler_texto(
        f"Endereço [{denuncia['endereco']}]: ", 5, 160, denuncia["endereco"]
    )
    descricao = ler_texto(
        f"Descrição [{denuncia['descricao']}]: ", 10, 500, denuncia["descricao"]
    )
    situacao = escolher_opcao("Situação", SITUACOES, denuncia["situacao"])
    if situacao is None:
        return False, "Edição cancelada."
    return editar_denuncia(
        dados, identificador, categoria, bairro, endereco, descricao, situacao
    )


def tela_excluir(dados: dict) -> tuple[bool, str]:
    """Mostra a denúncia e solicita confirmação antes de excluí-la.

    Parâmetros: dados, cópia da base que receberá a exclusão.
    Retorno: tupla (sucesso, mensagem); remove da cópia apenas após S.
    """
    identificador = ler_inteiro("ID da denúncia para excluir: ", minimo=1)
    denuncia = buscar_denuncia(dados, identificador)
    if denuncia is None:
        return False, f"Denúncia #{identificador} não encontrada."
    mostrar_denuncia(denuncia)
    if not confirmar("Excluir esta denúncia definitivamente?"):
        return False, "Exclusão cancelada."
    return excluir_denuncia(dados, identificador)


def mostrar_ranking(dados: dict) -> None:
    """Exibe totais gerais e os bairros por volume de denúncias e situação.

    Parâmetros: dados, dicionário da base carregada.
    Retorno: None; escreve o ranking sem modificar os dados.
    """
    ranking = gerar_ranking(dados["denuncias"])
    if not ranking:
        print("Nenhuma denúncia cadastrada para gerar o ranking.")
        return
    print("\n=== RANKING DOS BAIRROS ===")
    print("Total de relatos cadastrados, incluindo os resolvidos.")
    resumo = resumir_ranking(ranking)
    rotulo_denuncias = "denúncia" if resumo["total"] == 1 else "denúncias"
    rotulo_bairros = "bairro" if resumo["bairros"] == 1 else "bairros"
    print(
        f"\nTotal: {resumo['total']} {rotulo_denuncias} "
        f"em {resumo['bairros']} {rotulo_bairros}"
    )
    print(
        f"Abertas: {resumo['abertas']} | Em andamento: {resumo['em_andamento']} "
        f"| Resolvidas: {resumo['resolvidas']}"
    )
    for posicao, bairro in enumerate(ranking, start=1):
        print(f"\n{posicao} - {bairro['bairro']} | Total: {bairro['total']}")
        print(
            f"Abertas: {bairro['abertas']} | Em andamento: {bairro['em_andamento']} "
            f"| Resolvidas: {bairro['resolvidas']}"
        )


def menu_denuncias(dados: dict) -> None:
    """Controla o submenu CRUD e salva as alterações válidas.

    Parâmetros: dados, dicionário da base usado durante a execução.
    Retorno: None; volta ao menu principal ao escolher 0.
    Efeitos: lê o terminal, salva alterações e atualiza dados após a gravação.
    """
    opcoes = (
        "1 - Cadastrar", "2 - Listar", "3 - Consultar por ID",
        "4 - Editar", "5 - Excluir", "6 - Consultar por bairro", "0 - Voltar",
    )
    while True:
        print("\n=== DENÚNCIAS ===")
        for opcao in opcoes:
            print(opcao)
        escolha = ler_inteiro("Escolha uma opção: ", 0, 6)
        # Só aplicamos a cópia na base original depois de salvar com sucesso.
        copia = deepcopy(dados)
        sucesso = False
        mensagem = ""
        match escolha:
            case 1:
                sucesso, mensagem = tela_cadastrar(copia)
            case 2:
                tela_listar(dados)
            case 3:
                tela_consultar(dados)
            case 4:
                sucesso, mensagem = tela_editar(copia)
            case 5:
                sucesso, mensagem = tela_excluir(copia)
            case 6:
                tela_consultar_bairro(dados)
            case 0:
                return
        if sucesso:
            try:
                salvar_dados(copia)
            except (OSError, ValueError) as erro:
                mensagem = f"Não foi possível salvar: {erro}. A alteração não foi aplicada."
            else:
                dados.clear()
                dados.update(copia)
        if mensagem:
            print(f"{mensagem}")
        pausar()


def main() -> int:
    """Carrega os dados e controla o menu principal do ResolveAI.

    Parâmetros: nenhum.
    Retorno: inteiro 0 no encerramento normal ou 1 se a base não abrir.
    Efeitos: lê/cria o JSON e executa os menus. Arquivo inválido é preservado.
    """
    try:
        dados = carregar_dados()
    except (OSError, ValueError) as erro:
        print(f"Não foi possível abrir os dados: {erro}")
        print(f"Arquivo: {CAMINHO_DADOS}")
        return 1
    opcoes = ("1 - Denúncias", "2 - Ranking dos bairros", "0 - Sair")
    try:
        while True:
            print("\n=== RESOLVEAI ===")
            for opcao in opcoes:
                print(opcao)
            escolha = ler_inteiro("Escolha uma opção: ", 0, 2)
            match escolha:
                case 1:
                    menu_denuncias(dados)
                case 2:
                    mostrar_ranking(dados)
                    pausar()
                case 0:
                    print("Encerrando o ResolveAI...")
                    return 0
    except (EOFError, KeyboardInterrupt):
        print("\nExecução encerrada. As alterações já confirmadas estão salvas.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
