from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import MetaData
from sqlalchemy import (
    func,
    Column,
    DateTime,
    )

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)


class TimestampMixin(object):
    @declared_attr
    def created_at(self):
        return Column(DateTime, nullable=False, default=func.now())

    @declared_attr
    def modified_at(self):
        return Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    @property
    def created_at_string(self):
        return self.created_at.strftime("%d/%m/%y %I:%M:%S")

    @property
    def modified_at_string(self):
        return self.modified_at.strftime("%d/%m/%y %I:%M:%S")

