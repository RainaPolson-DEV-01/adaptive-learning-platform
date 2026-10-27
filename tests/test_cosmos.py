from backend.services.cosmos_service import container

item = {
    "id": "1001",
    "userId": "1001",
    "name": "Test User"
}

container.upsert_item(item)

print("Cosmos connection successful")
