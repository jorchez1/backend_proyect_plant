#routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import UserModel, AnalysisModel
from db import collection_users, collection_analysis
from bson import ObjectId
from models import PyObjectId
from services import (
    create_user, get_user_by_id, update_user, delete_user, 
    create_analysis, get_analysis_by_id, update_analysis, delete_analysis
)
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/usuarios")
async def create_usuario(user: UserModel):
    user.password = get_password_hash(user.password)
    user_id = await create_user(user)
    return {"id_usuario": user_id}

@router.get("/usuarios", response_model=list[UserModel])
async def get_usuarios(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    users = await collection_users.find().to_list(1000)
    return [UserModel(**user) for user in users]

@router.get("/usuarios/{user_id}", response_model=UserModel)
async def get_user(user_id: str, current_user: UserModel = Depends(get_current_user)):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserModel(**user)

@router.put("/usuarios/{id_usuario}")
async def update_usuario(id_usuario: str, user: UserModel, current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "admin" and str(current_user.id) != id_usuario:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_user = await update_user(id_usuario, user)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/usuarios/{id_usuario}")
async def delete_usuario(id_usuario: str, current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    success = await delete_user(id_usuario)
    if success:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/analisis")
async def create_analisis(analysis: AnalysisModel, current_user: UserModel = Depends(get_current_user)):
    analysis.user_id = current_user.id
    analysis_id = await create_analysis(analysis)
    return {"id_analisis": analysis_id}

@router.get("/analisis")
async def get_analisis(current_user: UserModel = Depends(get_current_user)):
    if current_user.role == "admin":
        analyses = await collection_analysis.find().to_list(1000)
    else:
        analyses = await collection_analysis.find({"user_id": current_user.id}).to_list(1000)
    return analyses

@router.get("/analisis/{id_analisis}")
async def get_analisis_by_id(id_analisis: str, current_user: UserModel = Depends(get_current_user)):
    analysis = await get_analysis_by_id(id_analisis)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if current_user.role != "admin" and str(analysis["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    return analysis

@router.put("/analisis/{id_analisis}")
async def update_analisis(id_analisis: str, analysis: AnalysisModel, current_user: UserModel = Depends(get_current_user)):
    existing_analysis = await get_analysis_by_id(id_analisis)
    if existing_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if current_user.role != "admin" and str(existing_analysis["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_analysis = await update_analysis(id_analisis, analysis)
    if updated_analysis:
        return updated_analysis
    raise HTTPException(status_code=404, detail="Analysis not found")

@router.delete("/analisis/{id_analisis}")
async def delete_analisis(id_analisis: str, current_user: UserModel = Depends(get_current_user)):
    existing_analysis = await get_analysis_by_id(id_analisis)
    if existing_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if current_user.role != "admin" and str(existing_analysis["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    success = await delete_analysis(id_analisis)
    if success:
        return {"detail": "Analysis deleted"}
    raise HTTPException(status_code=404, detail="Analysis not found")