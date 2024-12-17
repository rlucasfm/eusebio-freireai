CITATION_QA_TEMPLATE = """
    Por favor, forne a uma resposta com base apenas nas fontes fornecidas. 
    Quando se referir a informa es de uma fonte, 
    cite a(s) fonte(s) apropriada(s) usando seus respectivos números. 
    Toda resposta deve incluir pelo menos uma citação. 
    Somente cite uma fonte quando está explicitamente se referindo a ela. 
    Se nenhuma das fontes for útil, você deve indicar isso. 
    Tenha certeza de incluir a numeração indicando a fonte citada, se possível.
    Por exemplo:\n
    Fonte 1:\n
    O céu está vermelho pela noite e azul pela manhã.\n
    Fonte 2:\n
    A água está molhada quando o céu está vermelho.\n
    Pergunta: Quando a água está molhada?\n
    Resposta: A água está molhada quando o céu está vermelho [2], 
    o que ocorre à noite [1].\n
    Agora é sua vez. Abaixo seguem várias fontes numeradas de informação:
    \n------\n
    {context_str}
    \n------\n
    Pergunta: {query_str}\n
    Resposta: """
    
CITATION_REFINE_TEMPLATE = """
    Please provide an answer based solely on the provided sources. 
    When referencing information from a source, 
    cite the appropriate source(s) using their corresponding numbers. 
    Every answer should include at least one source citation. 
    Only cite a source when you are explicitly referencing it. 
    If none of the sources are helpful, you should indicate that. 
    For example:\n
    Source 1:\n
    The sky is red in the evening and blue in the morning.\n
    Source 2:\n
    Water is wet when the sky is red.\n
    Query: When is water wet?\n
    Answer: Water will be wet when the sky is red [2], 
    which occurs in the evening [1].\n
    Now it's your turn. 
    We have provided an existing answer: {existing_answer}
    Below are several numbered sources of information. 
    Use them to refine the existing answer. 
    If the provided sources are not helpful, you will repeat the existing answer.
    \nBegin refining!
    \n------\n
    {context_msg}
    \n------\n
    Query: {query_str}\n
    Answer: """