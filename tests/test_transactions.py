 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction():
    # First login to get token
    login_response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass"
    })
    token = login_response.json()["access_token"]
    
    # Create transaction
    response = client.post("/transactions/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": 100.0,
            "type": "expense",
            "category": "Food",
            "date": "2024-01-01"
        }
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 100.0
    assert response.json()["category"] == "Food"