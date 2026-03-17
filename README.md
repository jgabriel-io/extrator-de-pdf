# Cut-Doc: Extrator de Páginas de PDF

`cut-doc` é uma ferramenta de linha de comando para automatizar a busca de nomes em múltiplos arquivos PDF e extrair as páginas correspondentes. Ele é especialmente útil para processar grandes lotes de documentos, como certificados ou relatórios, e salvar as páginas relevantes em formatos PNG e PDF individuais, agrupados em um arquivo ZIP.

O projeto foi criado para otimizar a tarefa de separar certificados de conclusão de curso da FEPI.

## Funcionalidades

- Varre um diretório de arquivos PDF.
- Procura por um nome específico em cada página.
- Salva cada página encontrada como um arquivo PNG de alta resolução (300 DPI).
- Salva cada página encontrada como um arquivo PDF separado (opcional).
- Agrupa todos os arquivos gerados em um único arquivo `.zip` para fácil distribuição.
- Nome do arquivo ZIP sanitizado e com timestamp (Ex: `Nome-Sobrenome-20260317_1030.zip`).
- Limpa automaticamente os arquivos temporários após a criação do ZIP.

## Requisitos

- Python 3.7+
- `PyMuPDF`

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/jgabriel-io/extrator-de-pdf.git
    cd extrator-de-pdf
    ```

2.  **Crie e ative um ambiente virtual:**
    ```powershell
    # Criar o ambiente virtual
    python -m venv .venv

    # Ativar o ambiente virtual
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Instale as dependências:**
    ```powershell
    pip install pymupdf
    ```

## Como Usar

1.  Coloque todos os arquivos PDF que você deseja processar na pasta `pdf/` (ou crie-a se não existir).

2.  Execute o script `run.py` a partir do seu terminal, passando o nome que você deseja procurar como argumento.

    **Exemplo Básico:**
    ```powershell
    python run.py "João da Silva"
    ```

3.  Os arquivos de saída serão salvos em um arquivo ZIP dentro da pasta `out/`.

### Opções Avançadas

Você pode personalizar as pastas de entrada e saída e outras opções através de flags:

-   `--pdf-folder`: Especifica a pasta onde os PDFs estão localizados. (Padrão: `pdf`)
-   `--output-folder`: Especifica a pasta para salvar o ZIP final. (Padrão: `out`)
-   `--no-pdf`: Impede que os arquivos PDF individuais sejam salvos no ZIP, incluindo apenas os PNGs.

**Exemplo com flags:**
```powershell
python run.py "Maria Oliveira" --pdf-folder "C:\Users\seu_usuario\Documentos\Certificados" --output-folder "C:\Saidas" --no-pdf
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
