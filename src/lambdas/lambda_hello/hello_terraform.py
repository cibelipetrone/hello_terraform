import json

def lambda_handler(event, context):
    # Obter informações do usuário autenticado via Cognito
    claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    user_id = claims.get('sub', 'Usuário não identificado')
    email = claims.get('email', 'Email não disponível')
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Para CORS
        },
        'body': json.dumps({
            'message': f"Hello, Terraform! Você está autenticado com sucesso.",
            'userId': user_id,
            'email': email
        })
    }