from fastapi import FastAPI, Depends, HTTPException, status
from models import User
from schemas import UserCreate, UserMessageCreate_and_response, UserAtualizar, UserAtualizarResponse, UserDelete, UserDeleteResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# criar banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cria um novo usuário
@app.post("/novo-usuário/", response_model=UserMessageCreate_and_response)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    novo_usuario = User(name=user.name, email=user.email)

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O email já está em uso por outro usuário.")

    return {"name": novo_usuario.name, "email": novo_usuario.email, "message": "Usuário criado com sucesso!"}

# Procura um usuário existente pelo email
@app.get("/usuários-existentes/", response_model=UserMessageCreate_and_response)
def get_user(email: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == email).first()

    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    return {"name": usuario_existente.name, "email": usuario_existente.email, "message": "Usuário encontrado com sucesso!"}

# Atualiza um usuário existente pelo email
@app.put("/atualizar-usuário/", response_model=UserAtualizarResponse)
def update_user(email: str, user: UserAtualizar, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == email).first()

    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    if usuario_existente.name != user.new_name or usuario_existente.email != user.new_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome ou email atual não correspondem ao usuário existente.")

    try:
        usuario_existente.name = user.new_name
        usuario_existente.email = user.new_email
        db.commit()
        db.refresh(usuario_existente)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O novo email já está em uso por outro usuário.")

    return {"name": usuario_existente.name, "email": usuario_existente.email, "message": "Usuário atualizado com sucesso!"}

# Deleta um usuário existente pelo email
@app.delete("/deletar-usuário/", response_model=UserDeleteResponse)
def delete_user(email: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == email).first()

    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    db.delete(usuario_existente)
    db.commit()
    return {"email": email, "message": "Usuário deletado com sucesso!"}