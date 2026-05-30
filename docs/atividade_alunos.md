# Atividade Avaliativa — Pipeline de Deploy para Aplicação de Data Science

## Contexto

Você recebeu uma aplicação de Data Science já pronta. Ela apresenta um dashboard de monitoramento ambiental baseado em dados sintéticos inspirados em fontes espaciais e climáticas.

O foco desta atividade não é desenvolver a aplicação, mas sim criar uma pipeline no Azure DevOps para automatizar a publicação da solução na nuvem.

## Objetivo

Criar uma pipeline que publique a aplicação em um Azure Container Instance usando uma imagem Docker armazenada no Azure Container Registry.

## Fluxo esperado

```text
Repositório
   ↓
Azure DevOps Pipeline
   ↓
Docker Build
   ↓
Azure Container Registry
   ↓
Azure Container Instance
   ↓
URL pública da aplicação
```

## Requisitos técnicos

A pipeline deve conter etapas para:

1. realizar checkout do repositório;
2. criar ou validar o Resource Group;
3. criar ou validar o Azure Container Registry;
4. habilitar o Admin User no ACR ou configurar autenticação equivalente;
5. realizar build da imagem Docker;
6. publicar a imagem no ACR;
7. criar ou recriar o Azure Container Instance;
8. liberar a porta `8080`;
9. exibir no log da pipeline a URL pública da aplicação.

## Regras

- A aplicação deve ser publicada em Azure Container Instance.
- A imagem deve ser publicada em Azure Container Registry.
- A pipeline deve poder ser executada mais de uma vez.
- Não altere a aplicação, exceto se o professor autorizar.
- Use nomes de recursos que identifiquem o grupo.

## Sugestão de nomes de recursos

Substitua `grupoXX` pelo número ou nome do seu grupo.

```text
Resource Group: rg-spacedata-grupoXX
ACR: acrspacedatagrupoXX
ACI: aci-spacedata-grupoXX
Image: space-data-monitor
DNS Label: spacedata-grupoXX
```

## Entregáveis

O grupo deve entregar:

- print da pipeline executada com sucesso;
- link público da aplicação;
- print da aplicação funcionando no navegador;
- breve desenho ou imagem da arquitetura;
- README ou texto curto explicando o fluxo criado;
- principais comandos ou tasks utilizadas na pipeline.

## Tempo

Tempo máximo para conclusão: **4 horas**.
