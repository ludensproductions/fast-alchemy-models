from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .active_record import ActiveRecordModel
from .enums import TypeHistorical
from .simple_history import HistoricalBase


class SafeDeleteBase(ActiveRecordModel):
    """
    Extends BaseModel to add soft deletion and user tracking features.
    """

    __abstract__ = True

    created_by_id = Column(BigInteger, default=None)
    created_at = Column(DateTime, default=func.now())

    updated_at = Column(DateTime, nullable=True)
    updated_by_id = Column(BigInteger, default=None)

    deleted = Column(DateTime, default=None)
    deleted_by_cascade = Column(Boolean, default=False)

    def delete(self):
        """
        Soft deletes the current instance by marking it as deleted with a timestamp.
        """
        kwargs = {
            "updated_at": datetime.now(timezone.utc),
            "deleted": datetime.now(timezone.utc),
        }
        if self.user:
            kwargs["updated_by_id"] = self.user.id
        return super().update(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """ """
        if cls.user:
            kwargs["updated_by_id"] = cls.user.id
        return cls().fill(**kwargs).save()

    def update(self, **kwargs):
        """ """
        kwargs["updated_at"] = datetime.now(timezone.utc)
        if self.user:
            kwargs["updated_by_id"] = self.user.id
        return super().update(**kwargs)

    @classmethod
    def all(cls):
        return cls.where(deleted=None).all()

    @classmethod
    def upsert(cls, **kwargs):
        """
        Upserts a record: updates it if it exists, otherwise inserts it.
        """
        if instance := cls().where(id=kwargs.get("id"), deleted=None).first():
            return instance.update(**kwargs)
        else:
            return cls().create(**kwargs)

    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Get an existing record or create a new one
        """
        if instance := cls().where(id=kwargs.get("id"), deleted=None).first():
            return instance
        else:
            return cls().create(**kwargs)
