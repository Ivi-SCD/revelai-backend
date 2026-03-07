from app.core.db.mongo_manager import get_mongo_manager
from typing import Optional
import uuid


class BaseRepository:
    """Base repository with common CRUD operations."""

    def __init__(self, collection_name: str):
        self._collection_name = collection_name
        self._manager = get_mongo_manager()

    @property
    def collection(self):
        return self._manager.get_collection(self._collection_name)

    @staticmethod
    def _generate_id() -> str:
        return str(uuid.uuid4())

    async def find_by_id(self, id_field: str, id_value: str) -> Optional[dict]:
        doc = await self.collection.find_one({id_field: id_value})
        if doc:
            doc.pop("_id", None)
        return doc

    async def find_many(self, query: dict) -> list[dict]:
        cursor = self.collection.find(query)
        results = []
        async for doc in cursor:
            doc.pop("_id", None)
            results.append(doc)
        return results

    async def insert_one(self, data: dict) -> dict:
        await self.collection.insert_one(data)
        data.pop("_id", None)
        return data

    async def update_one(self, query: dict, update: dict) -> Optional[dict]:
        result = await self.collection.find_one_and_update(
            query, {"$set": update}, return_document=True
        )
        if result:
            result.pop("_id", None)
        return result

    async def delete_one(self, query: dict) -> bool:
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
