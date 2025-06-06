Situação a ser resolvida:

A escola TecnoVille está desenvolvendo um projeto de transformação urbana baseado no conceito de Smart City. A
ideia é implementar sensores em pontos estratégicos da cidade para coletar dados em tempo real sobre:

• 🌡️ Temperatura
• 💧 Umidade
• 💡 Luminosidade
• 🔢Contador de pessoas

Esses sensores serão instalados em locais como praças, corredores, pátios etc.

O objetivo do projeto é desenvolver um back-end utilizando Django Rest Framework para gerenciar esses
dados, que serão usados para monitorar as condições
em tempo real. A autenticação será realizada através de JSON Web Tokens (JWT).

Sobre a Api:
A API deve ter endpoints para criar, ler, atualizar e deletar (CRUD) dados dos sensores e ambientes.

Os dados devem contem 
Os dados dos sensores devem incluir:
 Temperatura (°C)
 Luminosidade (lux)
 Umidade (%)
 Contador(num)
são os tipos dos sensores


Deve ter login de usuario e ter como sair e deslogar
Implementar autenticação utilizando JSON Web Tokens (JWT) para proteger os endpoints.
Criar um super usuário para o nosso api_smart.
• username = seu primeiro nome (exatamente) sem acentuação. Gabriela
• password = seu número de matrícula no senai (está no portal) 24240113


Relacionamento entre tabelas ✅
Os relacionamentos deverão ser aplicados nas tabelas conforme
diagrama já mencionado acima.

Gerenciamento dos Sensores:
 Crie as opções de CRUD para cada registro. 

filtros:  tentei mais nao sei se vai funcionar ainda
Desenvolva opções de localização de
dados, principalmente por sensor, data e status.


Atualizar o status do sensor (ativo, inativo).



5. Dados:
Criar método para capturar dados de sensores e ambientes que estão nas planilhas disponibilizadas.

Os dados poderão ser exportados no formato de planilhas. - ter um endpoint so para isso 


🎯 O que o Adm deve fazer:
Histórias de Usuário:
1. Como administrador, eu quero criar um endpoint para registrar dados de sensores, para que eu
possa armazenar os dados de temperatura, luminosidade e umidade.
2. Como administrador, eu quero criar um endpoint para visualizar os dados dos sensores, para
que eu possa monitorar as condições ambientais.
3. Como administrador, eu quero implementar autenticação JWT, para garantir que apenas
usuários autorizados acessem os dados.