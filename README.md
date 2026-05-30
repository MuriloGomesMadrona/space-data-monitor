# SpaceData Monitor

Aplicação pronta para a atividade de **Data Science + Cloud + DevOps**.

O objetivo da turma é criar uma pipeline no **Azure DevOps** para publicar esta aplicação em container na Azure, usando:

- Azure DevOps Pipeline
- Docker
- Azure Container Registry (ACR)
- Azure Container Instance (ACI)

## Sobre a aplicação

O **SpaceData Monitor** é um dashboard em Streamlit que simula o monitoramento ambiental do Brasil com indicadores inspirados em fontes públicas de dados espaciais e climáticos.

A aplicação apresenta:

- focos de queimadas;
- área desmatada estimada;
- precipitação;
- temperatura média;
- índice de vegetação NDVI;
- score de risco ambiental;
- mapa de risco;
- gráficos e tabela de alertas.

> O dataset é sintético e foi criado apenas para fins acadêmicos.

## Estrutura do projeto

```text
space-data-monitor/
├── app/
│   └── app.py
├── data/
│   └── space_environmental_risk.csv
├── docs/
│   ├── atividade_alunos.md
│   ├── checklist_entrega.md
│   └── arquitetura_referencia.md
├── scripts/
│   └── run-local.sh
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md
```

## Executando localmente com Python

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

streamlit run app/app.py --server.port=8080 --server.address=0.0.0.0
```

Acesse:

```text
http://localhost:8080
```

## Executando com Docker

```bash
docker build -t space-data-monitor:local .

docker run --rm -p 8080:8080 space-data-monitor:local
```

Acesse:

```text
http://localhost:8080
```

## Desafio da turma

A aplicação já está pronta. O trabalho dos alunos é criar a pipeline para:

1. fazer checkout do repositório;
2. criar ou validar o Resource Group;
3. criar ou validar o Azure Container Registry;
4. buildar a imagem Docker;
5. publicar a imagem no ACR;
6. criar ou recriar o Azure Container Instance;
7. exibir a URL pública da aplicação no log da pipeline.

## Porta da aplicação

A aplicação está configurada para executar na porta:

```text
8080
```

Essa porta deve ser usada na criação do Azure Container Instance.
