from server import sqlalchemy_session
from server.errors.exc import FileUnknownId
from server.views import session_handler
from server.file.model import File


class FileRepository:
    @staticmethod
    def get_all():
        return File.query.all()

    @staticmethod
    def get_by_id(id_user, id: int):
        file = File.query.filter_by(id=id, id_user=id_user).first()
        if file is None:
            raise FileUnknownId(id)
        return file

    @staticmethod
    def get_by_task_id(id_user, id_task: int):
        return File.query.filter_by(id=id_task, id_user=id_user).all()

    @staticmethod
    @session_handler
    def insert(id_user, name: str, path: str, id_task: int):
        file = File(id_user=id_user, name=name, path=path, id_task=id_task)
        sqlalchemy_session.add(file)
        return file

    @classmethod
    @session_handler
    def delete(cls, id_user, id: int):
        file = cls.get_by_id(id_user, id)
        sqlalchemy_session.delete(file)
        return file
