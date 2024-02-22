from sqlalchemy_mixins.activerecord import ActiveRecordMixin


class CustomActiveRecordMixin(ActiveRecordMixin):
    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
            else:
                raise KeyError("Attribute '{}' doesn't exist".format(name))

        return self

    @classmethod
    def create(cls, **kwargs):
        """Create and persist a new record for the model
        :param kwargs: attributes for the record
        :return: the new model instance
        """
        return cls().fill(**kwargs).save()

    def update(self, **kwargs):
        """Same as :meth:`fill` method but persists changes to database."""
        return self.fill(**kwargs).save()

    def delete(self):
        """Removes the model from the current entity session and mark for deletion."""
        self.session.delete(self)
        self._flush_or_fail()

    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Get an existing record or create a new one
        """
        instance = cls().find(kwargs.get("id"))
        if instance:
            return instance
        else:
            return cls().create(**kwargs)

    @classmethod
    def where_or_fail(cls, **filters):
        """
        Shortcut for smart_query() method with additional check for instance
        Raises a ValueError if no instance are found
        """
        instance = cls.smart_query(filters)

        if instance.first():
            return instance

        raise ValueError(f"No {cls.__name__} found with the given filters: {filters}")

    @classmethod
    def upsert(cls, **kwargs):
        """
        Upserts a record: updates it if it exists, otherwise inserts it.
        """
        instance = cls().find(kwargs.get("id"))
        if instance:
            return instance.update(**kwargs)
        else:
            return cls().create(**kwargs)

    def save(self):
        """Saves the updated model to the current entity db."""
        self.session.add(self)
        self._flush_or_fail()
        return self

    def _flush_or_fail(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
