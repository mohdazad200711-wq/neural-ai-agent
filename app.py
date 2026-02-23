
from flask import Flask, render_template, request, jsonify, session
from ayurveda_logic import DOSHA_QUIZ, analyze_dosha, get_remedy_by_symptom

app = Flask(__name__)
app.secret_key = 'ayuraisecret' # For session management

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dosha_test')
def dosha_test():
    return render_template('dosha_test.html', questions=DOSHA_QUIZ)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Expecting JSON data from the frontend
    data = request.json
    answers = data.get('answers', [])
    
    if not answers:
        return jsonify({"error": "No answers provided"}), 400
        
    result = analyze_dosha(answers)
    return jsonify(result)

@app.route('/remedy')
def remedy():
    return render_template('remedies.html')

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

@app.route('/chat')
def chat():
    from ayurveda_logic import get_random_tip
    return render_template('chat.html', tip=get_random_tip())

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    message = data.get('message', '')
    lang = data.get('lang', 'en')
    if not message:
        return jsonify({"response": "I didn't hear you."})
    
    # Import here to avoid circular imports if any, or just use the imported function
    from ayurveda_logic import get_chat_response
    response = get_chat_response(message, lang)
    return jsonify({"response": response})

@app.route('/get_remedy', methods=['POST'])
def get_remedy():
    data = request.json
    symptom = data.get('symptom', '')
    
    if not symptom:
        return jsonify({"error": "No symptom provided"}), 400
        
    user = session.get('user', {})
    is_verified = user.get('verified', False)
        
    recommendations = get_remedy_by_symptom(symptom, verified=is_verified)
    return jsonify({"recommendations": recommendations, "verified": is_verified})

@app.route('/api/verify_proof', methods=['POST'])
def verify_proof():
    # Simulate legal proof verification
    data = request.json
    proof_type = data.get('proof_type', 'ID Card')
    
    if 'user' in session:
        session['user']['verified'] = True
        return jsonify({"status": "success", "message": f"{proof_type} verified! You now have full access to medical recommendations."})
    
    return jsonify({"error": "User not registered"}), 400

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        # Mock registration logic
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        country = data.get('country', 'Not Specified')
        
        # Store in session for this demo
        session['user'] = {'username': username, 'verified': False, 'country': country}
        
        return jsonify({"status": "success", "message": f"Welcome, {username} from {country}! Registration complete."})
    return render_template('register.html')

@app.route('/api/ai_call_script')
def api_ai_call_script():
    user = session.get('user', {})
    username = user.get('username', 'Seeker')
    country = user.get('country', 'your region')
    
    from ayurveda_logic import get_ai_call_script
    script = get_ai_call_script(username, country)
    return jsonify({"script": script})

@app.route('/get_remedy_count')
def get_remedy_count_route():
    from ayurveda_logic import get_remedy_count
    count = get_remedy_count()
    return jsonify({"count": count})

if __name__ == '__main__':
    app.run(debug=True)
