# Organizador Fiscal de XML - Simples Nacional

![Versão do Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Licença](https://img.shields.io/badge/License-MIT-green.svg)

Uma aplicação de desktop desenvolvida em Python para automatizar a organização de arquivos XML de Notas Fiscais de Serviço (NFS-e) com base na sua tributação no Simples Nacional.

![Captura de Tela da Aplicação](https://github.com/matias-en/Separador_atividades_anexos-SimplesNacional/blob/main/image/separador.png?raw=true)

---

## 🚀 Sobre o Projeto

Este projeto nasceu da necessidade de organizar de forma eficiente lotes de arquivos XML de notas fiscais, um desafio comum para contadores e pequenas empresas. A aplicação lê os arquivos, identifica o código de atividade fiscal (CNAE ou Código de Serviço Municipal) e move cada arquivo para uma pasta correspondente ao seu Anexo de tributação no Simples Nacional (Anexo III, IV e V).

Toda a configuração é feita através de uma interface gráfica intuitiva, sem a necessidade de editar o código.

## ✨ Principais Funcionalidades

-   **Interface Gráfica Intuitiva:** Desenvolvida com Tkinter, permite um uso fácil e direto.
-   **Leitura em Lote:** Selecione uma pasta e o programa processará todos os arquivos `.xml` contidos nela.
-   **Identificação Inteligente de Códigos:** Busca por códigos CNAE (7 dígitos) e Códigos de Serviço Municipais (9 dígitos) em qualquer campo do XML.
-   **Mapeamento Configurável:** Cadastre, edite e remova as regras de mapeamento (Código x Anexo) diretamente na interface.
-   **Configuração Persistente:** Suas regras de mapeamento são salvas no arquivo `mapeamentos.json` e carregadas automaticamente ao iniciar o programa.
-   **Organização Automática:** Cria pastas de destino para cada Anexo e move os arquivos classificados.
-   **Log de Processamento:** Acompanhe em tempo real quais arquivos foram processados, movidos ou não encontrados.

## ⚙️ Como Usar

Existem duas maneiras de executar a aplicação:

### Opção A: Usando o Executável (Recomendado para não-desenvolvedores)

1.  Vá para a seção de **[Releases](https://github.com/matias-en/Separador_atividades_anexos-SimplesNacional/tree/main/releases)** deste repositório.
2.  Baixe a versão mais recente do arquivo `.exe` (ex: `OrganizadorFiscal.exe`).
3.  Coloque o executável em uma pasta de sua preferência.
4.  Execute o programa. Na primeira vez, o arquivo `mapeamentos.json` será criado na mesma pasta.
5.  Cadastre suas regras de mapeamento na interface.
6.  Selecione a pasta com os XMLs de entrada (ex: `C:\Users\SeuNome\Desktop\Notas_Fiscais`).
7.  Inicie o processamento. Os arquivos organizados aparecerão em uma nova pasta chamada `xml_organizados`, criada **ao lado** da sua pasta de entrada (ex: `C:\Users\SeuNome\Desktop\xml_organizados`).

### Opção B: Rodando a partir do Código-Fonte

1.  Certifique-se de ter o **Git** e o **Python 3** instalados em sua máquina.
2.  Clone este repositório:
    ```bash
    git clone https://github.com/matias-en/Separador_atividades_anexos-SimplesNacional
    ```
3.  Navegue até a pasta do projeto:
    ```bash
    cd Separador_atividades_anexos-SimplesNacional
    ```
4.  Execute o script principal:
    ```bash
    python organizador.py 
    ```
    *(Substitua `organizador.py` pelo nome real do seu arquivo .py)*

## 📂 Onde os Arquivos São Salvos?

A pasta `xml_organizados` é gerada **no mesmo diretório da pasta que você selecionou para processar**, ou seja, "ao lado" dela.

**Exemplo Prático:**

Se a sua estrutura de pastas for esta:

Documentos/
└── Notas_Para_Processar/
├── nota1.xml
├── nota2.xml
└── nota3.xml

Após selecionar a pasta `Notas_Para_Processar` e rodar o programa, a sua estrutura ficará assim:

Documentos/
├── Notas_Para_Processar/      <-- Ficará vazia ou com os arquivos não classificados.
|
└── xml_organizados/           <-- Nova pasta com os arquivos organizados.
├── Anexo I/
│   └── nota2.xml
└── Anexo III/
├── nota1.xml
└── nota3.xml

## 🛠️ Tecnologias Utilizadas

-   **Python 3:** Linguagem principal do projeto.
-   **Tkinter:** Biblioteca padrão do Python para a criação da interface gráfica.
-   **Bibliotecas Nativas:** Utiliza apenas bibliotecas padrão do Python (`os`, `shutil`, `json`, `xml`, etc.), não necessitando de instalações via `pip`.

## 🏗️ Como Construir o Executável (para Desenvolvedores)

Se você fez alterações no código-fonte e deseja gerar um novo executável `.exe`, siga os passos:

1.  Instale o PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Navegue até a pasta do projeto via terminal.
3.  Execute o comando de build:
    ```bash
    pyinstaller --onefile --windowed --name OrganizadorFiscal organizador.py
    ```
4.  O executável final estará na pasta `dist/`.

## 📜 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido por **matias-en**.
