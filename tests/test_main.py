from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_data():
    """Test the /query endpoint."""
    response = client.post("/query", json={"query": "test query"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)

# Note: More comprehensive tests would involve mocking the ChromaDB client
# to control the search results and verify the output structure and content
# more thoroughly. This basic test only checks for a successful response
# and the presence of the 'results' key.