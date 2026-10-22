# IF_API
Este repositório contém os códigos desenvolvidos no projeto: Sistema de Irrigação do HortIf: Análise, Implantação e Monitoramento de uma Solução Automatizada para a Sustentabilidade Hídrica e Produtiva. Além disso, o README será utilizado como "Diário de Programação"

### Resumo do Projeto
Este projeto visa desenvolver um sistema automatizado de irrigação para a Horta Agroflorestal (HortIf) do IFSP-Campus Registro, visando a vulnerabilidade do manejo hídrico manual durante recessos e fins de semana, que compromete a produtividade das culturas devido ao estresse hídrico. A solução proposta integra tecnologias IoT com o método de Penman-Monteith (FAO) para o cálculo preciso da Evapotranspiração da Cultura (ET0), garantindo uma reposição hídrica eficiente através de uma API desenvolvida em Python que gerencia a comunicação entre sensores meteorológicos, o sistema de controle e um dashboard web responsivo para monitoramento em tempo real. Além de otimizar o uso de recursos, o projeto possui uma forte dimensão socioeducativa ao servir como laboratório pedagógico multidisciplinar, com previsão de conclusão para outubro de 2026, quando serão validados os dados quantitativos de consumo e a eficiência do sistema em garantir a saúde vegetal e a estabilidade produtiva do espaço agroflorestal.

# Diário do Projeto

<details>
    <summary> 05/08/2026 </summary>

- Abertura do Repositório     
- Ainda sem programação: Foco total na leitura de artigos e na produção do artigo para a Fecivale.
</details>


<details>
    <summary> 13/09/2026 </summary>

- inserção de ambiente virtual para biblioteca
- instalação do uv
- instalação do FAST API 

- Justificativa:
    -  A aplicação do FAST API justifica-se pelo fato de que ele poderá permitir uma integração mais fácil ao microcontrolador da horte, sem haver necessidade de grandes alterações na programação do sistema ja pronto
    - Será realizado uma integração com o Google Sheets da estação meteorologica através do Google AppScripts

</details>

<details>
    <summary> 15 e 16/09/2026 </summary>

- criação de pasta 'calculo.py' para calcular a evapotranspiração
- criação de pasta 'teste.py' como um ambiente para testes

- Ideia para o protótipo da FECIVALE:
    - Utlizar de API Meteorlógica pronta e aplicar as fórmulas da evapotranspiração
    - Estudar agora qual metodologia abordar: Data base ou biblioteca Pandas?
    
- Pendencias:
    - A definir projeto final (Utilizando-se de base meteorlógica própria)
</details>

<details>
    <summary> 19 a 21/09/2026 </summary>

- Atualização de pasta 'calculo.py' para calcular a evapotranspiração
- Atualização de pasta 'teste.py' como um ambiente para testes
- Criação de pasta 'data.py' para coletar os dados e organiza-los, permitindo o calculo

- Ideia para o protótipo da FECIVALE:
    - Utlizar de API Meteorlógica pronta e aplicar as fórmulas da evapotranspiração
    - Estudar agora qual metodologia abordar: Banco SQL/NoSQL ou biblioteca Pandas?
        - Definida: biblioteca Pandas
    
- Pendencias:
    - A definir projeto final (Utilizando-se de base meteorlógica própria ou uma pronta)
</details>

<details>
    <summary> 24/09/2026 </summary>

- Atualização de pasta 'data.py' (correção de erro de escrita)
- Alterações na pasta 'pasta.py' (integração de 'calculo.py' e 'data.py')


- Protótipo da FECIVALE:
    - Bibliotecas
        - Pandas (analise, limpeza, exploração e manipulação de dados)
        - Requests (utilizado para coletar dados da API)
    - 
    
- Pendencias:
    - A definir projeto final (Utilizando-se de base meteorlógica própria ou uma pronta)
</details>

<details>
    <summary>01/10/2026</summary>

- Atualizações na pasta.py (edições em 'calculo.py' e 'teste.py')
- Correção de código em 'teste.py'
    - Adição de openpyxl para criação de planilha excel
    - Alteração para que o dados sejam registrados em planilhas
- Variavel 'altitude' de volta a 'calculo.py' para calculo da variavel gamma
    - Justificativa: rigor metodológico
- Adicionado resumo do projeto ao 'README.md'



- Protótipo da FECIVALE:
    - Bibliotecas
        - Pandas (analise, limpeza, exploração e manipulação de dados)
        - Requests (utilizado para coletar dados da API)
        - Mathe (biblioteca para calculos matemáticos)
        - Openpyxl (integração pyhton e excel)

- Pendencias:
    - A definir projeto final (Utilizando-se de base meteorlógica própria ou uma pronta)
    - [URGENTE] integração a dashboard
</details>

<details>
    <summary>05/10/2026</summary>

- Criação de pastas para dashboard (html/css/js)
- Refinamento da dahsboard



- Protótipo da FECIVALE:
    - Bibliotecas
        - Pandas (analise, limpeza, exploração e manipulação de dados)
        - Requests (utilizado para coletar dados da API)
        - Mathe (biblioteca para calculos matemáticos)
        - Openpyxl (integração pyhton e excel)

- Pendencias:
    - A definir projeto final (Utilizando-se de base meteorlógica própria ou uma pronta)
    - [EM ANDAMENTO] integração a dashboard
</details>
  
<details>
    <summary>11/10/2026</summary>

- Refinamento da dahsboard (agora recebe os dados do python)
- Nova variavel adicionada a 'teste.py'
- 'script.js' ajustado (gráfico corrigido)
- *Dados temporais* obtidos por dia


- Protótipo da FECIVALE:
    - Bibliotecas
        - Pandas (analise, limpeza, exploração e manipulação de dados)
        - Requests (utilizado para coletar dados da API)
        - Mathe (biblioteca para calculos matemáticos)
        - Openpyxl (integração pyhton e excel)

- Pendencias:
    - A definir projeto final (Utilizando-se de base meteorlógica própria ou uma pronta)
    - [Concluido] integração a dashboard
    - [A fazer] documento explicando o código parte a parte
    - [A fazer] migração para FASTAPI (pós fecivale)

- Nota:
    - O modelo da dashboard não é definitivo
    - No momento não integração com servidores externos
    - A confirmar intervalo de dias a ser apresentado no protótipo
</details>
  
<details>
    <summary>22/10/2026</summary>

- Atualização de card no arquivo html
- Criação de arquivo .yml para rodar a API
- Criado arquivo 'requirements.txt' para auxiliar na atualização de 'dados.json


- Protótipo da FECIVALE:
    - Bibliotecas
        - Pandas (analise, limpeza, exploração e manipulação de dados)
        - Requests (utilizado para coletar dados da API)
        - Mathe (biblioteca para calculos matemáticos)
        - Openpyxl (integração pyhton e excel)

- Pendencias:
    - [Definido] ~~A definir projeto final (Utilizando-se de base meteorlógica própria ou uma pronta)~~

            - Definido por utilizar FASTAPI, **A definir qual serviço para rodar a API**
    - [Concluido] integração a dashboard
    - [A fazer] documento explicando o código parte a parte
    - [A fazer] migração para FASTAPI (pós fecivale)

- Nota:
    - O modelo da dashboard não é definitivo
    - A confirmar intervalo de dias a ser apresentado no protótipo
</details>