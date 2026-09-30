from fastapi import FastAPI,HTTPException, status, APIRouter
from typing import Annotated, Any, List, Optional
from pathlib import Path
from app.models.aluno import AlunoResponse, AlunoRequest



ALUNOS = [
    {"id": 1, "nome": "Pedro", "idade": 19, "email": "pedro@gmail.com", "senha": "1234"},
    {"id": 2, "nome": "Arthur", "idade": 28, "email": "arthur@gmail.com", "senha": "12345"},
    {"id": 3, "nome": "Marcelo", "idade": 35, "email": "marcelo@gmail.com", "senha": "12346"},
    {"id": 4, "nome": "Mariana", "idade": 30, "email":"mariana@gmail.com", "senha": "12347"}
]

router = APIRouter()


@router.get("/")
async def home():
    return "Olá alunos"


@router.get("/alunos/", response_model=List[AlunoResponse], status_code=status.HTTP_200_OK)
async def Alunos()-> Any:
    return ALUNOS


@router.get("/alunos/{idAluno}", response_model=AlunoResponse, status_code=status.HTTP_200_OK)
async def Consultar_Aluno(idAluno: Annotated[int, Path(title="O ID do aluno para a consulta", ge=1)]) -> Any:
      for item in ALUNOS:
        if item["id"] == idAluno:
            return item
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
      

@router.post("/alunos", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
# async def Inserir_Aluno(aluno: str):
async def Inserir_Aluno(aluno: AlunoRequest)-> Any:
  for _aluno in ALUNOS:
        if _aluno["id"] == aluno.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe um aluno com esse ID")
        
  ALUNOS.append(aluno.dict())
 
  return aluno
  

@router.put("/alunos/{idAluno}", response_model=AlunoResponse,  status_code=status.HTTP_200_OK)
async def Atualizar_Aluno(idAluno:int, aluno: AlunoRequest) -> Any:
 for _aluno in ALUNOS:
        if _aluno["id"] == aluno.id:
            _aluno["nome"] = aluno.nome
            _aluno["idade"] = aluno.idade
            _aluno["email"] = aluno.email
            _aluno["senha"] = aluno.senha
            
            return _aluno
 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")


@router.delete("/alunos/{idAluno}", response_model=AlunoResponse, status_code=status.HTTP_200_OK)
async def Deletar_Aluno(idAluno: int) -> Any:
    for index, alnno in enumerate(ALUNOS):
        if alnno["id"] == idAluno:
            return ALUNOS.pop(index)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
