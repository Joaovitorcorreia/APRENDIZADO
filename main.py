from fastapi import FastAPI, Depends
from models import User
from schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
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
@app.post("/novo-usuário/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    novo_usuario = User(name=user.name, email=user.email)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"name": novo_usuario.name, "email": novo_usuario.email, "message": "Usuário criado com sucesso!"}

# Procura um usuário existente pelo email
@app.get("/usuários-existentes/", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == email).first()
    if not usuario_existente:
        return {"email": email, "message": "Usuário não encontrado."}
    return {"name": usuario_existente.name, "email": usuario_existente.email, "message": "Usuário encontrado com sucesso!"}
