# ResolveAI - Denúncias Urbanas e Ranking dos Bairros

Projeto de **Computational Thinking Using Python - FIAP**, desenvolvido para a **Global Solution 2026/2 - CitizenTech**. Aplicação de terminal para registrar problemas urbanos, acompanhar sua situação e consultar um ranking dos bairros pelo volume de denúncias cadastradas.

A documentação técnica completa está em [Markdown](docs/Documentacao_ResolveAI.md) e em [PDF](docs/ResolveAI_Documentacao_Global_Solution.pdf).

## Integrantes

| Integrante | RM | Turma |
| --- | --- | --- |
| Andrei Oliveira de Sousa | 573373 | 1TDSPW |
| Felipe Coelho da Fonseca | 572133 | 1TDSPW |
| Henrique Soares Pereira | 569898 | 1TDSPW |
| Luiz Felipe Lourenço da Silva | 572576 | 1TDSPW |

## Problema e objetivo

Problemas como buracos, falta de iluminação e descarte irregular de lixo afetam o uso dos espaços públicos. O ResolveAI organiza esses relatos por bairro e permite acompanhar manualmente sua situação.

Nesta entrega, uma **denúncia urbana é o próprio registro do problema**, com categoria, bairro, endereço, descrição e situação. O programa implementa um recorte local da proposta do grupo, relacionado à zeladoria urbana e ao ODS 11 - Cidades e comunidades sustentáveis.

O resultado esperado é manter registros organizados entre execuções, facilitar consultas e mostrar o volume de relatos e suas situações em cada bairro. O ranking mede os registros deste programa; não mede a qualidade de um bairro ou o desempenho oficial de órgãos públicos.

## Como executar

**Requisito:** Python **3.10 ou superior**, necessário para `match-case` e as anotações de tipos utilizadas. O projeto usa somente bibliotecas padrão; não precisa de `pip`, internet ou servidor de banco de dados.

No terminal, dentro da pasta do projeto:

```console
python main.py
```

No Windows, se o Python Launcher estiver configurado:

```console
py main.py
```

Se esses comandos não estiverem disponíveis, selecione o interpretador instalado no VS Code ou utilize seu caminho completo. Exemplo para o Python 3.14 usado na verificação deste projeto:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" .\main.py
```

Esse último caminho depende da instalação do computador. A criação do PDF utiliza ferramentas de edição de documentos; elas não são dependências da aplicação.

O arquivo `dados/denuncias.json` é criado vazio **somente se estiver ausente**. Quando já existe, os registros são carregados e preservados. O caminho é calculado a partir da pasta do projeto, independentemente da pasta atual do terminal.

## Menus e funcionalidades

```text
=== RESOLVEAI ===
1 - Denúncias
2 - Ranking dos bairros
0 - Sair

=== DENÚNCIAS ===
1 - Cadastrar
2 - Listar
3 - Consultar por ID
4 - Editar
5 - Excluir
6 - Consultar por bairro
0 - Voltar
```

- **Cadastrar:** selecionar categoria e bairro pelo número, informar endereço e descrição. A denúncia recebe um ID e nasce como **Aberta**.
- **Listar:** mostrar ID, bairro, categoria e situação em uma linha por denúncia.
- **Consultar por ID:** exibir todos os campos, incluindo endereço e descrição.
- **Editar:** alterar os campos e a situação. **ENTER mantém o valor atual** de cada campo.
- **Excluir:** mostrar o registro e solicitar **S/N** antes da exclusão definitiva.
- **Consultar por bairro:** selecionar o bairro em uma lista e mostrar seus registros resumidos.
- **Ranking:** mostrar totais gerais e ordenar os bairros pela quantidade de denúncias, com contagens por situação.

Após cada operação, o programa apresenta **“Pressione ENTER para continuar...”**. As opções de voltar e sair retornam diretamente. Nas seleções de categoria, bairro e situação, `0` cancela a operação.

## Campos, opções fixas e regras

| Campo | Regra |
| --- | --- |
| `id` | Inteiro positivo gerado por `proximo_id`; não é editável nem reutilizado após exclusão. |
| `categoria` | Uma das cinco opções fixas. |
| `bairro` | Escolhido na lista fixa pela interface; a validação textual aceita de 2 a 80 caracteres. |
| `endereco` | Texto de 5 a 160 caracteres, após padronizar espaços. |
| `descricao` | Texto de 10 a 500 caracteres, após padronizar espaços. |
| `situacao` | Aberta, Em andamento ou Resolvida. |

**Categorias:** Buraco na via; Iluminação pública; Descarte irregular de lixo; Calçada danificada; Alagamento.

**Bairros:** Bela Vista; Centro; Jardim Paulista; Suburbano; Vila Nova. As opções ficam na constante `BAIRROS`, em `models/denuncias.py`.

A situação é alterada manualmente na edição. O programa permite escolher qualquer uma das três situações; não valida uma sequência obrigatória de transições. Não há campo de data, login ou histórico de alterações.

Consultas e ranking ignoram diferenças de maiúsculas, acentos e espaços repetidos nos nomes dos bairros. Nomes conhecidos são exibidos no padrão da lista: um registro antigo com `suburbano` aparece como **Suburbano**, sem reescrever o arquivo apenas pela consulta. Nomes antigos fora da lista fixa continuam como foram armazenados.

## Regras do ranking

1. Considerar todas as denúncias existentes, inclusive as resolvidas.
2. Agrupar os registros pelo bairro normalizado.
3. Contar total, abertas, em andamento e resolvidas.
4. Ordenar pelo total decrescente; em empate, pelo nome do bairro em ordem alfabética.
5. Exibir um resumo geral antes das posições.

O ranking é recalculado a cada consulta. Edições e exclusões aparecem na próxima visualização. Bairros sem denúncias não entram no ranking.

## Estrutura do projeto

```text
PythonGS/
|-- main.py
|-- models/
|   |-- __init__.py
|   `-- denuncias.py
|-- services/
|   |-- __init__.py
|   |-- denuncias.py
|   `-- ranking.py
|-- utils/
|   |-- __init__.py
|   |-- validacoes.py
|   `-- arquivos.py
|-- dados/
|   `-- denuncias.json
|-- docs/
|   |-- Documentacao_ResolveAI.md
|   `-- ResolveAI_Documentacao_Global_Solution.pdf
|-- identificacao.txt
`-- README.md
```

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Menus, leitura das entradas, exibição resumida/detalhada, confirmação e coordenação do salvamento. |
| `models/denuncias.py` | Tuplas de opções, estrutura de uma denúncia e formatação do nome do bairro. |
| `services/denuncias.py` | Buscar, filtrar por bairro, validar campos, cadastrar, editar e excluir. |
| `services/ranking.py` | Agrupar bairros, contar situações, ordenar o ranking e somar o resumo geral. |
| `utils/validacoes.py` | Validar e ler textos/números, normalizar nomes, escolher opções, confirmar e pausar. |
| `utils/arquivos.py` | Validar a base, carregar e salvar o JSON. |

## Persistência e organização das funções

O JSON contém `proximo_id` e uma lista `denuncias`. Exemplo **fictício**:

```json
{
    "proximo_id": 2,
    "denuncias": [
        {
            "id": 1,
            "categoria": "Buraco na via",
            "bairro": "Centro",
            "endereco": "Rua Exemplo, 10",
            "descricao": "Buraco aberto perto da esquina.",
            "situacao": "Aberta"
        }
    ]
}
```

Cada cadastro, edição ou exclusão trabalha sobre uma cópia da base. A cópia é validada e salva antes de substituir os dados em memória. A gravação usa um arquivo `.tmp` e `os.replace()`, reduzindo o risco de deixar um JSON incompleto. Se ocorrer uma falha de gravação, a alteração não é aplicada à base em memória e não é anunciada como sucesso.

Se o JSON estiver inválido, o programa informa o erro e preserva o arquivo. Confira seu conteúdo ou restaure uma cópia válida antes de executar novamente. Os dados não são reiniciados automaticamente.

As funções seguem programação procedural, com parâmetros e retornos anotados e docstrings. Por exemplo, `buscar_denuncia(dados: dict, identificador: int) -> dict | None` recebe a base e o ID, retornando o registro ou `None`. Funções de alteração retornam uma tupla `(sucesso, mensagem)`; ranking e filtros retornam listas. As anotações documentam os tipos; as validações são feitas explicitamente pelo código.

## Relação com os requisitos de Python

| Critério | Evidência na implementação |
| --- | --- |
| Menus e submenus - 5 pontos | `main()` e `menu_denuncias()`. |
| Entrada/saída - 4 pontos | `input()`, variáveis, conversão numérica e f-strings. |
| Decisões - 6 pontos | `match-case` nos menus; `if-elif-else` nas validações e na contagem de situações. |
| Repetições - 6 pontos | `while` nos menus e leituras; `for` nas listagens, filtros e ranking. |
| Estruturas de dados - 8 pontos | Listas, tuplas, strings, dicionários e sets usados nos fluxos do programa. |
| Funções - 6 pontos | Funções com parâmetros, retornos utilizados e docstrings. |
| Persistência - 4 pontos | Leitura e gravação permanente em JSON. |
| Usabilidade - 6 pontos | Seleções numeradas, mensagens, ENTER, cancelamento e confirmação S/N. |
| Organização/comentários - 5 pontos | Módulos separados, nomes em português, comentários e docstrings. |

O código da aplicação não declara classes e não utiliza list comprehension. A tabela relaciona a implementação aos critérios dos **50 pontos de código**; a nota depende da avaliação do professor.

## Como conferir

Em uma cópia de teste do projeto, cadastre denúncias em dois bairros. Anote os IDs retornados e confira:

1. Listar e consultar por ID mostram, respectivamente, resumo e detalhes.
2. A consulta por bairro apresenta somente os registros daquele bairro.
3. A edição permite manter campos com ENTER e mudar a situação.
4. O ranking inclui todas as situações e desempata alfabeticamente.
5. Recusar uma exclusão mantém o registro; confirmar remove e atualiza o ranking.
6. Fechar e abrir preserva os dados e o próximo ID.
7. Entradas inválidas, listas vazias e IDs inexistentes produzem mensagens claras.

Foram verificadas essas operações e a preservação da base em falha simulada de gravação, usando dados fictícios e armazenamento temporário. O PDF apresenta o roteiro e os resultados. Os testes de documentação não alteraram os registros reais.

## Escopo e uso de IA

O protótipo funciona localmente, em uma execução por vez. Não envia solicitações à prefeitura, não comprova a solução de um problema e não possui mapas, fotos, GPS, previsão por IA ou integração com APIs. A mudança de situação é um registro manual do usuário.

O projeto e a documentação tiveram apoio de **ChatGPT/Codex** na discussão do escopo, implementação, revisão e verificações.

## Arquivos para entrega

O enunciado de Python prevê um ZIP com código-fonte e documentação PDF; o arquivo `identificacao.txt` deve acompanhar a entrega com nome, RM e turma de cada integrante. Inclua os módulos completos e a pasta de dados quando desejar preservar a base existente. A aplicação cria o JSON se ele estiver ausente.

A pasta `backups/`, quando presente no ambiente de desenvolvimento, guarda versões anteriores e não faz parte da versão atual da aplicação.

## Referências

- FIAP. *1TDS Fevereiro - Global Solution 2026-2*, seção Computational Thinking Using Python, páginas 39 a 44.
- Leituras de apoio: [JSON](https://docs.python.org/3/library/json.html), [controle de fluxo](https://docs.python.org/3/tutorial/controlflow.html), [estruturas de dados](https://docs.python.org/3/tutorial/datastructures.html) e [cópia de objetos](https://docs.python.org/3/library/copy.html), na documentação oficial do Python.
