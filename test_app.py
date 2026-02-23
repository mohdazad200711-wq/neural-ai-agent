
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        print("[PASS] Home Page: OK")
    except Exception as e:
        print(f"[FAIL] Home Page: FAILED ({e})")

def test_dosha_quiz():
    try:
        response = requests.get(f"{BASE_URL}/dosha_test")
        assert response.status_code == 200
        print("[PASS] Dosha Quiz Page: OK")
    except Exception as e:
        print(f"[FAIL] Dosha Quiz Page: FAILED ({e})")

def test_analyze():
    payload = {"answers": ["Vata", "Pitta", "Kapha", "Pitta", "Pitta"]}
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "dominant_dosha" in data
        assert data["dominant_dosha"] == "Pitta"
        print("[PASS] Analyze Endpoint: OK")
    except Exception as e:
        print(f"[FAIL] Analyze Endpoint: FAILED ({e})")

def test_remedy():
    payload = {"symptom": "stress"}
    try:
        response = requests.post(f"{BASE_URL}/get_remedy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert "Ashwagandha" in data["recommendations"]
        print("[PASS] Remedy Endpoint: OK")
    except Exception as e:
        print(f"[FAIL] Remedy Endpoint: FAILED ({e})")

if __name__ == "__main__":
    print("Starting Tests...")
    test_home()
    test_dosha_quiz()
    test_analyze()
    test_remedy()
