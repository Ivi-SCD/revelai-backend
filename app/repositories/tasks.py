from app.repositories.base import BaseRepository
from app.models.tasks import Tasks
from typing import Optional


class TaskRepository(BaseRepository):
    def __init__(self):
        super().__init__("tasks")

    async def create(self, task: Tasks) -> dict:
        data = task.model_dump()
        if not data.get("id_task"):
            data["id_task"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_task: str) -> Optional[dict]:
        return await self.find_by_id("id_task", id_task)

    async def list_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> list[dict]:
        return await self.find_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )

    async def update_status(self, id_task: str, status: str) -> Optional[dict]:
        return await self.update_one({"id_task": id_task}, {"status": status})

    async def are_all_completed(self, id_cliente: str, id_produto: str) -> bool:
        tasks = await self.list_by_cliente_produto(id_cliente, id_produto)
        if not tasks:
            return False
        return all(t["status"] == "concluida" for t in tasks)

    async def get_progress(self, id_cliente: str, id_produto: str) -> dict:
        tasks = await self.list_by_cliente_produto(id_cliente, id_produto)
        total = len(tasks)
        if total == 0:
            return {"total": 0, "concluidas": 0, "percentual": 0.0}
        concluidas = sum(1 for t in tasks if t["status"] == "concluida")
        return {
            "total": total,
            "concluidas": concluidas,
            "percentual": round((concluidas / total) * 100, 2),
        }
