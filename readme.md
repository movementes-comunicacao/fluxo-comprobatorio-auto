md# 📊 FLUXO-COMPROBATORIO-AUTO

Sistema de automação para coleta de métricas de redes sociais (Instagram, Facebook, Twitter, YouTube, TikTok e Threads), organizando os dados em planilhas Google Sheets e relatórios `.xlsx`.

---

## 📁 Estrutura do Projeto

```
FLUXO-COMPROBATORIO-AUTO/
├── components/                   # Submódulos com automações e gerenciadores
├── data/                         # Pasta local para armazenamento temporário
├── srcs/
│   ├── auto_sheets/             # Módulos de extração e input de dados
│   ├── sec_utils.py             # Utilitários auxiliares
│   └── utils.py                 # Funções gerais como remoção de emojis
├── utils/
│   ├── .env     # Arquivos .env com variáveis de ambiente
│   └── defining_env.py          # Leitura do arquivo de variáveis
├── main.py                      # Ponto principal de execução
├── relatorio.xlsx               # Arquivo gerado com as métricas coletadas
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

---

## 🚀 Como usar

### 1. Clone o projeto (com submódulos)

O projeto usa submódulos Git. Use o comando abaixo para garantir que tudo seja baixado corretamente:

```bash
git clone --recurse-submodules https://github.com/movementes-comunicacao/fluxo-comprobatorio-auto.git
cd fluxo-comprobatorio-auto
```

> ⚠️ Se você já clonou o projeto sem `--recurse-submodules`, execute:
>
> ```bash
> git submodule update --init --recursive
> ```

---

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure as variáveis de ambiente

Crie ou edite os arquivos `.env` dentro da pasta `utils/.env`. Exemplo: `utils/ex.env`.

Você pode definir qual arquivo `.env` usar editando a variável `env_variable_prefix` no `main.py`:

```python
env_variable_prefix = "name"
```

---

### 5. Execute o script principal

```bash
python main.py
```

Você também pode executar com o argumento `dtchoose` para forçar seleção de período:

```bash
python main.py dtchoose
```

---

## 📌 Funcionalidades

- Extração de postagens das principais redes sociais
- Remoção de emojis e limpeza de texto
- Organização por mês
- Input automático em planilhas Google Sheets
- Exportação de relatório `.xlsx`

---

## 🧱 Dependências principais

- `pandas`
- `gspread`
- `playwright`
- `beautifulsoup4`
- `submodule components e suas dependências` - https://github.com/gabrielsbf/components.git

---

## 🔐 Acesso ao Google Sheets

Você precisará de uma conta de serviço Google com permissão nas planilhas. O caminho para o JSON de autenticação deve estar definido em `SERVICE_ACC_PATH` no arquivo `.env`.

---

## 🛠️ Em desenvolvimento por:

> Projeto interno de automação e extração de dados para comprovação de presença digital e desempenho social.

---