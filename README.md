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

1. **Entre na pasta `hello_terraform`**, pois é lá que estão as pastas `src` e `build`:

   ```powershell
   cd hello_terraform
   ```

2. **Crie a pasta `build` (caso ainda não exista):**

   ```powershell
   mkdir .\build
   ```

3. **Rode cada comando separadamente para gerar os arquivos ZIP:**

   - Primeiro comando:

     ```powershell
     Compress-Archive -Path .\src\lambda\lambda_hello\* -DestinationPath .\build\hello_terraform.zip
     ```

   - Segundo comando:

     ```powershell
     Compress-Archive -Path .\src\lambda\shopping_list\add_item_dynamodb.py -DestinationPath .\build\add_item_dynamodb.zip
     ```

   - Terceiro comando:

     ```powershell
     Compress-Archive -Path .\src\lambda\shopping_list\update_item.py -DestinationPath .\build\update_item.zip
     ```

   - Quarto comando:

     ```powershell
     Compress-Archive -Path .\src\lambda\shopping_list\delete_item.py -DestinationPath .\build\delete_item.zip
     ```

4. **Verifique se os arquivos `.zip` foram criados na pasta `build`.**

### 5. Inicialize o Terraform

``` 
cd terraform
terraform init
terraform plan
terraform apply
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
