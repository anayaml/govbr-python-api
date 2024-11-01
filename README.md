# govbr-python-api

Todas as informações de CPF para testes e token de acessos utilizadas nos testes foram retiradas de [API Docs - Gov.br](https://www.gov.br/conecta/catalogo/apis/cadastro-base-do-cidadao-cbc-cpf/swagger_cpf_light.json/swagger_view) e são de uso e visualização pública.<br/>
O ambiente utilizado para os testes foi o ambiente de Homologação.

## Objetivo

O objetivo deste teste é utilizar a base de dados do gov.br para um simples cadastro de usuários, em que seriam utilizados os atributos de nome completo, cpf e informações referentes a endereço do usuário.

## Como funciona

Utilizando o pacote ``requests`` abrimos uma requisição de solicitação para um token de acesso [neste endereço](https://h-apigateway.conectagov.estaleiro.serpro.gov.br/oauth2/jwt-token). Ao obter o token, abrimos uma requisição no endpoint de consulta-cpf disponível [aqui](https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cpf-light/v2/consulta/cpf). <br/>
O endpoint nos retorna um arquivo .json que será manipulado a fim de só utilzar os atributos que interessam ao cadastro de usuários.
