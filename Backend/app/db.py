#db.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Configuración de la conexión a MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
database = client.agriculture_app

# Colecciones de la base de datos
collection_users = database.users
collection_analysis = database.analysis

# Funciones de base de datos
async def get_user_by_id(user_id: str):
    return await collection_users.find_one({"_id": ObjectId(user_id)})

async def create_user(user_data: dict):
    result = await collection_users.insert_one(user_data)
    return str(result.inserted_id)

async def get_user_by_username(username: str):
    return await collection_users.find_one({"username": username})

async def update_user(user_id: str, user_data: dict):
    updated_user = await collection_users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_data}
    )
    if updated_user.modified_count == 1:
        return await collection_users.find_one({"_id": ObjectId(user_id)})
    return None
async def delete_user(user_id: str):
    delete_result = await collection_users.delete_one({"_id": ObjectId(user_id)})
    return delete_result.deleted_count == 1


async def create_analysis(analysis_data: dict):
    result = await collection_analysis.insert_one(analysis_data)
    return str(result.inserted_id)

async def get_analysis_by_id(analysis_id: str):
    return await collection_analysis.find_one({"_id": ObjectId(analysis_id)})

async def get_analyses_by_user_id(user_id: str):
    cursor = collection_analysis.find({"user_id": ObjectId(user_id)})
    return await cursor.to_list(length=100)


async def update_analysis(analysis_id: str, analysis_data: dict):
    updated_analysis = await collection_analysis.update_one(
        {"_id": ObjectId(analysis_id)},
        {"$set": analysis_data}
    )
    if updated_analysis.modified_count == 1:
        return await collection_analysis.find_one({"_id": ObjectId(analysis_id)})
    return None

async def delete_analysis(analysis_id: str):
    delete_result = await collection_analysis.delete_one({"_id": ObjectId(analysis_id)})
    return delete_result.deleted_count == 1

