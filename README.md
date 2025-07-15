# Alfred: Seu Assistente de Desenvolvimento Pessoal

Alfred é um assistente de desenvolvimento inteligente projetado para operar localmente, otimizando seu fluxo de trabalho de codificação. Ele atua como um agente orientado a eventos, utilizando um conjunto de ferramentas modulares para analisar, otimizar e gerenciar seu código.

## Visão Geral

O objetivo principal do Alfred é garantir o melhor desempenho possível para o código que você escreve. Ele fará isso inspecionando o desenvolvimento, realizando testes de benchmark em funções e sinalizando as que apresentarem melhor desempenho. Embora opere offline, ele pode se conectar à internet para buscar sugestões de otimização de modelos de linguagem avançados (como o Gemini), mas sempre validará essas sugestões localmente através de testes empíricos.

## Arquitetura

Alfred é construído sobre um paradigma de **Agente Orientado a Eventos com Ferramentas**:

*   **Agente:** O núcleo do sistema, Alfred, é um agente autônomo que orquestra as operações.
*   **Orientado a Eventos:** Ele reage a eventos (como salvar um arquivo ou digitar um comando) para fornecer assistência proativa.
*   **Ferramentas:** Suas funcionalidades são encapsuladas em ferramentas modulares (ex: `CodeParserTool`, `BenchmarkingTool`, `CodeSuggestionTool`), que o agente utiliza conforme necessário.

## Como Executar

1.  Certifique-se de ter o Python 3 instalado.
2.  Execute o agente a partir da raiz do projeto:
    ```bash
    ./alfred.sh
    ```
3.  Você verá o prompt do Alfred (`>`).

## Comandos Disponíveis

*   `/index`: Indexa (ou reindexa) todas as funções Python no projeto. Mostra uma lista de todas as funções encontradas.
*   `/benchmark <function_name>`: Mede o tempo de execução de uma função específica. A função já deve ter sido indexada.
*   `/suggest <function_name>`: Fornece uma sugestão de otimização para uma função específica. (Atualmente, retorna um placeholder).
*   `/test <test_file_path>`: Executa testes unitários em um arquivo de teste específico usando pytest.
*   `/exit`: Encerra o Alfred.

**Recursos Adicionais:**
*   **Autocompletar com Tab:** Pressione `Tab` para autocompletar comandos e nomes de funções.

## Próximos Passos

1.  Implementar a chamada real à API na `CodeSuggestionTool` (atualmente simulada devido a limites de cota da API).
2.  Refatorar o `alfred.py` para melhorar a modularidade (concluído, com comandos agora carregados dinamicamente).
3.  Adicionar uma ferramenta para execução de testes unitários (concluído).
4.  Atualizar o `README.md` com as novas funcionalidades (concluído).
