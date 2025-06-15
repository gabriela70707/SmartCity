# 🌆 Smart City - Monitoramento Urbano com Django Rest Framework

## 📌 Sobre o Projeto
A escola **TecnoVille** está desenvolvendo um projeto de **transformação urbana** baseado no conceito de **Smart City**. A ideia é instalar sensores em pontos estratégicos da cidade para coletar **dados em tempo real** sobre:

✅ 🌡️ **Temperatura**  
✅ 💧 **Umidade**  
✅ 💡 **Luminosidade**  
✅ 🔢 **Contador de pessoas**  

Esses sensores serão posicionados em **praças, corredores e pátios**, permitindo o **monitoramento das condições urbanas** e ajudando na **tomada de decisões estratégicas**.

---

## ⚙️ Tecnologias Utilizadas
Este projeto foi desenvolvido utilizando:

- 🐍 **Python 3.11**
- 🎛️ **Django Rest Framework** (API REST)
- 🔐 **JWT (JSON Web Tokens)** (Autenticação segura)
- 🗃️ **Banco de dados SQLite** (Padrão Django)
- 📊 **Pandas & OpenPyXL** (Para importação/exportação de planilhas)

---

## 🌐 API - Endpoints Principais
A API permite **CRUD completo** sobre sensores e ambientes, além de opções avançadas de **importação e exportação de dados**.

### 🔹 CRUD - Sensores e Ambientes
| Método  | Endpoint               | Descrição |
|---------|-----------------------|------------|
| `POST`  | `/api/sensores/`       | **Criar** um novo sensor |
| `GET`   | `/api/sensores/`       | **Listar** todos os sensores |
| `PUT`   | `/api/sensores/{id}/`  | **Atualizar** um sensor existente |
| `DELETE`| `/api/sensores/{id}/`  | **Remover** um sensor |

Além disso, a API permite **filtrar dados** por **sensor, data e status**.

---

### 🔹 Autenticação JWT
A API utiliza **tokens JWT** para autenticação segura. O login é realizado via:

```bash
POST /api/token/
```
Para proteger os endpoints, apenas usuários autenticados podem registrar, atualizar ou deletar dados.

### 🔹 Importação de Arquivos
Os dados dos sensores podem ser importados via planilhas Excel através deste endpoint:
`POST` `/api/importar-excel/`

### 🔹 Exportação de Arquivos
O sistema pode gerar planilhas Excel automaticamente com os dados registrados, utilizando:
`GET` `/api/exportar-excel/`

---

## Rodando o projeto 🚀
1️⃣ Clonando o Projeto
Para rodar o projeto basta clona-lo no terminal da sua maquina:
```git clone https://github.com/gabriela70707/SmartCity.git```
```cd SmartCity```
```code .```  (Para abrir no VsCode, caso nao tenha instalado, instale e execute o comando novamente)

**Após isso, criar a env e ativa-lá:**

2️⃣ Ativando a ENV
**No terminal do VsCode:**

```bash
python -m venv env 
cd .\env\Scripts\
.\activate
```
**após isso voltar para a pasta raiz utilizando o comando:**

`cd..` *2 vezes*

---

## 🛠️ Configuração do Ambiente
1️⃣ Instalar Dependências
Antes de iniciar, certifique-se de instalar as dependências do projeto:

```bash 
pip install -r requirements.txt
```

2️⃣ Rodar Migrações
```bash 
python manage.py migrate
```

3️⃣ Criar um Superusuário
```bash
python manage.py createsuperuser
```
**Ou usar um existente: (caso siga o passo 4)**
username: Gabriela
password: 24240113

4️⃣ Carregar Dados Iniciais
Se quiser iniciar o projeto com dados registrados, use:

```bash
python manage.py loaddata dados.json
```

## 🎯 O que o Administrador pode fazer?
O administrador pode: 
✅ Adicionar dados em ambientes e sensores.
✅ Importar arquivos Excel com novos registros.
✅ Atualizar e deletar dados existentes.
✅ Filtrar registros por sensor, data e status.
✅ Exportar dados da tabela para planilhas Excel.

## 📌 Relacionamento Entre Tabelas
O sistema segue um modelo relacional entre Sensores, Ambientes e Histórico, garantindo uma estrutura organizada para os dados capturados.

## 💡 Considerações Finais
Este projeto tem como objetivo tornar o monitoramento urbano mais eficiente, facilitando a gestão de sensores e permitindo decisões baseadas em dados reais. 🔥

Se quiser contribuir ou sugerir melhorias, fique à vontade! 😃🚀