from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_date = db.Column(db.BigInteger, primary_key=True, default=lambda: int(uuid.uuid1().time / 10))
    event_name = db.Column(db.String, nullable=False)
    event_address = db.Column(db.String, nullable=False)
    event_desc = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Event {self.event_name}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
