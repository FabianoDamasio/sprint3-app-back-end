from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from typing import List

from sqlalchemy.exc import IntegrityError

from model import Session, Membro, Family, Users
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Membrezia", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
membro_tag = Tag(name="Membro", description="Adição, visualização e remoção de membros à base")
family_tag = Tag(name="Família", description="Adição, visualização e remoção de famílias à base")
user_tag = Tag(name="Usuários", description="Adição, visualização e remoção de usuários à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/new_membro', tags=[membro_tag],
          responses={"200": MembroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro(form: MembroSchema):
    print('fomr', form)
    """Adiciona um novo Membro à base de dados

    Retorna uma representação dos membros e famílias associadas.
    """
    membro = Membro(
        name = form.name,
        cpf = form.cpf,
        age = form.age,
        civil_status = form.civil_status,
        street = form.street,
        number = form.number,
        complement = form.complement,
        district = form.district,
        city = form.city,
        cep = form.cep
    )
    logger.debug(f"Adicionando membro de nome: '{membro.name}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando membro
        session.add(membro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado membro de nome: '{membro.name}'")
        return apresenta_membro(membro), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Membro de mesmo nome já salvo na base!"
        logger.warning(f"Erro ao adicionar membro '{membro.name}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo membro!"
        logger.warning(f"Erro ao adicionar membro '{membro.name}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/membros', tags=[membro_tag],
         responses={"200": ListagemMembrosSchema, "404": ErrorSchema})
def get_membros():
    """Faz a busca por todos os membros cadastrados

    Retorna uma representação da listagem de membros.
    """
    logger.debug(f"Coletando membros ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    membros = session.query(Membro).all()

    if not membros:
        # se não há membros cadastrados
        return {"membros": []}, 200
    else:
        logger.debug(f"%d membros econtrados" % len(membros))
        # retorna a representação de membros
        print(membros)
        return apresenta_membros(membros), 200


@app.get('/membro', tags=[membro_tag],
         responses={"200": MembroViewSchema, "404": ErrorSchema})
def get_membro(query: MembroBuscaSchema):
    """Faz a busca por um membro a partir do cpf do membro

    Retorna uma representação dos produtos e comentários associados.
    """
    membro_cpf = query.cpf
    membro = query.name
    membro_id = query.id
    logger.debug(f"Coletando dados sobre membro #{membro_cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    if(membro) :
        membro = session.query(Membro).filter(Membro.name == membro).first()
    elif(membro_cpf) :
        membro = session.query(Membro).filter(Membro.cpf == membro_cpf).first()
    elif(membro_id) : 
        membro = session.query(Membro).filter(Membro.id == membro_id).first()

    if not membro:
        # se o produto não foi encontrado
        error_msg = "Membro não encontrado na base"
        logger.warning(f"Erro ao buscar membro '{membro_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Membro econtrado: '{membro.name}'")
        # retorna a representação de membro
        return apresenta_membro(membro), 200


@app.delete('/del_membro', tags=[membro_tag],
            responses={"200": MembroDelSchema, "404": ErrorSchema})
def del_membro(query: MembroBuscaSchema):
    """Deleta um membro a partir do id, nome ou cpf

    Retorna uma mensagem de confirmação da remoção.
    """
    membro_name = query.name
    membro_cpf = query.cpf
    membro_id = query.id
    logger.debug(f"Deletando dados sobre produto #{membro_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    if(membro_name) :
        memberFind = session.query(Membro).filter(Membro.name == membro_name).first()
        count = session.query(Membro).filter(Membro.name == membro_name).delete()
    elif(membro_cpf) :
        memberFind = session.query(Membro).filter(Membro.cpf == membro_cpf).first()
        count = session.query(Membro).filter(Membro.cpf == membro_cpf).delete()
    elif(membro_id) : 
        memberFind = session.query(Membro).filter(Membro.id == membro_id).first()
        count = session.query(Membro).filter(Membro.id == membro_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Membro #{memberFind.name} removido")
        return {"mesage": "Membro removido", "membro": memberFind.name, "cpf": memberFind.cpf}
    else:
        # se o membro não foi encontrado
        error_msg = "Membro não encontrado na base"
        logger.warning(f"Erro ao deletar membro #'{memberFind.name}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.put('/family_a_membro', tags=[membro_tag],
          responses={"200": MembroViewSchema, "404": ErrorSchema})
def add_familia_a_membro(form: FamilySchemaMember):
    """Adiciona familia a um membro
    """
    last_name = form.sobrenome
    member_id = form.id_do_membro
    logger.debug(f"Adicionando #{member_id} a família #{last_name}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca pela família
    family = session.query(Family).filter(Family.last_name == last_name).first()
    if not family:
        # se a família não for encontrado
        error_msg = "Família não encontrada na base"
        logger.warning(f"Erro ao adicionar membro a família '{last_name}', {error_msg}")
        return {"mesage": error_msg}, 404

    # fazendo a busca pelo membro
    member = session.query(Membro).filter(Membro.id == member_id).first()
    if not member:
        # membro não encontrado
        error_msg = "Membro não encontrado na base"
        logger.warning(f"Erro ao adicionar encontrar '{member.name}', {error_msg}")
        return {"mesage": error_msg}, 404

    # adicionando membro a família
    member.adiciona_familia(family)
    session.commit()

    logger.debug(f"Adicionado membro #{member.name} a família #{last_name}")

    # retorna a representação de família
    return apresenta_membro(member), 200






@app.post('/add_familia', tags=[family_tag],
          responses={"200": FamilySchema, "409": ErrorSchema, "400": ErrorSchema})
def add_family(form: FamilySchema):
    """Adiciona uma nova família à base de dados
    """
    family = Family(
        last_name = form.last_name
    )
    logger.debug(f"Adicionando família com sobrenome: '{family.last_name}'")

    session = Session()
    familyFind = session.query(Family).filter(Family.last_name == family.last_name).first()
    if not familyFind :
        try:
            # criando conexão com a base
            session = Session()
            # adicionando familia
            session.add(family)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado família com sobrenome: '{family.last_name}'")
            return show_family(family), 200

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar nova família"
            logger.warning(f"Erro ao adicionar família '{family.last_name}', {error_msg}")
            return {"mesage": error_msg}, 400
    else:
        error_msg = "Família de mesmo nome já salva na base"
        return {"mesage": error_msg}, 404
    


@app.get('/family', tags=[family_tag],
          responses={"200": FamilyViewchema, "404": ErrorSchema})
def get_family(query: FamilyBuscaSchema):
    """Consulta um família da base no sobrenome ou id
    """
    family_id = query.id
    family_last_name = query.sobrenome
    # criando conexão com a base
    session = Session()
    # validando campo para busca
    if(family_id) :
        family = session.query(Family).filter(Family.id == family_id).first()
    elif(family_last_name) :
        family = session.query(Family).filter(Family.last_name == family_last_name).first()

    if not family:
        # se a família nâo for encontrada
        error_msg = "Família não encontrado na base"
        logger.warning(f"Erro ao encontrar família '{family_last_name}', {error_msg}")
        return {"mesage": error_msg}, 404

    logger.debug(f"Família encontrada #{family_last_name} id '{family_id}'")

    # retorna a representação de família
    return show_family(family), 200


@app.get('/all_familys', tags=[family_tag],
         responses={"200": ListagemFamiliasSchema, "404": ErrorSchema})
def get_familys():
    """Faz a busca por todos as famílias cadastradas

    Retorna uma representação da listagem de famílias.
    """
    logger.debug(f"Coletando famílias")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    family = session.query(Family).all()

    if not family:
        # se não há famílias cadastradas
        return {"famílias": []}, 200
    else:
        logger.debug(f"%d famílias econtrados" % len(family))
        # retorna a representação de famílias
        return show_familys(family), 200
        
@app.put('/edit_family', tags=[family_tag],
          responses={"200": FamilyViewchema, "404": ErrorSchema})
def edit_family(query: FamilyBuscaSchema, form: FamilyEditSchema):
    """Editar uma família da base no último nome
    """
    family_last_name = query.sobrenome
    family_id = query.id

    family_new_last_name = form.novo_sobrenome
    edit_family = Family (
        last_name=family_new_last_name
    )
    # criando conexão com a base
    session = Session()
    # fazendo a busca pela família
    if(family_id):
        family = session.query(Family).filter(Family.id == family_id).first()
    else:
        family = session.query(Family).filter(Family.last_name == family_last_name).first()

    if not family:
        # se a família nâo for encontrada
        error_msg = "Família não encontrado na base"
        logger.warning(f"Erro ao encontrar família '{family_last_name}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        family.edita_familia(edit_family)
        session.commit()

    logger.debug(f"Família alterada #{family_last_name}")

    # retorna a representação de família
    return show_family(family), 200

@app.delete('/del_family', tags=[family_tag],
            responses={"200": FamilyViewchema, "404": ErrorSchema})
def del_family(query: FamilyBuscaSchema):
    """Deleta uma família com base no sobrenome ou id

    Retorna uma mensagem de confirmação da remoção.
    """
    family_last_name = query.sobrenome
    family_id = query.id
    logger.debug(f"Deletando família #{family_last_name}")
    # criando conexão com a base
    session = Session()
    # fazendo validação no campo preenchido para consulta
    if(family_id):
        familyFind = session.query(Family).filter(Family.id == family_id).first()
        count = session.query(Family).filter(Family.id == family_id).delete()
    else:
        familyFind = session.query(Family).filter(Family.last_name == family_last_name).first()
        count = session.query(Family).filter(Family.last_name == family_last_name).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Família removida #{familyFind.last_name}")
        return {"mesage": "Família removida", "família": familyFind.last_name}
    else:
        # se a família não foi encontrada
        error_msg = "Família não encontrado na base"
        logger.warning(f"Erro ao deletar a família #'{familyFind.last_name}', {error_msg}")
        return {"mesage": error_msg}, 404
    





@app.post('/add_user', tags=[user_tag],
          responses={"201": UserSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Adiciona um novo usuário à base de dados
    """
    user = Users(
        login = form.login,
        password = form.password
    )
    logger.debug(f"Adicionando usuário: '{user.login}'")

    session = Session()
    userFind = session.query(Users).filter(Users.login == user.login).first()

    if not userFind:
        try:
            # criando conexão com a base
            session = Session()
            # adicionando usuário
            session.add(user)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado membro de nome: '{user.login}'")
            return {"mesage": 'Adicionado com sucesso'}, 201

        except IntegrityError as e:
            # como a duplicidade do nome é a provável razão do IntegrityError
            error_msg = "usuário de mesmo nome já salvo na base!"
            logger.warning(f"Erro ao adicionar usuário '{user.login}', {error_msg}")
            return {"mesage": error_msg}, 409

    else:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo usuário!"
        logger.warning(f"Erro ao adicionar novo usuário '{user.login}', {error_msg}")
        return {"mesage": error_msg}, 400
    


@app.get('/user', tags=[user_tag],
          responses={"200": UserViewchema, "404": ErrorSchema, "401": ErrorSchema})
def get_user(query: UserBuscaSchema):
    """Consulta um família da base no sobrenome ou id
    """
    login = query.login
    password = query.password
    # criando conexão com a base
    session = Session()
    # validando campo para busca
    loginFind = session.query(Users).filter(Users.login == login).first()

    if not loginFind:
        # se a família nâo for encontrada
        error_msg = "Usuário não encontrado"
        logger.warning(f"Erro ao encontrar o usuário '{login}', {error_msg}")
        return {"check": False, "mesage": error_msg}, 404
    
    if(loginFind):
        if(loginFind.password == password):
            return {"check": True}, 200
        else:
            error_msg = "Usuário ou senha estão incorretos!"
            return {"check": False,"mesage": error_msg}, 401
        
@app.get('/all_users', tags=[user_tag],
         responses={"200": UserViewchema, "404": ErrorSchema})
def get_users():
    """Faz a busca por todos os usuários cadastrados
    """
    logger.debug(f"Coletando usuários")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    users = session.query(Users).all()

    if not users:
        # se não há famílias cadastradas
        return {"users": []}, 200
    else:
        logger.debug(f"%d famílias econtrados" % len(users))
        # retorna a representação de famílias
        return show_users(users), 200


@app.delete('/del_user', tags=[user_tag],
            responses={"200": UserViewchema, "404": ErrorSchema})
def del_user(query: UserDelSchema):
    """Deleta um usuário
    Retorna uma mensagem de confirmação da remoção.
    """
    login = query.login
    logger.debug(f"Deletando usuário #{login}")
    # criando conexão com a base
    session = Session()
    loginFind = session.query(Users).filter(Users.login == login).first()
    count = session.query(Users).filter(Users.login == login).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Usuário removido #{loginFind.login}")
        return {"mesage": "Usuário removido", "login": loginFind.login}
    else:
        # se o usuário não foi encontrado
        error_msg = "Usuário não encontrado na base"
        logger.warning(f"Erro ao deletar o usuário #'{loginFind.login}', {error_msg}")
        return {"mesage": error_msg}, 404