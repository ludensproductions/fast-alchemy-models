from datetime import datetime

from dependencies.context.user import UserContext
from dependencies.database import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin
from utils.enums import TypeHistorical

from .active_record import CustomActiveRecordMixin

class FastAlchemyModel(
    UserContext, CustomActiveRecordMixin, SmartQueryMixin, SerializeMixin
):
    """
    An abstract class for common database features.
    """

    __abstract__ = True

    created_by_id = Column(BigInteger, default=None)
    created_at = Column(DateTime, default=func.now())

    updated_at = Column(DateTime, nullable=True)
    updated_by_id = Column(BigInteger, default=None)

    deleted = Column(DateTime, default=None)
    deleted_by_cascade = Column(Boolean, default=False)

    @classmethod
    def create_historical(cls):
        from .simple_history import HistoricalBase

        """
        Creates a historical object if __historical__ is True.
        """
        class_name = f"{cls.__name__}Historical"

        # Define the attributes/methods for the new class
        class_dict = {
            "__tablename__": f"{cls.__tablename__}historical",
            "__historical__": False,
            f"id": Column(BigInteger),
        }

        # Add fields from the original class to the new class
        for column in cls.__table__.columns:

            if column.name != "id":
                class_dict[column.name] = Column(column.type)
            else:
                class_dict[column.name] = Column(Integer)

        main_class = cls.get_main_class()
        # Create a new class dynamically
        return type(class_name, (main_class, HistoricalBase), class_dict)

    def delete(self):
        """
        Soft deletes the current instance by marking it as deleted with a timestamp.
        """
        kwargs = {"updated_at": datetime.utcnow(), "deleted": datetime.utcnow()}
        if self.user:
            kwargs["updated_by_id"] = self.user.id
        item = super().update(**kwargs)
        if self.__historical__:
            self.__historical__.create_historical_record(
                TypeHistorical.DEL, **self.to_dict()
            )
        return item

    @classmethod
    def create(cls, **kwargs):
        """ """
        if cls.user:
            kwargs["updated_by_id"] = cls.user.id
        item = cls().fill(**kwargs).save()
        if cls.__historical__:
            cls.__historical__.create_historical_record(
                TypeHistorical.ADD, **item.to_dict()
            )
        return item

    def update(self, **kwargs):
        """ """
        kwargs["updated_at"] = datetime.utcnow()
        if self.user:
            kwargs["updated_by_id"] = self.user.id
        item = super().update(**kwargs)
        if self.__historical__:
            self.__historical__.create_historical_record(
                TypeHistorical.UPDATE, **item.to_dict()
            )
        return item

    @classmethod
    def all(cls):
        return cls.where(deleted=None).all()

    @classmethod
    def upsert(cls, **kwargs):
        """
        Upserts a record: updates it if it exists, otherwise inserts it.
        """
        instance = cls().where(id=kwargs.get("id"), deleted=None).first()
        if instance:
            return instance.update(**kwargs)
        else:
            return cls().create(**kwargs)

    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Get an existing record or create a new one
        """
        instance = cls().where(id=kwargs.get("id"), deleted=None).first()
        if instance:
            return instance
        else:
            return cls().create(**kwargs)






