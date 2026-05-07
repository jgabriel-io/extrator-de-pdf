# Cut-Doc

Ferramenta web para buscar um nome em um arquivo PDF e extrair as páginas onde ele aparece, empacotadas em um ZIP com PNG e PDF individual.

Criada para separar certificados da FEPI, que envia um único PDF com os certificados de todos os alunos.

🔗 **[cut-doc-extrator-de-pdf.onrender.com](https://cut-doc-extrator-de-pdf.onrender.com)**

## Funcionalidades

- Busca com fallback inteligente: busca exata → case-insensitive → normalização de acentos
- Extrai cada página encontrada como PNG (300 DPI) e PDF individual (opcional)
- Retorna tudo em um único `.zip`

## Uso local

1. Clone o repositório:
    ```bash
    git clone https://github.com/jgabriel-io/extrator-de-pdf.git
    cd extrator-de-pdf
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1  # Windows
    source .venv/bin/activate      # Linux/macOS
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Inicie o servidor:
    ```bash
    gunicorn web_app:app
    ```

Acesse `http://localhost:8000`.

## Licença

MIT — veja o arquivo [LICENSE](LICENSE).
