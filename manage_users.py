import boto3
import sys
import argparse

def update_user_email(user_pool_id, username, new_email):
    print(f"Atualizando email do usuário '{username}' para '{new_email}'...")
    
    try:
        # Inicializar cliente Cognito
        cognito = boto3.client('cognito-idp', region_name='sa-east-1')
        
        # Atualizar atributos do usuário
        response = cognito.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': new_email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ]
        )
        
        print(f"Email atualizado com sucesso para '{new_email}'!")
        return True
        
    except Exception as e:
        print(f"Erro ao atualizar email: {str(e)}")
        return False

def update_username(user_pool_id, old_username, new_username):
    print(f"Atualizando nome de usuário de '{old_username}' para '{new_username}'...")
    
    try:
        # Inicializar cliente Cognito
        cognito = boto3.client('cognito-idp', region_name='sa-east-1')
        
        # Para atualizar o username, é necessário usar admin-update-user-attributes
        response = cognito.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=old_username,
            UserAttributes=[
                {
                    'Name': 'preferred_username',
                    'Value': new_username
                }
            ]
        )
        
        print(f"Nome de usuário preferido atualizado para '{new_username}'.")
        print(f"Nota: O Username principal não pode ser alterado diretamente no Cognito.")
        print(f"O valor 'preferred_username' foi atualizado, mas o login ainda usa '{old_username}'.")
        return True
        
    except Exception as e:
        print(f"Erro ao atualizar nome de usuário: {str(e)}")
        return False

def create_new_user(user_pool_id, username, email, password="Test123!"):
    print(f"Criando novo usuário '{username}' com email '{email}'...")
    
    try:
        # Inicializar cliente Cognito
        cognito = boto3.client('cognito-idp', region_name='sa-east-1')
        
        # Criar novo usuário
        response = cognito.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ],
            TemporaryPassword=password,
            MessageAction='SUPPRESS'  # Não enviar email
        )
        
        # Definir senha permanente
        cognito.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )
        
        print(f"Usuário '{username}' criado com sucesso!")
        print(f"Email: {email}")
        print(f"Senha: {password}")
        return True
        
    except Exception as e:
        print(f"Erro ao criar usuário: {str(e)}")
        return False

def print_menu():
    print("\n===== GERENCIADOR DE USUÁRIOS COGNITO =====")
    print("1. Atualizar email de usuário existente")
    print("2. Atualizar nome de usuário preferido")
    print("3. Criar novo usuário")
    print("0. Sair")
    return input("Escolha uma opção: ")

if __name__ == "__main__":
    # Configurações padrão
    USER_POOL_ID = 'sa-east-1_KIWpvq1cF'
    
    # Verificar se há argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Gerenciar usuários no Cognito')
    parser.add_argument('--mode', choices=['menu', 'email', 'username', 'create'], 
                        default='menu', help='Modo de operação')
    parser.add_argument('--username', help='Nome de usuário atual')
    parser.add_argument('--new-username', help='Novo nome de usuário')
    parser.add_argument('--email', help='Novo email')
    parser.add_argument('--password', default='Test123!', help='Senha para novo usuário')
    
    args = parser.parse_args()
    
    # Modo menu interativo
    if args.mode == 'menu':
        while True:
            choice = print_menu()
            
            if choice == '1':
                username = input("Nome de usuário: ")
                new_email = input("Novo email: ")
                update_user_email(USER_POOL_ID, username, new_email)
            
            elif choice == '2':
                username = input("Nome de usuário atual: ")
                new_username = input("Nome de usuário preferido: ")
                update_username(USER_POOL_ID, username, new_username)
            
            elif choice == '3':
                username = input("Nome de usuário para o novo usuário: ")
                email = input("Email para o novo usuário: ")
                password = input("Senha (deixe em branco para usar 'Test123!'): ") or "Test123!"
                create_new_user(USER_POOL_ID, username, email, password)
            
            elif choice == '0':
                print("Saindo...")
                break
            
            else:
                print("Opção inválida!")
            
            input("\nPressione Enter para continuar...")
    
    # Modo linha de comando
    elif args.mode == 'email' and args.username and args.email:
        update_user_email(USER_POOL_ID, args.username, args.email)
    
    elif args.mode == 'username' and args.username and args.new_username:
        update_username(USER_POOL_ID, args.username, args.new_username)
    
    elif args.mode == 'create' and args.username and args.email:
        create_new_user(USER_POOL_ID, args.username, args.email, args.password)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0)