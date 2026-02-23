
# Ayurveda Logic Module

# Data for Dosha Calculation
# Each question maps answers to (Vata, Pitta, Kapha) points
DOSHA_QUIZ = [
    {
        "question": "How is your body frame?",
        "options": [
            {"text": "Thin, lean, prominent joints", "dosha": "Vata"},
            {"text": "Medium build, good muscle tone", "dosha": "Pitta"},
            {"text": "Large, sturdy, heavy build", "dosha": "Kapha"}
        ]
    },
    {
        "question": "How is your skin?",
        "options": [
            {"text": "Dry, rough, cool to touch", "dosha": "Vata"},
            {"text": "Warm, reddish, prone to acne/freckles", "dosha": "Pitta"},
            {"text": "Thick, oily, cool, pale", "dosha": "Kapha"}
        ]
    },
    {
        "question": "How is your digestion?",
        "options": [
            {"text": "Irregular, gas, bloating", "dosha": "Vata"},
            {"text": "Strong, sharp hunger, heartburn", "dosha": "Pitta"},
            {"text": "Slow, steady, can skip meals easily", "dosha": "Kapha"}
        ]
    },
    {
        "question": "How is your sleep?",
        "options": [
            {"text": "Light, interrupted, trouble falling asleep", "dosha": "Vata"},
            {"text": "Moderate, sound, can wake up easily", "dosha": "Pitta"},
            {"text": "Deep, heavy, hard to wake up", "dosha": "Kapha"}
        ]
    },
    {
        "question": "How is your temperament?",
        "options": [
            {"text": "Energetic, creative, anxious", "dosha": "Vata"},
            {"text": "Focused, ambitious, irritable", "dosha": "Pitta"},
            {"text": "Calm, patient, slow to anger", "dosha": "Kapha"}
        ]
    }
]

# Herbal Remedies Database
HERBAL_REMEDIES = {
    "Vata": {
        "description": "Vata is governed by air and ether. To balance Vata, focus on warming, grounding, and nourishing herbs.",
        "herbs": [
            {"name": "Ashwagandha", "benefit": "Reduces stress and anxiety, improves sleep, and boosts energy."},
            {"name": "Triphala", "benefit": "Supports digestion and elimination, gentle detox."},
            {"name": "Ginger", "benefit": "Warms the body, aids digestion, and reduces gas."},
            {"name": "Licorice Root", "benefit": "Soothing and moisturizing for dry tissues."}
        ],
        "lifestyle_tips": [
            "Stick to a regular daily routine.",
            "Eat warm, cooked, oily foods.",
            "Avoid cold, dry, and raw foods.",
            "Engage in gentle exercise like Yoga or walking."
        ]
    },
    "Pitta": {
        "description": "Pitta is governed by fire and water. To balance Pitta, focus on cooling, calming, and moderating herbs.",
        "herbs": [
            {"name": "Amla (Indian Gooseberry)", "benefit": "Cooling, rich in Vitamin C, supports liver health."},
            {"name": "Brahmi", "benefit": "Cools the mind, improves focus, and reduces anger."},
            {"name": "Neem", "benefit": "Purifies the blood and skin, reduces inflammation."},
            {"name": "Shatavari", "benefit": "Cooling and nourishing for the reproductive system."}
        ],
        "lifestyle_tips": [
            "Avoid excessive heat and sun exposure.",
            "Eat cooling, sweet, and bitter foods.",
            "Avoid spicy, sour, and salty foods.",
            "Practice cooling breathwork (Sheetali Pranayama)."
        ]
    },
    "Kapha": {
        "description": "Kapha is governed by earth and water. To balance Kapha, focus on warming, stimulating, and lightening herbs.",
        "herbs": [
            {"name": "Trikatu (Ginger, Black Pepper, Long Pepper)", "benefit": "Stimulates digestion and metabolism, burns ama (toxins)."},
            {"name": "Turmeric", "benefit": "Anti-inflammatory, warming, and immune-boosting."},
            {"name": "Tulsi (Holy Basil)", "benefit": "Supports respiratory health and reduces congestion."},
            {"name": "Guggul", "benefit": "Supports healthy weight management and cholesterol levels."}
        ],
        "lifestyle_tips": [
            "Engage in vigorous exercise daily.",
            "Eat warm, light, and spicy foods.",
            "Avoid heavy, oily, and sweet foods.",
            "Wake up early (before 6 AM)."
        ]
    }
}

def analyze_dosha(answers):
    """
    Analyzes user answers to determine the dominant Dosha.
    answers: List of selected options (e.g., ["Vata", "Pitta", "Vata", ...])
    """
    counts = {"Vata": 0, "Pitta": 0, "Kapha": 0}
    
    for answer in answers:
        if answer in counts:
            counts[answer] += 1
            
    # Find the Dosha with the maximum count
    dominant_dosha = max(counts, key=counts.get)
    
    return {
        "dominant_dosha": dominant_dosha,
        "counts": counts,
        "details": HERBAL_REMEDIES[dominant_dosha]
    }

# Digestive Health
# Load Knowledge Base from JSON
import json
import os

def load_knowledge_base():
    """
    Loads the herbal database from a JSON file.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'herbal_database.json')
    
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading database: {e}")
        # Fallback to empty/basic structure if file missing
        return {
            "remedies": {"cold": ["Tulsi"], "headache": ["Ginger"]},
            "general_advice": {"default": "Drink warm water."},
            "tips": ["Ayurveda is ancient wisdom."]
        }

KB = load_knowledge_base()
db_en = KB.get("remedies", {})
db_hi = KB.get("remedies_hi", {})
GENERAL_ADVICE_EN = KB.get("general_advice", {})
GENERAL_ADVICE_HI = KB.get("general_advice_hi", {})
TIPS_EN = KB.get("tips", [])
TIPS_HI = KB.get("tips_hi", [])
SYMPTOM_MAP_HI = KB.get("symptom_map_hi", {})

import random

def get_random_tip(lang='en'):
    tips = TIPS_HI if lang == 'hi' else TIPS_EN
    if not tips:
        return "Nature heals." if lang == 'en' else "प्रकृति ही उपचार है।"
    return random.choice(tips)

def get_remedy_by_symptom(symptom, lang='en', verified=False):
    """
    Enhanced keyword matching supporting English and Hindi.
    Restricts certain medical advice if not verified.
    """
    symptom = symptom.lower()
    recommendations = set()
    
    # Gate sensitive topics
    sensitive_topics = ["cancer", "covid", "diabetes", "blood pressure", "heart"]
    is_sensitive = any(topic in symptom for topic in sensitive_topics)
    
    if is_sensitive and not verified:
        return ["VERIFICATION_REQUIRED"]

    # Select appropriate database
    current_db = db_hi if lang == 'hi' else db_en
    
    # Logic for Hindi Input mapping to English keys (since keys are shared/mapped)
    # If lang is Hindi, we first check if the input matches any known Hindi symptom keywords
    # and map them to our internal standard keys (mostly English based in JSON structure keys)
    # BUT wait, the JSON structure for remedies_hi uses SAME KEYS as remedies ("digestion", "cold")
    # So we need to map Hindi INPUT -> English KEY -> Hindi VALUE.
    
    target_keys = set()
    
    if lang == 'hi':
        # Check against symptom map
        for hi_word, en_key in SYMPTOM_MAP_HI.items():
            if hi_word in symptom:
                target_keys.add(en_key)
    else:
        # English: Direct match with English keys
        # Checking against the keys of the DB
        for key in db_en.keys():
            if key in symptom:
                target_keys.add(key)
                
    # If we found target keys via mapping or direct match
    if target_keys:
        for key in target_keys:
            if key in current_db:
                recommendations.update(current_db[key])
                
    # If verified and searching for cooling, add advanced therapy
    if verified and "cooling" in target_keys:
        recommendations.add("Shirodhara (Verified Advantage)")
    elif verified and lang == 'en' and "cooling" in symptom:
        recommendations.add("Shirodhara (Verified Advantage)")

    return list(recommendations)

def get_chat_response(message, lang='en'):
    """
    Multilingual rule-based chatbot logic.
    """
    message = message.lower()
    response_parts = []
    
    # Helpers for language
    is_hi = (lang == 'hi')
    advice_db = GENERAL_ADVICE_HI if is_hi else GENERAL_ADVICE_EN
    
    # Greetings
    greetings_en = ["hello", "hi", "hey"]
    greetings_hi = ["namaste", "hello", "hi", "kaise ho", "pranam"]
    
    if any(w in message for w in (greetings_hi if is_hi else greetings_en)):
        # Scale awareness
        count = get_remedy_count()
        welcome = f"नमस्ते! मैं आयुरबॉट हूँ। मेरे ज्ञानकोष में हमारे पास {count}+ आयुर्वेदिक उपचार हैं। {get_random_tip('hi')}" if is_hi else f"Namaste! I am AyurBot. I have access to a vast database of {count}+ Ayurvedic remedies. {get_random_tip('en')}"
        response_parts.append(welcome)

    # Dosha Inquiry
    if "dosha" in message or (is_hi and "दोष" in message):
        msg = "अपना दोष जानने के लिए, कृपया मुख्य मेनू में 'दोष प्रश्नोत्तरी' लें।" if is_hi else "To find your Dosha, please take our Dosha Quiz in the main menu."
        response_parts.append(msg)

    # Check for symptoms
    remedies = get_remedy_by_symptom(message, lang)
    if remedies:
        if is_hi:
            response_parts.append(f"आपके लक्षणों के लिए, आयुर्वेद सुझाव देता है: {', '.join(remedies)}।")
        else:
            response_parts.append(f"For your symptoms, Ayurveda recommends: {', '.join(remedies)}.")
        
        # General Advice Context
        # We need to detect context to give specific general advice
        # Using English keys to look up advice since GENERAL_ADVICE db uses English keys
        # We need to know WHICH key was matched. 
        # For simplicity, we'll re-check keywords or mapped keys
        
        found_key = None
        if is_hi:
            for hi_word, en_key in SYMPTOM_MAP_HI.items():
                if hi_word in message:
                    found_key = en_key
                    break
        else:
            for key in advice_db.keys():
                if key in message:
                    found_key = key
                    break
                    
        if found_key and found_key in advice_db:
             response_parts.append(advice_db[found_key])
            
    # Gratitude
    if "thank" in message or (is_hi and ("dhanyavad" in message or "shukriya" in message or "धन्यवाद" in message)):
        msg = "आपका स्वागत है! आपका स्वास्थ्य अच्छा रहे।" if is_hi else "You're welcome! May you have good health."
        response_parts.append(msg)

    # Fallback
    if not response_parts:
        if is_hi:
            return f"मैं सुन रहा हूँ। कृपया अपनी समस्या बताएं (जैसे, 'सिर दर्द', 'गैस')। टिप: {advice_db['default']}"
        else:
            return f"I am listening. Tell me your problem (e.g., 'hair fall', 'gas'). Tip: {advice_db['default']}"
            
    return " ".join(response_parts)
        

def get_ai_call_script(username="Seeker", country="your region"):
    """
    Generates a personalized AI confirmation call script.
    """
    return [
        f"Namaste, {username}! I am AyurBot, your personal Ayurvedic AI.",
        f"I see you are joining us from {country}. Our database has been optimized for your regional seasonal cycles.",
        "I have now unlocked your access to advanced Cooling remedies and personalized help.",
        "Your legal documents have been verified, and your profile is now 100% complete.",
        "May you find perfect balance. Goodbye!",
    ]

def get_remedy_count():
    """Returns the total number of unique remedies across all categories."""
    all_remedies = set()
    # Assuming 'remedies' in KB refers to the English remedies (db_en)
    # If you want to count unique remedies from both English and Hindi,
    # you would need a more sophisticated mapping or iterate over both db_en and db_hi
    # and potentially normalize names. For now, we'll use db_en as per the instruction's
    # implied structure (database.get('remedies', {}))
    for category in KB.get('remedies', {}).values():
        for remedy in category:
            # Ensure remedy is a string before applying string methods
            if isinstance(remedy, str):
                cleaned_remedy = remedy.replace('(Verified Advantage)', '').strip()
                if cleaned_remedy: # Only add if not empty after cleaning
                    all_remedies.add(cleaned_remedy)
            else:
                all_remedies.add(remedy) # Add non-string remedies directly
    return len(all_remedies)
