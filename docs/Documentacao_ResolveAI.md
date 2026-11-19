# ResolveAI - Documentação Técnica

Global Solution 2026/2 - CitizenTech | Computational Thinking Using Python - FIAP

Turma: 1TDSPW | Documentação revisada em 19/11/2026.

Integrantes: Andrei Oliveira de Sousa (RM 573373), Felipe Coelho da Fonseca (RM 572133), Henrique Soares Pereira (RM 569898) e Luiz Felipe Lourenço da Silva (RM 572576).

## 1. Descrição do Sistema

O ResolveAI organiza relatos de problemas urbanos que afetam a circulação, a segurança e o uso dos espaços públicos. O protótipo Python permite registrar denúncias, consultar seus detalhes, atualizar a situação e visualizar o volume de relatos por bairro.

Nesta aplicação, denúncia urbana é o próprio registro do problema, como buraco na via ou falta de iluminação. O recorte implementa parte da proposta CitizenTech da HalfTech e se relaciona ao ODS 11 - Cidades e comunidades sustentáveis. O resultado esperado é facilitar a organização e o acompanhamento local dos relatos.

## 2. Aderência aos Critérios de Avaliação

| Critério do enunciado | Implementação e evidência |
| --- | --- |
| Menus - 5 pontos | main() apresenta o menu principal; menu_denuncias() controla o submenu com CRUD e consultas. |
| Interação - 4 pontos | input(), variáveis, conversão com int() e saída de dados utilizando f-strings. |
| Decisões - 6 pontos | match-case nos menus; if-elif-else em validar_texto() e na contagem de situações do ranking. |
| Repetições - 6 pontos | while mantém menus e leituras; for percorre opções, denúncias, bairros e resultados. |
| Estruturas de dados - 8 pontos | Listas e dicionários nos registros; tuplas nas opções; strings nos campos; sets nos bairros únicos e na validação de IDs. |
| Funções - 6 pontos | Funções com parâmetros, retornos utilizados, anotações de tipos e docstrings. |
| Persistência - 4 pontos | utils/arquivos.py carrega e grava dados/denuncias.json em UTF-8. |
| Usabilidade - 6 pontos | Opções numeradas, validações, ENTER, cancelamento, confirmação S/N e mensagens para ausência de dados. |
| Organização - 5 pontos | Separação entre main, models, services e utils, com nomes claros e comentários sobre decisões relevantes. |

A tabela relaciona o código aos 50 pontos da rubrica da disciplina, páginas 39 e 40 do enunciado. A avaliação final depende do professor. O código não declara classes e não utiliza list comprehension.

## 3. Funcionalidades e Regras do Produto

### Operações disponíveis

| Operação | Comportamento |
| --- | --- |
| Cadastrar | Escolher categoria e bairro, informar endereço e descrição. Gerar ID único e situação inicial Aberta. |
| Listar | Exibir uma linha por registro com ID, bairro, categoria e situação. |
| Consultar por ID | Localizar uma denúncia e mostrar todos os campos, inclusive endereço e descrição. |
| Editar | Alterar campos e situação. ENTER mantém o valor atual. Uma edição sem mudanças não grava novamente. |
| Excluir | Apresentar o registro e pedir S/N. S remove definitivamente; N cancela. |
| Consultar por bairro | Selecionar um bairro e apresentar somente seus registros, em formato resumido. |
| Ranking dos bairros | Exibir totais gerais e posições por quantidade de denúncias, com contagens de cada situação. |

### Categorias, bairros e situações

Categorias: Buraco na via; Iluminação pública; Descarte irregular de lixo; Calçada danificada; Alagamento.

Bairros na interface: Bela Vista; Centro; Jardim Paulista; Suburbano; Vila Nova. As opções são tuplas em models/denuncias.py.

Situações: Aberta, Em andamento e Resolvida. A alteração é manual e pode escolher qualquer uma das três situações, sem uma sequência obrigatória.

### Interação

Nas seleções de categoria, bairro e situação, a opção 0 cancela. As operações terminam com “Pressione ENTER para continuar...”. Voltar e Sair retornam diretamente. O endereço e a descrição são recebidos como texto e precisam respeitar os limites definidos.

O protótipo é local: não envia pedidos à prefeitura, não valida fotos ou GPS, não comprova resolução de problemas e não oferece previsões por IA. Não há cadastro de usuários, data ou histórico de alterações.

## 4. Estrutura dos Arquivos

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
|-- dados/denuncias.json
|-- docs/Documentacao_ResolveAI.md
|-- docs/ResolveAI_Documentacao_Global_Solution.pdf
|-- identificacao.txt
`-- README.md
```

| Arquivo | Responsabilidade |
| --- | --- |
| main.py | Menus, telas, seleção das opções, confirmação, exibição e coordenação do salvamento. |
| models/denuncias.py | Categorias, bairros e situações; criação do dicionário e nome padrão do bairro para exibição. |
| services/denuncias.py | Buscar por ID, filtrar por bairro, validar campos, cadastrar, editar e excluir. |
| services/ranking.py | Agrupar bairros, contar situações, ordenar as posições e calcular o resumo geral. |
| utils/validacoes.py | Leitura e validação de entradas, tratamento de textos, escolhas, confirmação e pausa. |
| utils/arquivos.py | Validar a base, carregar o JSON e gravar as alterações. |

Os arquivos __init__.py identificam os pacotes. As importações conectam os módulos sem orientação a objetos. A pasta backups/, quando presente no desenvolvimento, guarda versões anteriores e não integra o código da versão atual.

## 5. Persistência JSON e Operações CRUD

A base contém proximo_id e a lista denuncias. O JSON é criado vazio apenas quando não existe. Se já houver um arquivo válido, os registros são preservados. Exemplo fictício:

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

| Dado | Regra |
| --- | --- |
| proximo_id | Inteiro positivo, maior que todos os IDs atuais; incrementado a cada cadastro salvo. |
| id | Inteiro positivo, único, não editável e não reutilizado após uma exclusão. |
| categoria / situacao | Textos que pertencem às respectivas tuplas de opções permitidas. |
| bairro | Texto de 2 a 80 caracteres; na interface, escolhido na lista fixa. |
| endereco | Texto de 5 a 160 caracteres após padronizar espaços. |
| descricao | Texto de 10 a 500 caracteres após padronizar espaços. |

### Como uma alteração é salva

Cadastrar, editar e excluir operam sobre uma cópia feita com deepcopy(). A função salvar_dados() valida essa cópia, grava denuncias.json.tmp e usa os.replace() para substituir o arquivo anterior. Apenas depois do sucesso o menu atualiza a base em memória e apresenta a confirmação.

A exclusão remove o item da lista e mantém proximo_id. O ranking é recalculado a partir dos registros restantes. Uma falha de validação ou gravação não aplica a alteração à base original.

## 6. Fluxogramas do Sistema

### Fluxo principal

Fluxo principal: Início -> carregar/criar e validar JSON -> menu principal -> Denúncias / Ranking / Sair. Denúncias e Ranking retornam ao menu principal.

Denúncias abre o submenu CRUD. Ranking consulta a base atual. Ambos retornam ao menu principal; Sair encerra a execução.

### Fluxo de uma alteração válida

Alteração válida: copiar a base -> ler e validar -> gravar JSON temporário -> substituir o JSON e atualizar a memória -> mostrar resultado e aguardar ENTER. Falhas preservam os dados anteriores.

Entrada inválida é corrigida ou cancelada antes de gravar. Se houver erro de gravação, a cópia não substitui a base em memória e o programa exibe a falha. As operações de consulta apenas leem os registros.

## 7. Ranking dos Bairros

O ranking considera todas as denúncias atuais, inclusive as resolvidas. Um set reúne os nomes dos bairros sem repetição. A normalização ignora caixa, acentos e espaços repetidos; assim, Centro e CENTRO pertencem ao mesmo grupo.

Cada bairro recebe total, abertas, em_andamento e resolvidas. A função criterio_ordenacao() retorna (-total, nome_normalizado): o total negativo produz ordem decrescente e o nome resolve empates alfabeticamente.

### Exemplo fictício usado na verificação

| ID | Bairro | Categoria | Situação |
| --- | --- | --- | --- |
| 1 | Centro | Buraco na via | Aberta |
| 2 | CENTRO | Iluminação pública | Resolvida |
| 3 | Bela Vista | Descarte irregular de lixo | Em andamento |

Saída conferida pelo fluxo de terminal em uma cópia temporária do projeto:

```text
Total: 3 denúncias em 2 bairros
Abertas: 1 | Em andamento: 1 | Resolvidas: 1

1 - Centro | Total: 2
Abertas: 1 | Em andamento: 0 | Resolvidas: 1

2 - Bela Vista | Total: 1
Abertas: 0 | Em andamento: 1 | Resolvidas: 0
```

### Interpretação e atualização

O ranking mostra volume de relatos deste programa. Não representa índice por população, gravidade dos problemas ou desempenho oficial de uma prefeitura. Bairros sem registros não aparecem.

A lista é gerada a cada consulta. Uma edição de bairro ou situação e uma exclusão são refletidas na próxima visualização. formatar_bairro() padroniza nomes conhecidos apenas para exibição; não reescreve os registros antigos por causa de uma consulta.

## 8. Conceitos Aplicados e Principais Funções

| Conceito | Aplicação no código |
| --- | --- |
| Listas e dicionários | denuncias armazena os registros; cada registro e cada resumo de bairro é um dicionário. |
| Tuplas e strings | Categorias, situações, bairros e opções dos menus são tuplas; os campos textuais são strings. |
| Sets | Bairros normalizados sem repetição no ranking e IDs sem duplicação na validação da base. |
| match-case e if-elif-else | Encaminhamento do menu, limites das entradas e contagem das três situações. |
| while, for e enumerate | Navegação, repetição de entradas inválidas, consultas, agrupamento e numeração das posições. |
| Funções e módulos | Separação de responsabilidades; argumentos, retornos, docstrings e anotações de tipos. |
| Arquivos e exceções | JSON em UTF-8, leitura/escrita com with e tratamento de falhas de conteúdo e acesso. |

### Principais contratos de funções

| Função / parâmetros | Retorno e finalidade |
| --- | --- |
| buscar_denuncia(dados, identificador) | dict ou None. Localiza um registro sem modificar a base. |
| consultar_por_bairro(dados, bairro) | list[dict]. Seleciona os registros do bairro normalizado. |
| cadastrar_denuncia / editar_denuncia / excluir_denuncia | tuple[bool, str]. Recebem a base e os campos necessários; retornam sucesso e mensagem. |
| gerar_ranking(denuncias) | list[dict]. Agrupa, conta e ordena os bairros. |
| resumir_ranking(ranking) | dict. Soma totais gerais e informa a quantidade de bairros. |
| carregar_dados / salvar_dados | dict / None. Recebem caminho e, na gravação, a base a persistir. |

Todas as 33 funções da aplicação possuem docstrings e anotações de parâmetros e retorno na versão verificada. As anotações documentam os tipos; a validação em tempo de execução é realizada pelas condições do código. Funções de tela retornam None ou a tupla de resultado da operação.

## 9. Validações e Tratamento de Erros

### Entradas e integridade

| Verificação | Comportamento |
| --- | --- |
| Número inválido ou fora do intervalo | ler_inteiro() e escolher_opcao() explicam o erro e repetem a entrada. |
| Texto vazio, curto ou longo | validar_texto() confere o tipo e o tamanho depois de padronizar os espaços. |
| ID inexistente | A busca retorna None e a tela apresenta uma mensagem sem alterar a base. |
| Cancelamento | 0 nas seleções cancela; N recusa a exclusão. A cópia não é aplicada à base. |
| Edição sem mudanças | ENTER mantém valores atuais. Se nada mudar, informa o resultado e não grava novamente. |
| Nomes antigos de bairro | A validação da base aceita texto entre 2 e 80 caracteres. Nomes conhecidos são exibidos no padrão; os demais são preservados. |

### Falhas e recuperação

| Situação | Resposta da aplicação |
| --- | --- |
| Arquivo ausente | Cria a pasta necessária e a base vazia com proximo_id igual a 1. |
| JSON inválido ou estrutura inconsistente | Informa o erro e interrompe a abertura sem apagar o arquivo. IDs repetidos e opções desconhecidas são rejeitados. |
| Falha ao gravar | Mostra a falha, limpa o temporário quando possível e mantém a base anterior em memória. |
| EOF ou CTRL+C durante os menus | Encerra de forma controlada. As operações já confirmadas continuam no JSON. |

Se o JSON estiver inválido, confira o conteúdo ou restaure uma cópia válida antes de abrir o sistema novamente. O programa não apaga a base para tentar corrigir o problema. Na interface atual, não há função de restauração ou histórico de versões.

O projeto foi pensado para uma execução local por vez. A confirmação de sucesso aparece somente após concluir a gravação da operação.

## 10. Guia de Execução

### Preparação do ambiente

Utilize Python 3.10 ou superior. O sistema usa apenas os módulos padrão sys, copy, json, os e unicodedata, além dos módulos do próprio projeto. Não há pacote a instalar com pip, servidor, credencial ou acesso à internet necessário para o CRUD.

Abra a pasta do projeto no VS Code ou em outro editor. No terminal, dentro da pasta, execute:

```console
python main.py
```

No Windows, o launcher pode ser utilizado quando estiver configurado:

```console
py main.py
```

Também é possível selecionar o interpretador no VS Code ou informar o caminho completo. Exemplo da instalação usada nesta verificação:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" .\main.py
```

O caminho completo é específico da instalação. O requisito da aplicação continua sendo Python 3.10 ou superior. A verificação desta documentação foi executada com Python 3.14.3.

### Navegação

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

O JSON fica em dados/denuncias.json, sempre a partir da pasta do projeto. Bases existentes são mantidas. Após cada operação, pressione ENTER para retornar ao menu; use 0 para voltar ou sair.

## 11. Verificação do Funcionamento

Execute o roteiro em uma cópia de teste com base vazia para obter IDs previsíveis. Em uma base já utilizada, anote os IDs retornados pelo cadastro. Os endereços e relatos abaixo são fictícios.

| Passo | Ação | Resultado esperado |
| --- | --- | --- |
| 1 | Denúncias > 1: Buraco na via, Centro, Rua Exemplo, 10; descrever o problema. | ID 1; situação inicial Aberta. |
| 2 | Cadastrar Iluminação pública em Centro e Descarte irregular de lixo em Bela Vista. | IDs 2 e 3; ambos inicialmente abertos. |
| 3 | Denúncias > 2 e > 3: listar e consultar o ID 1. | Resumo na listagem; endereço e descrição na consulta por ID. |
| 4 | Denúncias > 6: escolher Centro. | Somente os registros 1 e 2. |
| 5 | Denúncias > 4: editar ID 2 para Resolvida e ID 3 para Em andamento; ENTER mantém os demais campos. | Campos preservados e situações atualizadas. |
| 6 | Voltar > Ranking dos bairros. | 3 denúncias em 2 bairros; Centro com 2, Bela Vista com 1; uma em cada situação. |
| 7 | Excluir ID 3 e responder N. | Exclusão cancelada; o ranking permanece igual. |
| 8 | Excluir ID 3 e responder S. | Registro removido; próxima consulta e ranking não o incluem. |
| 9 | Cadastrar outra denúncia. | Novo ID 4; o ID excluído não é reutilizado. |
| 10 | Sair e executar novamente. | Registros, situações e próximo ID preservados. |

### Resultados das verificações realizadas

Em 18/11/2026 foram conferidos CRUD, consultas, agrupamento do ranking, resumo por situação, edição e exclusão, cancelamentos e IDs não reutilizados. A execução completa pelo terminal e o reinício passaram com dados fictícios em uma cópia temporária.

Também passaram as verificações de JSON ausente e inválido, falha simulada de gravação preservando o arquivo anterior, sintaxe compatível com Python 3.10 e análise do código sem classes ou comprehensions. As 33 funções tinham docstrings e tipos anotados. O roteiro de terminal confirmou nove pausas com ENTER.

O arquivo real dados/denuncias.json foi comparado antes e depois dos testes e permaneceu idêntico. Esses resultados registram verificações desta versão, sem substituir a avaliação acadêmica.

## 12. Referências

1. FIAP. 1TDS Fevereiro - Global Solution 2026-2. Seção Computational Thinking Using Python, páginas 39 a 44. Enunciado fornecido pelo grupo.

Leituras de apoio na documentação oficial do Python:

- [JSON](https://docs.python.org/3/library/json.html)
- [Controle de fluxo](https://docs.python.org/3/tutorial/controlflow.html)
- [Estruturas de dados](https://docs.python.org/3/tutorial/datastructures.html)
- [Cópia de objetos](https://docs.python.org/3/library/copy.html)
