# Font Spacing Engine

## Descrição

O **Font Spacing Engine** é um sistema que integra a API do Google Fonts com o motor de manipulação FontForge para realizar a normalização sistemática de famílias tipográficas. Seu objetivo principal é eliminar sidebearings (espaçamentos laterais) existentes nas fontes e aplicar novos algoritmos de espaçamento.


## Funcionalidades

- **Download Automatizado**: Integração com a API do Google Fonts para baixar fontes TTF diretamente do repositório oficial.
- **Processamento de Espaçamento**: Utiliza FontForge para manipular fontes, removendo kerning e referências existentes, resetando sidebearings e aplicando algoritmos de autoWidth dinâmicos baseados no tamanho EM da fonte.
- **Agrupamento Óptico**: Classifica letras em grupos por afinidade óptica (retas, redondas, diagonais) para aplicar compensações adequadas no espaçamento.
- **Extração de Métricas**: Coleta métricas detalhadas de sidebearings (esquerdo e direito) para cada glifo alfabético.
- **Exportação em CSV**: Gera um arquivo CSV estruturado com todas as métricas coletadas, facilitando análise posterior em ferramentas como Excel ou Python.

## Como Funciona

1. **Download**: O sistema baixa fontes selecionadas da API do Google Fonts e as armazena na pasta `data/raw/`.
2. **Processamento**: Cada fonte é aberta no FontForge, onde:
   - São removidas tabelas de kerning e ajustes GPOS.
   - Glifos compostos são convertidos em contornos reais.
   - Sidebearings são resetados para zero.
   - É aplicado autoWidth com parâmetros calculados dinamicamente (baseados em 20% do EM para separação base, com mínimos e máximos ajustados).
   - Letras são agrupadas e processadas com compensações específicas para otimizar o espaçamento óptico.
3. **Extração**: Após o processamento, as métricas de sidebearings são extraídas para cada letra (maiúscula e minúscula).
4. **Exportação**: Todas as métricas são compiladas em um CSV na pasta `data/output/`.

## Pré-requisitos

- Python 3.7+
- FontForge instalado no sistema
- Chave da API do Google Fonts (obtenha em [Google Fonts Developer API](https://developers.google.com/fonts/docs/developer_api))

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/emanuelfrx/font_spacing_engine.git
   cd font_spacing_engine
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Instale o FontForge:
   - No Ubuntu/Debian: `sudo apt install fontforge`
   - No macOS: `brew install fontforge`
   - No Windows: Baixe do site oficial do FontForge.

4. Configure a chave da API: Edite o arquivo `main.py` e substitua `GOOGLE_FONTS_API_KEY` pela sua chave.

## Uso

Execute o script principal:
```bash
python main.py
```

O sistema processará a lista de fontes definida em `main.py` e gerará o arquivo `data/output/metricas_fontes_lote.csv` com as métricas.

## Estrutura do Projeto

```
font_spacing_engine/
├── main.py                 # Script principal de execução
├── README.md               # Este arquivo
├── requirements.txt        # Dependências Python
├── data/
│   ├── raw/                # Fontes baixadas (TTF)
│   ├── processed/          # Fontes processadas (TTF)
│   └── output/             # Arquivo CSV de métricas
└── src/
    ├── __init__.py
    ├── config.py           # Configurações (atualmente vazio)
    ├── downloader.py       # Módulo de download do Google Fonts
    ├── processor.py        # Módulo de processamento com FontForge
    └── exporter.py         # Módulo de exportação para CSV
```

