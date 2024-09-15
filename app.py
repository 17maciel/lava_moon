import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definindo o banco de dados
engine = create_engine('sqlite:///site.db')
Base = declarative_base()

# Definição do modelo User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    birthdate = Column(Date, nullable=False)
    password = Column(String(60), nullable=False)

Base.metadata.create_all(engine)

# Criação da sessão para o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Função para autenticar o usuário
def authenticate_user(cpf, password):
    user = session.query(User).filter_by(cpf=cpf, password=password).first()
    return user

# Tela de login
def login_screen():
    st.title("Sistema Lava Jato - Login")

    cpf = st.text_input("CPF:")
    password = st.text_input("Senha:", type='password')

    if st.button("Login"):
        user = authenticate_user(cpf, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user_name'] = user.name
            st.success("Login realizado com sucesso!")
        else:
            st.error("CPF ou senha inválidos. Tente novamente.")

    if st.button("Cadastrar novo usuário"):
        st.session_state['show_register'] = True

# Tela de cadastro de novos usuários
def register_screen():
    st.title("Cadastro de Novo Usuário")
    
    name = st.text_input("Nome:")
    cpf = st.text_input("CPF:")
    birthdate = st.date_input("Data de Nascimento:")
    password = st.text_input("Senha:", type='password')

    if st.button("Cadastrar"):
        try:
            new_user = User(name=name, cpf=cpf, birthdate=birthdate, password=password)
            session.add(new_user)
            session.commit()
            st.success("Usuário cadastrado com sucesso!")
            st.session_state['show_register'] = False
        except Exception as e:
            st.error(f"Erro ao cadastrar usuário: {e}")

# Tela principal para realizar cadastros e lançamentos após login
def dashboard_screen():
    st.title(f"Bem-vindo, {st.session_state['user_name']}")
    
    st.subheader("Cadastros e Lançamentos")
    
    # Exemplo de cadastro de serviço
    st.write("Cadastrar Serviço")
    service_name = st.text_input("Nome do Serviço:")
    service_price = st.number_input("Preço do Serviço:", min_value=0.0, format="%.2f")

    if st.button("Salvar Serviço"):
        st.success(f"Serviço '{service_name}' cadastrado com sucesso!")

    # Exemplo de lançamento de transações
    st.write("Lançar Transação")
    customer_name = st.text_input("Nome do Cliente:")
    service_performed = st.text_input("Serviço Realizado:")
    transaction_value = st.number_input("Valor da Transação:", min_value=0.0, format="%.2f")

    if st.button("Lançar Transação"):
        st.success(f"Transação do cliente '{customer_name}' no valor de R${transaction_value} registrada!")

    st.button("Sair", on_click=logout)

# Função de logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_name'] = None
    st.success("Você saiu do sistema.")

# Configuração inicial do estado da sessão
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'show_register' not in st.session_state:
    st.session_state['show_register'] = False

# Fluxo de navegação baseado no estado de login
if st.session_state['logged_in']:
    dashboard_screen()
else:
    if st.session_state['show_register']:
        register_screen()
    else:
        login_screen()
