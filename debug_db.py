import json
import os
import sys

try:
    with open('herbal_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("JSON Load Success")
    print("Keys:", list(data.keys()))
    if "remedies" in data:
        print("Remedies keys count:", len(data["remedies"]))
        if "stress" in data["remedies"]:
            print("Stress details:", data["remedies"]["stress"])
        else:
            print("Stress NOT found in remedies")
    else:
        print("Remedies key NOT found")
        
except Exception as e:
    print(f"JSON Load Failed: {e}")

# Check ayurveda_logic loading
try:
    from ayurveda_logic import get_remedy_by_symptom
    print("Function imported")
    res = get_remedy_by_symptom("stress")
    print("Result for 'stress':", res)
except Exception as e:
    print(f"Logic Logic Failed: {e}")
