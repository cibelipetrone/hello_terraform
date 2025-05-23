# Projeto AWS Lambda com Terraform

Este projeto tem como objetivo criar uma função AWS Lambda com Terraform, como estudo de infraestrutura como código (IaC).

## Tecnologias utilizadas

- AWS Lambda
- Terraform
- Python

## Como iniciar o projeto

### 1. Pré-requisitos:

- AWS CLI instalado e configurado
- Terraform instalado
- Python
- Git

### 2. Clone o repositorio:

 ```
git clone
cd hello-terraform
```

### 3. Instalando as dependências Python

Antes de empacotar as funções Lambda, instale as dependências necessárias:

```sh
pip install -r requirements.txt
```

### 4. Gerando os arquivos ZIP das Lambdas

Antes de rodar o `terraform plan` ou `terraform apply`, é necessário gerar os arquivos `.zip` das funções Lambda. Siga os passos abaixo:

1. **Entre na pasta `hello_terraform`**, pois é lá que está a pasta `scripts`:

 ```
 cd hello_terraform
 ```

2. **Rode o comando para gerar os arquivos ZIP:**

  ```bash
  python scripts/build_lambdas.py
  ```

3. **Verifique se os arquivos `.zip` foram criados na pasta `dist`.**

### 5. Inicialize o Terraform

``` 
cd terraform
terraform init
terraform plan
terraform apply
```

## Como Usar os Scripts

### 1. Menu Interativo para Gerenciar Usuários

```bash
python manage_users.py
```

Você verá um menu com opções para:

- Atualizar email  
- Atualizar nome de usuário preferido  
- Criar novo usuário  
- Sair  

### 2. Modo Linha de Comando - Atualizar Email

```bash
python manage_users.py --mode email --username grazi --email novo@exemplo.com
```

### 3. Modo Linha de Comando - Atualizar Nome de Usuário Preferido

```bash
python manage_users.py --mode username --username grazi --new-username novonome
```

### 4. Modo Linha de Comando - Criar Novo Usuário

```bash
python manage_users.py --mode create --username novousuario --email novo@exemplo.com --password SenhaSegura123
```

### Script de Token e Autenticação

```bash
python test_api_interactive.py
```

## Como colaborar

Para colaborar com o projeto e propor mudanças é necessario a abertura de Pull Requests (PRs)

### Convenção de nomes de branches

Use o seguinte padrão para nomear suas branches:

- `feature/nome-do-recurso`: novas funcionalidades
- `bugfix/descricao-do-bug`: correção de problemas
- `hotfix/ajuste-crítico`: correções urgentes em produção
- `release/x.y.z`: novo release

### Conventional Commits

Siga o padrão para realizar os commits:

```
<tipo>(escopo opcional): descrição
```

Tipos mais comuns:

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `chore`: tarefas de manutenção (builds, configs, etc.)
- `docs`: apenas documentação
- `refactor`: refatoração de código (sem nova feature ou bug fix)
- `test`: testes
- `style`: formatação, identação, etc. (sem alteração de código funcional)

Exemplo:

```
feat(lambda): adiciona tratamento de erro
```
