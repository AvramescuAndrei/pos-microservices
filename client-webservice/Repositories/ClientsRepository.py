from DB.mongo import get_clients_collection


class ClientsRepository:
    def __init__(self):
        self.collection = get_clients_collection()

    def create_client(self, data):
        doc = data.dict()
        doc["tickets"] = []
        self.collection.insert_one(doc)
        return doc

    def get_all_clients(self):
        return list(self.collection.find({}, {"_id": 0}))

    def get_client(self, email: str):
        return self.collection.find_one({"email": email}, {"_id": 0})

    def update_client(self, email: str, payload):
        self.collection.update_one(
            {"email": email},
            {"$set": payload.dict(exclude_none=True)}
        )
        return self.get_client(email)

    def delete_client(self, email: str):
        self.collection.delete_one({"email": email})

    def add_ticket(self, email: str, ticket):
        self.collection.update_one(
            {"email": email},
            {"$push": {"tickets": ticket.dict()}}
        )
