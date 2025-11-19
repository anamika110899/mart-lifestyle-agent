
from sqlmodel import Session, select
from db import engine
from models.task import Task

class TaskRepo:
    def add(self, description: str):
        with Session(engine) as session:
            task = Task(description=description)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def list_all(self):
        with Session(engine) as session:
            tasks = session.exec(select(Task)).all()
            return [
                {"id": t.id, "description": t.description, "is_done": t.is_done}
                for t in tasks
            ]

    def exists(self, description: str) -> bool:
        with Session(engine) as session:
            stmt = select(Task).where(Task.description == description)
            return session.exec(stmt).first() is not None

    def mark_done(self, task_id: int):
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                return False
            task.is_done = True
            session.add(task)
            session.commit()
            return True
