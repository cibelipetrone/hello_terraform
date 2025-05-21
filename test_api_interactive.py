import json
import urllib.request
import urllib.error
import os
import getpass  # Para entrada segura de senha

def print_color(text, color):
    # Códigos ANSI para cores no terminal
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'reset': '\033[0m'
    }
    
    # Verificar se estamos em um ambiente Windows e ajustar
    if os.name == 'nt':
        # Habilitar cores ANSI no Windows
        os.system('')
    
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def get_user_input():
    print_color("=== Configuração da API ===", "cyan")
    
    client_id = input("Digite o Client ID (ou pressione Enter para usar o padrão): ") or "ga4jro0spsb7vs9832d7g4v2i"
    username = input("Digite o nome de usuário: ") or "grazi"
    password = getpass.getpass("Digite a senha: ") or "Test123!"
    api_url = input("Digite a URL da API (ou pressione Enter para usar o padrão): ") or "https://fkvjwyt090.execute-api.sa-east-1.amazonaws.com/prod/hello"
    region = input("Digite a região AWS (ou pressione Enter para usar o padrão): ") or "sa-east-1"
    
    return {
        "client_id": client_id,
        "username": username,
        "password": password,
        "api_url": api_url,
        "region": region
    }

def get_token(config):
    print_color("Obtendo token de autenticação...", "cyan")
    
    try:
        # Preparar URL do Cognito
        cognito_url = f"https://cognito-idp.{config['region']}.amazonaws.com/"
        
        # Preparar dados para a requisição
        data = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": config['client_id'],
            "AuthParameters": {
                "USERNAME": config['username'],
                "PASSWORD": config['password']
            }
        }
        
        # Converter dados para JSON
        data_json = json.dumps(data).encode('utf-8')
        
        # Preparar a requisição
        req = urllib.request.Request(cognito_url)
        req.add_header('X-Amz-Target', 'AWSCognitoIdentityProviderService.InitiateAuth')
        req.add_header('Content-Type', 'application/x-amz-json-1.1')
        
        # Fazer a requisição
        response = urllib.request.urlopen(req, data_json)
        
        # Ler e processar a resposta
        response_data = response.read().decode('utf-8')
        json_data = json.loads(response_data)
        
        # Extrair o token
        id_token = json_data['AuthenticationResult']['IdToken']
        print_color("Token obtido com sucesso!", "green")
        return id_token
    
    except urllib.error.HTTPError as e:
        print_color(f"Erro HTTP: {e.code}", "red")
        if hasattr(e, 'read'):
            error_message = e.read().decode('utf-8')
            print_color(f"Detalhes: {error_message}", "red")
        return None
    except Exception as e:
        print_color(f"Erro ao obter token: {str(e)}", "red")
        return None

def test_api(token, api_url):
    print_color("Testando endpoint GET /hello...", "cyan")
    
    try:
        # Preparar a requisição
        req = urllib.request.Request(api_url)
        req.add_header('Authorization', token)
        
        # Fazer a requisição
        response = urllib.request.urlopen(req)
        
        # Ler e processar a resposta
        response_data = response.read().decode('utf-8')
        json_data = json.loads(response_data)
        
        # Exibir resultado
        print_color(f"Sucesso! Status code: {response.getcode()}", "green")
        print_color("Resposta da API:", "cyan")
        print(json.dumps(json_data, indent=2))
        return json_data
    
    except urllib.error.HTTPError as e:
        print_color(f"Erro HTTP: {e.code}", "red")
        if hasattr(e, 'read'):
            error_message = e.read().decode('utf-8')
            print_color(f"Detalhes: {error_message}", "red")
        return None
    except Exception as e:
        print_color(f"Erro ao testar API: {str(e)}", "red")
        return None

def main():
    print_color("=== TESTE DA API DE LISTA DE COMPRAS ===", "cyan")
    
    # Obter configurações
    config = get_user_input()
    
    # Obter token
    token = get_token(config)
    if not token:
        return
    
    # Testar API
    test_api(token, config['api_url'])

if __name__ == "__main__":
    main()