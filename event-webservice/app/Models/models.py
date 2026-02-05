from peewee import Model, AutoField, IntegerField, CharField, TextField, BooleanField, ForeignKeyField
from app.DB.database import db


class BaseModel(Model):
    class Meta:
        database = db


class Event(BaseModel):
    ID = AutoField()
    ID_OWNER = IntegerField()
    nume = CharField(max_length=255)
    locatie = CharField(max_length=255)
    descriere = TextField(null=True)
    numarLocuri = IntegerField()

    class Meta:
        table_name = "events"


class EventPacket(BaseModel):
    ID = AutoField()
    nume = CharField(max_length=255)
    descriere = TextField(null=True)
    numarLocuri = IntegerField(null=True)

    class Meta:
        table_name = "event_packets"


class PacketEvent(BaseModel):
    ID = AutoField()
    packet = ForeignKeyField(EventPacket, backref="packet_events", on_delete="CASCADE")
    event = ForeignKeyField(Event, backref="packet_events", on_delete="CASCADE")

    class Meta:
        table_name = "packet_events"
        indexes = (
            (("packet", "event"), True),
        )


class Ticket(BaseModel):
    COD = CharField(primary_key=True, max_length=64)
    event = ForeignKeyField(Event, backref="tickets", null=True, on_delete="SET NULL")
    packet = ForeignKeyField(
    EventPacket, backref="tickets", null=True, on_delete="SET NULL"
)

    valid = BooleanField(default=True)

    class Meta:
        table_name = "tickets"
