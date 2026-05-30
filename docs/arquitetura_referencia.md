# Arquitetura de Referência

A arquitetura esperada para a atividade é:

```text
Aluno
  ↓
Azure DevOps
  ↓
Pipeline CI/CD
  ↓
Docker Build
  ↓
Azure Container Registry
  ↓
Azure Container Instance
  ↓
Usuário acessa o dashboard pela URL pública
```

## Componentes

### Azure DevOps Pipeline

Responsável por automatizar o fluxo de entrega da aplicação.

### Docker

Responsável por empacotar a aplicação Streamlit em uma imagem portável.

### Azure Container Registry

Responsável por armazenar a imagem Docker gerada pela pipeline.

### Azure Container Instance

Responsável por executar o container da aplicação sem necessidade de gerenciar servidores.

### Dashboard

Aplicação Streamlit publicada na porta `8080`.
