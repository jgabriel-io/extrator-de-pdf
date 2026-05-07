# Cut-Doc

Ferramenta web para buscar um nome em um arquivo PDF e extrair as páginas onde ele aparece, empacotadas em um ZIP com PNG e PDF individual.

Criada para separar certificados da FEPI, que envia um único PDF com os certificados de todos os alunos.

## Funcionalidades

- Busca com fallback inteligente: busca exata → case-insensitive → normalização de acentos
- Extrai cada página encontrada como PNG (300 DPI) e PDF individual (opcional)
- Retorna tudo em um único `.zip`

## Instalação

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

## Uso local

```bash
gunicorn web_app:app
```

Acesse `http://localhost:8000`, suba o PDF, informe o nome e baixe o ZIP.

## Deploy

O projeto inclui um `Procfile` pronto para Render, Railway e Heroku. Basta conectar o repositório e fazer o deploy — a plataforma detecta o `Procfile` automaticamente.

## Licença

MIT — veja o arquivo [LICENSE](LICENSE).
