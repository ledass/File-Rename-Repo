import os
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "Rename")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "users")

if not MONGO_URI:
    print("❌ MONGO_URI is missing")
    exit(1)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)  
db = client[DB_NAME]  
collection = db[COLLECTION_NAME]

async def save_user(m):
    if not await collection.find_one({"id": m.from_user.id}):
        await collection.insert_one({"name": m.from_user.mention, "id": m.from_user.id})
  
async def save_thumb(m):
    try:
        await collection.update_one(
            {"id": m.from_user.id},
            {
                "$set": {
                    "name": m.from_user.mention,
                    "thumb": m.photo.file_id
                }
            },
            upsert=True  
        )
        return "saved"
    except Exception as e:
        print(f"Error in save_thumb: {e}")
        return "error"

async def save_caption(id, caption):
    try:
        await collection.update_one(
            {"id": id},
            {
                "$set": {                    
                    "caption": caption 
                }
            },
            upsert=True  
        )
        return "saved"
    except Exception as e:
        print(f"Error in save_caption: {e}")
        return "error"

async def set_channel(m, id):
    try:
        await collection.update_one(
            {"id": m},
            {
                "$set": {
                    "channel": id
                }
            },
            upsert=True  
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

async def get_channel(m):
    t = await collection.find_one({"id": m})
    if t and t.get("channel"):
        return t.get("channel")
    return None 

async def del_channel(m):
    t = await collection.find_one({"id": m})
    if t and t.get("channel"):
        await collection.update_one(
            {"id": m},
            {
                "$set": {
                    "channel": None
                }
            },
            upsert=True  
        )
        return True
    return False 

async def get_thumb(m):
    t = await collection.find_one({"id": m})
    if t and t.get("thumb"):
        return t.get("thumb")
    return None 

async def get_caption(m):
    t = await collection.find_one({"id": m})
    if t and t.get("caption"): 
        return t.get("caption")
    return None 

async def set_metadata(id, metadata):
    try:
        await collection.update_one(
            {"id": id},
            {
                "$set": {                    
                    "metadata": metadata 
                }
            },
            upsert=True  
        )
        return "saved"
    except Exception as e:
        print(f"Error in set_metadata: {e}")
        return "error"

async def set_autorename(id, bool, mode):
    try:
        await collection.update_one(
            {"id": id},
            {
                "$set": {                    
                    "autorename": bool,
                    "mode": mode
                }
            },
            upsert=True  
        )
        return "saved"
    except Exception as e:
        print(f"Error in set_autorename: {e}")
        return "error"

async def get_autorename(m):
    t = await collection.find_one({"id": m})
    if t and t.get("autorename"): 
        return t.get("autorename")
    return None 

async def get_autorename_mode(m):
    t = await collection.find_one({"id": m})
    if t and t.get("mode"): 
        return t.get("mode")
    return "error"

async def del_filename(m):
    t = await collection.find_one({"id": m})
    if t and t.get("metadata"):
        await collection.update_one(
            {"id": m},
            {
                "$set": {
                    "filename": None
                }
            },
            upsert=True  
        )
        return True
    return False 

async def get_metadata(m):
    t = await collection.find_one({"id": m})
    if t and t.get("metadata"): 
        return t.get("metadata")
    return None 

async def del_metadata(m):
    t = await collection.find_one({"id": m})
    if t and t.get("metadata"):
        await collection.update_one(
            {"id": m},
            {
                "$set": {
                    "metadata": None
                }
            },
            upsert=True  
        )
        return True
    return False 

async def del_caption(m):
    t = await collection.find_one({"id": m})
    if t and t.get("caption"):
        await collection.update_one(
            {"id": m},
            {
                "$set": {
                    "caption": None
                }
            },
            upsert=True  
        )
        return True
    return False 

async def del_thumb(m):
    t = await collection.find_one({"id": m})
    if t and t.get("thumb"):
        await collection.update_one(
            {"id": m},
            {
                "$set": {
                    "thumb": None
                }
            },
            upsert=True  
        )
        return True
    return False 
