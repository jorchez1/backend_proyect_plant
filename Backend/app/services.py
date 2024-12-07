#services.py
from db import (
    create_user as db_create_user,
    get_user_by_id as db_get_user_by_id,
    update_user as db_update_user,
    delete_user as db_delete_user,
    create_analysis as db_create_analysis,
    get_analysis_by_id as db_get_analysis_by_id,
    update_analysis as db_update_analysis,
    delete_analysis as db_delete_analysis
)
from models import UserModel, AnalysisModel

# Usuarios

async def create_user(user: UserModel):
    user_data = user.dict(by_alias=True)
    return await db_create_user(user_data)

async def get_user_by_id(id_usuario: str):
    return await db_get_user_by_id(id_usuario)

async def update_user(id_usuario: str, user: UserModel):
    user_data = user.dict(by_alias=True)
    return await db_update_user(id_usuario, user_data)

async def delete_user(id_usuario: str):
    return await db_delete_user(id_usuario)


# Análisis

async def create_analysis(analysis: AnalysisModel):
    analysis_data = analysis.dict(by_alias=True)
    return await db_create_analysis(analysis_data)

async def get_analysis_by_id(id_analisis: str):
    return await db_get_analysis_by_id(id_analisis)

async def update_analysis(id_analisis: str, analysis: AnalysisModel):
    analysis_data = analysis.dict(by_alias=True)
    return await db_update_analysis(id_analisis, analysis_data)

async def delete_analysis(id_analisis: str):
    return await db_delete_analysis(id_analisis)
