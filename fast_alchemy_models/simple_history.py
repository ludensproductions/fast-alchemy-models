from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .models import FastAlchemyModel
from .enums import TypeHistorical


class HistoricalBase(FastAlchemyModel):
    """
    Enables storing and tracking historical versions of records.
    """

    __abstract__ = True

    history_id = Column(BigInteger, primary_key=True, index=True)
    history_date = Column(DateTime, default=func.now())

    history_change_reason = Column(String, default=None)
    history_type = Column(String, default=TypeHistorical.ADD.value)
    history_user_id = Column(BigInteger)

    @classmethod
    def create_historical_record(cls, action, **kwargs):
        kwargs["history_type"] = action
        if cls.user:
            kwargs["history_user_id"] = cls.user.id
        return cls().fill(**kwargs).save()

    @classmethod
    def all(cls):
        return cls.query.all()
    

class SafeDeleteMeta(type):
    def __init__(cls, name, bases, class_dict):
        super().__init__(name, bases, class_dict)
        if cls.__historical__:
            cls.__historical__ = cls.create_historical()