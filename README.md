# Organizador Fiscal de XML - Simples Nacional

![Versão do Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Licença](https://img.shields.io/badge/License-MIT-green.svg)

Uma aplicação de desktop desenvolvida em Python para automatizar a organização de arquivos XML de Notas Fiscais (NF-e/NFS-e) com base na sua tributação no Simples Nacional.

![Captura de Tela da Aplicação](URL_DA_SUA_IMAGEM_AQUI)
*(Dica: Tire uma captura de tela do seu aplicativo, adicione ao seu repositório e substitua a URL acima)*

---

## 🚀 Sobre o Projeto

Este projeto nasceu da necessidade de organizar de forma eficiente lotes de arquivos XML de notas fiscais, um desafio comum para contadores e pequenas empresas. A aplicação lê os arquivos, identifica o código de atividade fiscal (CNAE ou Código de Serviço Municipal) e move cada arquivo para uma pasta correspondente ao seu Anexo de tributação no Simples Nacional (Anexo I, II, III, etc.).

Toda a configuração é feita através de uma interface gráfica intuitiva, sem a necessidade de editar o código.

## ✨ Principais Funcionalidades

-   **Interface Gráfica Intuitiva:** Desenvolvida com Tkinter, permite um uso fácil e direto.
-   **Leitura em Lote:** Selecione uma pasta e o programa processará todos os arquivos `.xml` contidos nela.
-   **Identificação Inteligente de Códigos:** Busca por códigos CNAE (7 dígitos) e Códigos de Serviço Municipais (9 dígitos) em qualquer campo do XML.
-   **Mapeamento Configurável:** Cadastre, edite e remova as regras de mapeamento (Código x Anexo) diretamente na interface.
-   **Configuração Persistente:** Suas regras de mapeamento são salvas no arquivo `mapeamentos.json` e carregadas automaticamente ao iniciar o programa.
-   **Organização Automática:** Cria pastas de destino para cada Anexo e move os arquivos classificados.
-   **Log de Processamento:** Acompanhe em tempo real quais arquivos foram processados, movidos ou não encontrados.

## 🛠️ Tecnologias Utilizadas

-   **Python 3:** Linguagem principal do projeto.
-   **Tkinter:** Biblioteca padrão do Python para a criação da interface gráfica.
-   **Bibliotecas Nativas:** Utiliza apenas bibliotecas padrão do Python (`os`, `shutil`, `json`, `xml`, etc.), não necessitando de instalações via `pip`.

## ⚙️ Como Usar

Existem duas maneiras de executar a aplicação:

### Opção A: Usando o Executável (Recomendado para não-desenvolvedores)

1.  Vá para a seção de **[Releases](https://github.com/matias-en/Simples-Nacional---Organizador_xml/releases)** deste repositório.
2.  Baixe a versão mais recente do arquivo `.exe` (ex: `OrganizadorFiscal.exe`).
3.  Coloque o executável em uma pasta de sua preferência.
4.  Execute o programa. Na primeira vez, o arquivo `mapeamentos.json` será criado na mesma pasta.
5.  Cadastre suas regras de mapeamento na interface.
6.  Selecione a pasta com os XMLs de entrada e inicie o processamento. Os arquivos organizados aparecerão na pasta `xml_organizados`.

### Opção B: Rodando a partir do Código-Fonte

1.  Certifique-se de ter o **Git** e o **Python 3** instalados em sua máquina.
2.  Clone este repositório:
    ```bash
    git clone [https://github.com/matias-en/Simples-Nacional---Organizador_xml.git](https://github.com/matias-en/Simples-Nacional---Organizador_xml.git)
    ```
3.  Navegue até a pasta do projeto:
    ```bash
    cd Simples-Nacional---Organizador_xml
    ```
4.  Execute o script principal:
    ```bash
    python seu_script.py 
    ```
    *(Substitua `seu_script.py` pelo nome real do seu arquivo .py)*

## 📂 Estrutura de Pastas do Projeto
