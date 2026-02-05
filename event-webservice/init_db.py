from app.DB.database import db
from app.Models.models import Event, EventPacket, PacketEvent, Ticket


def create_tables():
    with db:
        db.create_tables([Event, EventPacket, PacketEvent, Ticket])
    print("Tables created successfully.")


def seed_data():
    with db.atomic():
        if Event.select().count() == 0:
            e1 = Event.create(
                ID_OWNER=1,
                nume="Concert Braila",
                locatie="Braila",
                descriere="Concert rock",
                numarLocuri=10,
            )
            e2 = Event.create(
                ID_OWNER=2,
                nume="Conference Iași",
                locatie="Iași",
                descriere="Tech conf",
                numarLocuri=50,
            )

            p1 = EventPacket.create(
                nume="Pachet Concert+Conf",
                descriere="Acces la ambele",
                numarLocuri=None,
            )

            PacketEvent.create(packet=p1, event=e1)
            PacketEvent.create(packet=p1, event=e2)

    print("Seed data inserted (if DB was empty).")


if __name__ == "__main__":
    create_tables()
    seed_data()
