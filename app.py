from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
# Secret key is used by Flask to keep session data safe
app.secret_key = 'opes-edge-eec2026-logic-legends-secret'

# Path to the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def get_db():
    """Opens a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


# ============================
# PUBLIC ROUTES
# ============================

@app.route('/')
def index():
    """Home page — the premium landing page."""
    return render_template('index.html')


@app.route('/agriculture')
def agriculture():
    """Agriculture module placeholder."""
    return render_template('agriculture/index.html')


@app.route('/education')
def education():
    """Education module placeholder."""
    return render_template('education/index.html')


@app.route('/healthcare')
def healthcare():
    """Healthcare module placeholder."""
    """Healthcare module - main hub."""
    return render_template('healthcare/index.html')


@app.route('/community')
def community():
    """Community Services module placeholder."""
    """Community Services — main hub."""
    return render_template('community/index.html')


@app.route('/energy')
def energy():
    """Energy Management module placeholder."""
    return render_template('energy/index.html')


@app.route('/water')
def water():
    """Water Management module placeholder."""
    return render_template('water/index.html')


@app.route('/about')
def about():
    """About page — scrolls to about section on home for now."""
    return render_template('index.html', scroll_to='about')


# ============================
# AUTHENTICATION ROUTES
# ============================

@app.route('/login')
def login():
    """Login page placeholder."""
    return render_template('login.html')


@app.route('/register')
def register():
    """Registration page placeholder."""
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard placeholder."""
    return render_template('dashboard.html')

# ============================================================
# AGRICULTURE ROUTES
# ============================================================

# @app.route('/agriculture')
# def agriculture():
#     """Agriculture module placeholder."""
#     return render_template('agriculture/index.html')

@app.route('/agriculture/profile', methods=['GET', 'POST'])
def farmer_profile():
    conn = get_db()
    profile = conn.execute('SELECT * FROM farmer_profiles ORDER BY id DESC LIMIT 1').fetchone()

    if request.method == 'POST':
        name = request.form.get('farmer_name', '').strip()
        experience = request.form.get('experience_years', '').strip()
        location = request.form.get('location', '').strip()
        language = request.form.get('preferred_language', 'English')

        if not name or not location:
            flash('Farmer name and location are required.', 'danger')
            conn.close()
            return redirect(url_for('farmer_profile'))

        if profile:
            conn.execute('''UPDATE farmer_profiles 
                         SET farmer_name=?, experience_years=?, location=?, preferred_language=? 
                         WHERE id=?''', (name, experience, location, language, profile['id']))
            flash('Profile updated successfully!', 'success')
        else:
            conn.execute('''INSERT INTO farmer_profiles 
                         (farmer_name, experience_years, location, preferred_language) 
                         VALUES (?, ?, ?, ?)''', (name, experience, location, language))
            flash('Profile created successfully!', 'success')

        conn.commit()
        conn.close()
        return redirect(url_for('farmer_profile'))

    conn.close()
    return render_template('agriculture/profile.html', profile=profile)

@app.route('/agriculture/crops')
def crops():
    conn = get_db()
    crops = conn.execute('SELECT * FROM crops ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('agriculture/crops.html', crops=crops)

@app.route('/agriculture/crops/add', methods=['GET', 'POST'])
def add_crop():
    if request.method == 'POST':
        crop_name = request.form.get('crop_name', '').strip()
        category = request.form.get('crop_category', '')
        sowing = request.form.get('sowing_date', '')
        harvest = request.form.get('expected_harvest_date', '')
        area = request.form.get('area', '')
        soil = request.form.get('soil_type', '')
        location = request.form.get('location', '').strip()

        if not crop_name or not category:
            flash('Crop name and category are required.', 'danger')
            return redirect(url_for('add_crop'))

        conn = get_db()
        conn.execute('''INSERT INTO crops 
                     (crop_name, crop_category, sowing_date, expected_harvest_date, area, soil_type, location)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (crop_name, category, sowing, harvest, area, soil, location))
        conn.commit()
        conn.close()
        flash('Crop added successfully!', 'success')
        return redirect(url_for('crops'))

    return render_template('agriculture/crop_form.html', crop=None, edit=False)

@app.route('/agriculture/crops/edit/<int:id>', methods=['GET', 'POST'])
def edit_crop(id):
    conn = get_db()
    crop = conn.execute('SELECT * FROM crops WHERE id = ?', (id,)).fetchone()

    if not crop:
        conn.close()
        flash('Crop not found.', 'danger')
        return redirect(url_for('crops'))

    if request.method == 'POST':
        crop_name = request.form.get('crop_name', '').strip()
        category = request.form.get('crop_category', '')
        sowing = request.form.get('sowing_date', '')
        harvest = request.form.get('expected_harvest_date', '')
        area = request.form.get('area', '')
        soil = request.form.get('soil_type', '')
        location = request.form.get('location', '').strip()

        conn.execute('''UPDATE crops SET crop_name=?, crop_category=?, sowing_date=?, 
                     expected_harvest_date=?, area=?, soil_type=?, location=? WHERE id=?''',
                     (crop_name, category, sowing, harvest, area, soil, location, id))
        conn.commit()
        conn.close()
        flash('Crop updated successfully!', 'success')
        return redirect(url_for('crops'))

    conn.close()
    return render_template('agriculture/crop_form.html', crop=crop, edit=True)

@app.route('/agriculture/crops/delete/<int:id>', methods=['POST'])
def delete_crop(id):
    conn = get_db()
    conn.execute('DELETE FROM crops WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Crop deleted successfully.', 'success')
    return redirect(url_for('crops'))

@app.route('/agriculture/crop/<int:id>')
def crop_detail(id):
    conn = get_db()
    crop = conn.execute('SELECT * FROM crops WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not crop:
        flash('Crop not found.', 'danger')
        return redirect(url_for('crops'))
    return render_template('agriculture/crop_detail.html', crop=crop)

@app.route('/agriculture/soil')
def soil():
    return render_template('agriculture/soil.html')

@app.route('/agriculture/health', methods=['GET', 'POST'])
def crop_health():
    guidance = None
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        notes = request.form.get('notes', '').strip()
        guidance = generate_health_guidance(symptoms, notes)
    return render_template('agriculture/health.html', guidance=guidance)

@app.route('/agriculture/weather')
def weather():
    return render_template('agriculture/weather.html')

@app.route('/agriculture/market')
def market():
    return render_template('agriculture/market.html')

@app.route('/agriculture/resources')
def resources():
    return render_template('agriculture/resources.html')

@app.route('/agriculture/assistant', methods=['GET', 'POST'])
def assistant():
    response = None
    question = ''
    if request.method == 'POST':
        question = request.form.get('question', '').strip().lower()
        response = get_assistant_response(question)
    return render_template('agriculture/assistant.html', response=response, question=question)

# ============================================================
# PHASE 3 — EDUCATION ROUTES
# ============================================================

# @app.route('/education')
# def education():
#     return render_template('education/index.html')

@app.route('/education/dashboard')
def education_dashboard():
    conn = get_db()
    courses = conn.execute('SELECT * FROM courses LIMIT 4').fetchall()
    resources = conn.execute('SELECT * FROM education_resources LIMIT 4').fetchall()
    conn.close()
    return render_template('education/dashboard.html', courses=courses, resources=resources)

@app.route('/education/profile', methods=['GET', 'POST'])
def education_profile():
    conn = get_db()
    profile = conn.execute('SELECT * FROM student_profiles ORDER BY id DESC LIMIT 1').fetchone()

    if request.method == 'POST':
        name = request.form.get('student_name', '').strip()
        college = request.form.get('college', '').strip()
        course = request.form.get('course', '').strip()
        branch = request.form.get('branch', '').strip()
        semester = request.form.get('semester', '').strip()
        skills = request.form.get('skills', '').strip()
        interests = request.form.get('interests', '').strip()
        career_goal = request.form.get('career_goal', '').strip()

        if not name:
            flash('Student name is required.', 'danger')
            conn.close()
            return redirect(url_for('education_profile'))

        if profile:
            conn.execute('''UPDATE student_profiles 
                         SET student_name=?, college=?, course=?, branch=?, semester=?, skills=?, interests=?, career_goal=? 
                         WHERE id=?''',
                         (name, college, course, branch, semester, skills, interests, career_goal, profile['id']))
            flash('Profile updated successfully!', 'success')
        else:
            conn.execute('''INSERT INTO student_profiles 
                         (student_name, college, course, branch, semester, skills, interests, career_goal)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                         (name, college, course, branch, semester, skills, interests, career_goal))
            flash('Profile created successfully!', 'success')

        conn.commit()
        conn.close()
        return redirect(url_for('education_profile'))

    conn.close()
    return render_template('education/profile.html', profile=profile)

@app.route('/education/resources')
def education_resources():
    # conn = get_db()
    # resources = conn.execute('SELECT * FROM education_resources ORDER BY created_at DESC').fetchall()
    # conn.close()
    # return render_template('education/resources.html', resources=resources)
    return render_template('education/resources.html')
@app.route('/education/courses')
def education_courses():
    conn = get_db()
    courses = conn.execute('SELECT * FROM courses ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('education/courses.html', courses=courses)

@app.route('/education/materials')
def education_materials():
    conn = get_db()
    materials = conn.execute('SELECT * FROM study_materials ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('education/materials.html', materials=materials)

@app.route('/education/exams')
def education_exams():
    return render_template('education/exams.html')

@app.route('/education/coding')
def education_coding():
    # conn = get_db()
    # challenges = conn.execute('SELECT * FROM coding_challenges ORDER BY created_at DESC').fetchall()
    # conn.close()
    # return render_template('education/coding.html', challenges=challenges)
    return render_template('education/coding.html')

# @app.route('/education/scholarships')
# def education_scholarships():
#     conn = get_db()
#     scholarships = conn.execute('SELECT * FROM scholarships ORDER BY created_at DESC').fetchall()
#     conn.close()
#     return render_template('education/scholarships.html', scholarships=scholarships)
@app.route('/education/scholarships')
def education_scholarships():
    # Static/demo approach — no database dependency
    return render_template('education/scholarships.html')

@app.route('/education/career')
def education_career():
    conn = get_db()
    careers = conn.execute('SELECT * FROM career_paths ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('education/career.html', careers=careers)

@app.route('/education/opportunities')
def education_opportunities():
    conn = get_db()
    opportunities = conn.execute('SELECT * FROM opportunities ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('education/opportunities.html', opportunities=opportunities)

# education assistance
@app.route('/education/assistant', methods=['GET', 'POST'])
def education_assistant():
    response = None
    question = ''
    if request.method == 'POST':
        question = request.form.get('question', '').strip().lower()
        response = get_education_response(question)
    return render_template('education/assistant.html', response=response, question=question)

# healthcare assistance
@app.route('/healthcare/assistant', methods=['GET', 'POST'])
def healthcare_assistant():
    response = None
    question = ''
    if request.method == 'POST':
        question = request.form.get('question', '').strip().lower()
        response = get_healthcare_response(question)
    return render_template('healthcare/index.html', health_response=response, health_question=question)

#Energy roots
# @app.route('/energy')
# def energy():
#     """Energy Management — main hub."""
#     return render_template('energy/index.html')

@app.route('/energy/consumption')
def energy_consumption():
    """Energy consumption tracking and calculator."""
    return render_template('energy/consumption.html')

@app.route('/energy/efficiency')
def energy_efficiency():
    """Energy efficiency tips and guides."""
    return render_template('energy/efficiency.html')

@app.route('/energy/renewable')
def energy_renewable():
    """Renewable energy information."""
    return render_template('energy/renewable.html')

@app.route('/energy/conservation')
def energy_conservation():
    """Energy conservation practices."""
    return render_template('energy/conservation.html')

@app.route('/energy/resources')
def energy_resources():
    """Energy resources and external links."""
    return render_template('energy/resources.html')

@app.route('/energy/assistant', methods=['GET', 'POST'])
def energy_assistant():
    response = None
    question = ''
    if request.method == 'POST':
        question = request.form.get('question', '').strip().lower()
        response = get_energy_response(question)
    return render_template('energy/index.html', energy_response=response, energy_question=question)
# ============================================================
# HELPERS
# ============================================================

def generate_health_guidance(symptoms, notes):
    tips = []
    if 'yellow_leaves' in symptoms:
        tips.append("Yellow leaves often indicate nitrogen deficiency or overwatering. Check soil moisture and consider organic compost.")
    if 'leaf_spots' in symptoms:
        tips.append("Leaf spots may be fungal. Ensure proper spacing for airflow and avoid wetting leaves during irrigation.")
    if 'wilting' in symptoms:
        tips.append("Wilting can mean root damage or underwatering. Check soil moisture 2 inches deep before watering.")
    if 'pest_damage' in symptoms:
        tips.append("For pest damage, inspect the underside of leaves. Neem oil spray can help as an organic first step.")
    if 'slow_growth' in symptoms:
        tips.append("Slow growth may be due to poor soil nutrition or compacted soil. Consider soil testing and light tilling.")
    if not tips:
        tips.append("Please select symptoms or describe the problem for guidance. For serious issues, consult a local agricultural expert.")
    return tips

def get_assistant_response(question):
    responses = {
        'suitable': "For Kharif season, rice, maize, cotton, and soybean are commonly suitable. For Rabi, wheat, barley, and mustard work well. Always match with your soil type and local rainfall.",
        'soil': "To improve soil health: add organic compost, practice crop rotation, maintain pH between 6.0-7.5, and avoid over-tilling. Test soil annually.",
        'water': "Water early morning or evening. Use drip irrigation if possible. Mulch around plants to reduce evaporation by up to 50%.",
        'yellow': "Yellow leaves usually mean nitrogen deficiency or overwatering. Check drainage and apply nitrogen-rich organic manure.",
        'pest': "Use integrated pest management: neem oil, beneficial insects, pheromone traps, and crop rotation. Avoid broad pesticides that kill pollinators.",
        'fertilizer': "Organic options: vermicompost, green manure, bone meal. Chemical NPK should match soil test results. Never over-fertilize.",
        'harvest': "Harvest timing depends on the crop. Most grains are ready when stalks turn golden and moisture drops to 14-20%.",
        'organic': "Organic farming avoids synthetic chemicals. Focus on compost, bio-pesticides, crop rotation, and companion planting.",
    }
    for key, resp in responses.items():
        if key in question:
            return resp
    return "That's a great farming question. While our AI assistant is in training, we recommend consulting your local Krishi Vigyan Kendra (KVK) or agricultural extension officer for expert advice tailored to your region."

def get_education_response(question):
    responses = {
        'ai': "For AI, start with Python, linear algebra, and statistics. Then learn machine learning (scikit-learn), deep learning (TensorFlow/PyTorch), and work on projects. Free resources: fast.ai, Andrew Ng's courses, and Kaggle Learn.",
        'exam': "For exam prep: create a study schedule, solve previous papers, focus on weak topics first, use active recall, and teach concepts to others. The Pomodoro technique (25 min study + 5 min break) works well.",
        'language': "Python is best for beginners due to simple syntax. For systems programming, learn C/C++. For web, JavaScript is essential. For mobile, Kotlin or Swift. Start with one language and build projects.",
        'data science': "Data Science requires: Python/R, SQL, statistics, machine learning, and visualization (matplotlib, Tableau). Practice on Kaggle datasets. Build a portfolio with 3-4 end-to-end projects.",
        'web': "For web development: learn HTML/CSS/JavaScript first. Then pick a backend (Flask/Django/Node.js) and a frontend framework (React/Vue). Build a full-stack project for your portfolio.",
        'career': "Tech careers in demand: AI Engineer, Data Scientist, Software Developer, Cloud Engineer, Cybersecurity Analyst. Focus on fundamentals + projects + communication skills.",
        'scholarship': "Look for PMSSS, INSPIRE, KVPY, and state government scholarships. Maintain good academic scores and apply early. Check National Scholarship Portal for updates.",
        'skill': "Essential skills: problem solving, programming, communication, teamwork, and adaptability. Soft skills matter as much as technical skills in interviews.",
    }
    for key, resp in responses.items():
        if key in question:
            return resp
    return "Great question! Our Education Assistant is learning every day. For detailed guidance, explore our Courses and Resources sections, or consult your college career counselor."

# healthcare assistance responces
def get_healthcare_response(question):

    responses = {
        'fever': "Fever is usually a sign your body is fighting infection. Rest, stay hydrated, and monitor temperature. If fever exceeds 103°F (39.4°C) or lasts more than 3 days, consult a doctor immediately.",
        'cough': "For common cold and cough: rest, drink warm fluids, use saline nasal drops, and consider steam inhalation. If symptoms worsen or breathing becomes difficult, seek medical care.",
        'cold': "For common cold and cough: rest, drink warm fluids, use saline nasal drops, and consider steam inhalation. If symptoms worsen or breathing becomes difficult, seek medical care.",
        'headache': "Tension headaches can often be relieved with rest, hydration, and reducing screen time. For severe, sudden, or recurring headaches, consult a healthcare professional.",
        'stomach': "For mild stomach issues: eat bland foods (BRAT diet), stay hydrated with ORS, and avoid spicy food. Persistent pain, vomiting, or blood in stool requires immediate medical attention.",
        'diabetes': "Manage diabetes with regular blood sugar monitoring, balanced meals, and prescribed medication. Consult your doctor before making any changes to your treatment plan.",
        'bp': "Monitor blood pressure regularly. Reduce salt intake, exercise moderately, and take prescribed medicines. Consult your doctor if readings are consistently high or low.",
        'blood pressure': "Monitor blood pressure regularly. Reduce salt intake, exercise moderately, and take prescribed medicines. Consult your doctor if readings are consistently high or low.",
        'nutrition': "A balanced diet includes fruits, vegetables, whole grains, protein, and healthy fats. Drink 8-10 glasses of water daily. Limit processed foods and added sugar.",
        'diet': "A balanced diet includes fruits, vegetables, whole grains, protein, and healthy fats. Drink 8-10 glasses of water daily. Limit processed foods and added sugar.",
        'exercise': "Aim for 150 minutes of moderate exercise per week. Include walking, stretching, and strength training. Start slow and consult a doctor if you have existing health conditions.",
        'mental': "Mental health matters. Practice mindfulness, maintain social connections, sleep well, and seek professional help if you feel overwhelmed. Kiran Helpline: 1800-599-0019.",
        'stress': "Manage stress with deep breathing, regular exercise, adequate sleep, and talking to someone you trust. Persistent anxiety may need professional support.",
        'vaccination': "Stay up-to-date with vaccinations. Children should follow the Universal Immunization Program schedule. Adults should get annual flu shots and recommended boosters.",
        'vaccine': "Stay up-to-date with vaccinations. Children should follow the Universal Immunization Program schedule. Adults should get annual flu shots and recommended boosters.",
        'pregnancy': "Regular prenatal checkups are essential. Take folic acid, eat iron-rich foods, and avoid alcohol and tobacco. Register for Janani Suraksha Yojana benefits.",
        'child': "Monitor your child's growth milestones, ensure complete vaccination, and provide nutritious meals. For fever in infants under 3 months, seek immediate medical care.",
        'baby': "Monitor your child's growth milestones, ensure complete vaccination, and provide nutritious meals. For fever in infants under 3 months, seek immediate medical care.",
        'emergency': "For medical emergencies: call 108 for ambulance, 102 for maternal/child emergency, or visit the nearest hospital. Do not wait for online advice in life-threatening situations.",
        'ambulance': "Dial 108 for free ambulance service across most of India. Keep your address ready and describe the patient's condition clearly.",
        'sleep': "Adults need 7-9 hours of quality sleep. Maintain a regular schedule, avoid caffeine after 2 PM, and keep electronic devices away from bed.",
        'water': "Drink 8-10 glasses (2-3 liters) of water daily. Proper hydration supports digestion, circulation, temperature regulation, and kidney function.",
        'hydration': "Drink 8-10 glasses (2-3 liters) of water daily. Proper hydration supports digestion, circulation, temperature regulation, and kidney function.",
        'heart': "For heart health: eat a balanced diet low in saturated fats, exercise regularly, avoid smoking, limit alcohol, and get regular health checkups.",
        'eye': "Rest your eyes every 20 minutes when using screens (20-20-20 rule). Eat vitamin A-rich foods. Get annual eye checkups, especially if you have diabetes.",
        'dental': "Brush twice daily with fluoride toothpaste, floss regularly, and visit a dentist every 6 months. Limit sugary foods and drinks.",
        'skin': "Protect skin from sun with SPF 30+, stay hydrated, and moisturize. For persistent rashes or unusual moles, consult a dermatologist.",
        'first aid': "For cuts: clean with water, apply antiseptic, and cover with a clean bandage. For burns, cool with running water for 20 minutes. For serious injuries, call 108.",
        'covid': "Stay updated with COVID-19 guidelines from MoHFW. Get vaccinated and boosted as recommended. For symptoms like difficulty breathing, seek immediate medical care.",
        'corona': "Stay updated with COVID-19 guidelines from MoHFW. Get vaccinated and boosted as recommended. For symptoms like difficulty breathing, seek immediate medical care.",
        'anemia': "Eat iron-rich foods like spinach, lentils, and jaggery. Pair with vitamin C sources for better absorption. Get tested if you feel unusually tired or pale.",
        'thyroid': "Thyroid disorders require medical diagnosis and medication. Eat iodine-rich foods, avoid excessive soy, and get regular TSH tests as advised by your doctor.",
        'asthma': "Avoid triggers like dust, smoke, and pollen. Keep your inhaler accessible. Follow your doctor's action plan. Seek emergency care if breathing becomes severely difficult.",
        'arthritis': "Stay active with low-impact exercises like swimming and yoga. Maintain a healthy weight. Warm compresses can help joint stiffness. Consult a rheumatologist for treatment.",
        'cancer': "Early detection saves lives. Follow recommended screenings: breast self-exams, cervical screening, and colonoscopy as per age guidelines. Consult an oncologist for any concerns.",
        'hiv': "HIV is preventable and manageable. Use protection, never share needles, and get tested regularly. With treatment, people with HIV live long, healthy lives. Helpline: 1097.",
        'aids': "HIV is preventable and manageable. Use protection, never share needles, and get tested regularly. With treatment, people with HIV live long, healthy lives. Helpline: 1097.",
        'tb': "Tuberculosis is curable with proper medication. Complete the full course of treatment. Cover your mouth when coughing and ensure good ventilation. Free treatment is available under RNTCP.",
        'tuberculosis': "Tuberculosis is curable with proper medication. Complete the full course of treatment. Cover your mouth when coughing and ensure good ventilation. Free treatment is available under RNTCP.",
        'dengue': "Prevent dengue by eliminating stagnant water around your home. Symptoms include high fever, severe headache, and body pain. Seek medical care immediately if symptoms appear.",
        'malaria': "Use mosquito nets and repellents. Symptoms include fever, chills, and sweating. Seek prompt medical treatment. Free testing and treatment available at government health centers.",
        'typhoid': "Typhoid spreads through contaminated food and water. Drink boiled water, eat freshly cooked food, and wash hands regularly. Complete the full antibiotic course if prescribed.",
        'jaundice': "Jaundice indicates liver issues. Rest, avoid alcohol and fatty foods, and drink plenty of fluids. Seek medical evaluation to determine the underlying cause.",
        'depression': "You are not alone. Talk to someone you trust, maintain a routine, and seek professional help. Kiran Mental Health Helpline: 1800-599-0019. Help is available 24/7.",
        'anxiety': "Practice deep breathing (4-7-8 technique), limit caffeine, and maintain a sleep schedule. If anxiety interferes with daily life, consult a mental health professional.",
        'smoking': "Quitting smoking improves health immediately. Within 20 minutes, heart rate drops. Seek support through national quitlines and counseling. Your lungs can heal over time.",
        'alcohol': "Limit alcohol consumption. For men: max 2 drinks/day. For women: max 1 drink/day. Seek help if you cannot control drinking. Support groups and counseling are available.",
        'yoga': "Yoga improves flexibility, reduces stress, and enhances overall wellness. Start with basic asanas like Surya Namaskar, Pranayama, and meditation. Practice under guidance if you have health conditions.",
        'meditation': "Meditation reduces stress and improves focus. Start with 5-10 minutes daily. Focus on your breath. Apps like Dhyana and Insight Timer can guide beginners.",
        'or': "Oral Rehydration Solution (ORS) is life-saving for diarrhea. Mix 6 level teaspoons of sugar and 1/2 level teaspoon of salt in 1 liter of clean water. Give small, frequent sips.",
        'rehydration': "Oral Rehydration Solution (ORS) is life-saving for diarrhea. Mix 6 level teaspoons of sugar and 1/2 level teaspoon of salt in 1 liter of clean water. Give small, frequent sips.",
        'sanitation': "Wash hands with soap for 20 seconds. Use toilets safely. Keep drinking water clean. Proper sanitation prevents diseases like diarrhea, typhoid, and hepatitis.",
        'hygiene': "Wash hands with soap for 20 seconds. Use toilets safely. Keep drinking water clean. Proper sanitation prevents diseases like diarrhea, typhoid, and hepatitis.",
    }
    for key, resp in responses.items():
        if key in question:
            return resp
    return "Thank you for your health question. Our AI assistant provides general informational guidance only. For personalized medical advice, please consult a qualified healthcare professional or visit your nearest government health center."

#community assistance
@app.route('/community/assistant', methods=['GET', 'POST'])
def community_assistant():
    response = None
    question = ''
    if request.method == 'POST':
        question = request.form.get('question', '').strip().lower()
        response = get_community_response(question)
    return render_template('community/index.html', comm_response=response, comm_question=question)

#community assistance responses
def get_community_response(question):
    responses = {
        'volunteer': "You can volunteer through platforms like India.gov.in Volunteer India, MyGov, or local NGOs registered on NGO Darpan. Teaching, disaster relief, and elderly care are always in demand.",
        'ngo': "Find verified NGOs on NGO Darpan (ngodarpan.gov.in). You can search by state, cause, and registration status. Always verify an NGO before donating.",
        'teach': "You can volunteer through platforms like India.gov.in Volunteer India, MyGov, or local NGOs registered on NGO Darpan. Teaching, disaster relief, and elderly care are always in demand.",
        'mentor': "You can volunteer through platforms like India.gov.in Volunteer India, MyGov, or local NGOs registered on NGO Darpan. Teaching, disaster relief, and elderly care are always in demand.",
        'event': "Check MyGov (mygov.in) for national campaigns, or contact your local municipal corporation for neighbourhood events. Blood donation camps and health camps happen regularly.",
        'events': "Check MyGov (mygov.in) for national campaigns, or contact your local municipal corporation for neighbourhood events. Blood donation camps and health camps happen regularly.",
        'report': "For civic issues, use Swachh Bharat portal for sanitation, or contact your municipal corporation. For crimes, dial 100. For emergencies, dial 108. For women safety, call 1091.",
        'complaint': "For civic issues, use Swachh Bharat portal for sanitation, or contact your municipal corporation. For crimes, dial 100. For emergencies, dial 108. For women safety, call 1091.",
        'pothole': "Report road issues to your municipal corporation or use the Swachh Bharat portal. Include exact location and photos for faster resolution.",
        'road': "Report road issues to your municipal corporation or use the Swachh Bharat portal. Include exact location and photos for faster resolution.",
        'water': "For water supply issues, contact your local municipal corporation or visit Jal Jeevan Mission portal (jaljeevanmission.gov.in). For drinking water complaints, call 1916 in many cities.",
        'sanitation': "For sanitation issues, use the Swachh Bharat portal (swachhbharat.mygov.in) or contact your local municipal health officer.",
        'garbage': "For sanitation issues, use the Swachhbharat portal (swachhbharat.mygov.in) or contact your local municipal health officer.",
        'scheme': "Key government schemes: PMJAY (health insurance), Janani Suraksha (maternal care), National Pension Scheme, and PMAY (housing). Visit india.gov.in for full details.",
        'schemes': "Key government schemes: PMJAY (health insurance), Janani Suraksha (maternal care), National Pension Scheme, and PMAY (housing). Visit india.gov.in for full details.",
        'government': "Key government schemes: PMJAY (health insurance), Janani Suraksha (maternal care), National Pension Scheme, and PMAY (housing). Visit india.gov.in for full details.",
        'govt': "Key government schemes: PMJAY (health insurance), Janani Suraksha (maternal care), National Pension Scheme, and PMAY (housing). Visit india.gov.in for full details.",
        'shelter': "Contact your district administration or visit the National Urban Livelihoods Mission portal. For immediate shelter needs, contact local police stations or municipal offices.",
        'food': "Contact your district administration or visit the National Urban Livelihoods Mission portal. For immediate food needs, contact local NGOs or Anganwadi centres.",
        'blood': "Find blood banks through the National Health Portal (nhp.gov.in) or contact your nearest government hospital. Many cities have 24/7 blood bank helplines.",
        'donation': "Verify NGOs on NGO Darpan before donating. For disaster relief, donate through PM CARES or Chief Minister Relief Funds. Always ask for receipts.",
        'donate': "Verify NGOs on NGO Darpan before donating. For disaster relief, donate through PM CARES or Chief Minister Relief Funds. Always ask for receipts.",
        'tree': "Join tree plantation drives through MyGov, local municipal corporations, or environmental NGOs like SayTrees. Monsoon season (June-September) is ideal for planting.",
        'plant': "Join tree plantation drives through MyGov, local municipal corporations, or environmental NGOs like SayTrees. Monsoon season (June-September) is ideal for planting.",
        'green': "Join tree plantation drives through MyGov, local municipal corporations, or environmental NGOs like SayTrees. Monsoon season (June-September) is ideal for planting.",
        'environment': "Participate in Swachh Bharat drives, tree plantations, and waste segregation. Contact your municipal corporation for local environmental initiatives.",
        'clean': "Participate in Swachh Bharat drives, tree plantations, and waste segregation. Contact your municipal corporation for local environmental initiatives.",
        'swachh': "Participate in Swachh Bharat drives, tree plantations, and waste segregation. Contact your municipal corporation for local environmental initiatives.",
        'skill': "Learn skills through NSDC, PMKVY centres, or local community skill centres. Digital literacy, tailoring, and plumbing courses are widely available.",
        'training': "Learn skills through NSDC, PMKVY centres, or local community skill centres. Digital literacy, tailoring, and plumbing courses are widely available.",
        'digital': "Digital literacy camps are organized by CSC (Common Service Centres) and local NGOs. Check mygov.in for upcoming camps in your area.",
        'library': "Find public libraries through your district administration or municipal corporation. Many offer free internet, reading rooms, and skill books.",
        'emergency': "For police: 100 | Ambulance: 108 | Fire: 101 | Women Helpline: 1091 | Child Helpline: 1098 | Senior Citizen: 14567 | Mental Health: 1800-599-0019",
        'help': "For police: 100 | Ambulance: 108 | Fire: 101 | Women Helpline: 1091 | Child Helpline: 1098 | Senior Citizen: 14567 | Mental Health: 1800-599-0019",
        'safety': "For police: 100 | Ambulance: 108 | Fire: 101 | Women Helpline: 1091 | Child Helpline: 1098 | Senior Citizen: 14567 | Mental Health: 1800-599-0019",
        'women': "Women Helpline: 1091 | National Commission for Women: ncw.nic.in | One Stop Centres provide medical, legal, and counselling support.",
        'child': "Child Helpline: 1098 | NCPCR: ncPCR.gov.in | For child labour or abuse, contact local police or district child protection unit immediately.",
        'senior': "Senior Citizen Helpline: 14567 | National Portal for Senior Citizens: socialjustice.gov.in | Many cities have dedicated elderly care centres.",
        'elderly': "Senior Citizen Helpline: 14567 | National Portal for Senior Citizens: socialjustice.gov.in | Many cities have dedicated elderly care centres.",
        'disaster': "NDMA (ndma.gov.in) provides disaster preparedness guides. During emergencies, follow local administration instructions and tune into All India Radio.",
        'flood': "NDMA (ndma.gov.in) provides disaster preparedness guides. During emergencies, follow local administration instructions and tune into All India Radio.",
        'earthquake': "NDMA (ndma.gov.in) provides disaster preparedness guides. During emergencies, follow local administration instructions and tune into All India Radio.",
        'mygov': "MyGov (mygov.in) is the citizen engagement platform of India. Participate in surveys, discussions, volunteer programs, and government campaigns.",
        'india.gov': "India.gov.in is the national portal for government information, services, and schemes. It is the best starting point for any government-related query.",
        'nss': "National Service Scheme (NSS) is for college students. Contact your college NSS coordinator to join community service activities and earn certificates.",
        'ncc': "National Cadet Corps (NCC) trains school and college students in discipline and leadership. Contact your institution's NCC unit to enroll.",
        'youth': "National Service Scheme (NSS) and National Cadet Corps (NCC) offer youth engagement. MY Bharat (mybharat.gov.in) is a new platform for youth participation.",
    }
    for key, resp in responses.items():
        if key in question:
            return resp
    return "Thanks for your question! Our Community Assistant provides general guidance. For specific local information, contact your municipal corporation or visit india.gov.in. For emergencies, dial 100 (Police) or 108 (Ambulance)."

#energy responce assistence 

def get_energy_response(question):
    responses = {
        'solar': "Rooftop solar is ideal for Indian homes. 1 kW generates 4-5 units/day. Subsidy up to 40% for systems under 3 kW via solarrooftop.gov.in. Payback period is 4-6 years.",
        'panel': "Rooftop solar is ideal for Indian homes. 1 kW generates 4-5 units/day. Subsidy up to 40% for systems under 3 kW via solarrooftop.gov.in. Payback period is 4-6 years.",
        'subsidy': "Central subsidy: 40% up to 3 kW, 20% above 3 kW. Apply via solarrooftop.gov.in. State subsidies may add extra benefits.",
        'bill': "To reduce electricity bills: switch to LED, set AC at 24°C, use 5-star appliances, and unplug devices. Use our calculator in the Consumption section.",
        'save': "To reduce electricity bills: switch to LED, set AC at 24°C, use 5-star appliances, and unplug devices. Use our calculator in the Consumption section.",
        'led': "LED bulbs use 75% less energy than incandescent and last 25x longer. Under UJALA scheme, get them at ₹10-20 per bulb.",
        'bulb': "LED bulbs use 75% less energy than incandescent and last 25x longer. Under UJALA scheme, get them at ₹10-20 per bulb.",
        'ac': "Set AC to 24°C. Clean filters monthly. Use ceiling fans to circulate cool air. Inverter ACs save 30-40% compared to normal ACs.",
        'fan': "Ceiling fans use 50-75W. BLDC fans use only 30-35W and can save ₹1,500/year. Look for BEE 5-star rated fans.",
        'fridge': "Keep fridge at 3-5°C. Ensure 6-inch gap from walls for ventilation. Defrost regularly. A 5-star fridge saves ₹800-1,000/year.",
        'inverter': "Pure sine wave inverters are best for homes. Maintain battery water levels. A 150Ah battery with 850VA inverter powers 3-4 fans and lights for 6-8 hours.",
        'battery': "Pure sine wave inverters are best for homes. Maintain battery water levels. A 150Ah battery with 850VA inverter powers 3-4 fans and lights for 6-8 hours.",
        'geyser': "Solar water heaters save 1,000-1,500 units/year. If using electric, set timer to heat water only when needed. Insulate pipes.",
        'heater': "Solar water heaters save 1,000-1,500 units/year. If using electric, set timer to heat water only when needed. Insulate pipes.",
        'star': "BEE star ratings: 5-star is most efficient. A 5-star AC uses 30% less power than 3-star. Check ratings at beestarlabel.com before buying.",
        'rating': "BEE star ratings: 5-star is most efficient. A 5-star AC uses 30% less power than 3-star. Check ratings at beestarlabel.com before buying.",
        '5 star': "BEE star ratings: 5-star is most efficient. A 5-star AC uses 30% less power than 3-star. Check ratings at beestarlabel.com before buying.",
        'wind': "Small wind turbines (1-10 kW) work well in coastal and hilly areas with average wind speeds above 12 km/h. MNRE provides subsidies.",
        'biogas': "A 2-cubic-meter biogas plant converts kitchen waste into cooking gas for a family of 5. Contact your district Khadi Board for installation support.",
        'waste': "A 2-cubic-meter biogas plant converts kitchen waste into cooking gas for a family of 5. Contact your district Khadi Board for installation support.",
        'green': "Green energy refers to renewable sources like solar, wind, and biogas. India targets 50% non-fossil capacity by 2030.",
        'renewable': "Green energy refers to renewable sources like solar, wind, and biogas. India targets 50% non-fossil capacity by 2030.",
        'pm-kusum': "PM-KUSUM provides 60% subsidy for solar pumps for farmers. Apply through your state nodal agency or mnre.gov.in.",
        'kusum': "PM-KUSUM provides 60% subsidy for solar pumps for farmers. Apply through your state nodal agency or mnre.gov.in.",
        'pump': "PM-KUSUM provides 60% subsidy for solar pumps for farmers. Apply through your state nodal agency or mnre.gov.in.",
        'ujala': "UJALA scheme provides LED bulbs at ₹10, tube lights at ₹85, and fans at ₹1,150. Available at DISCOM offices and select retailers.",
        'discom': "Pay bills and register complaints via your state DISCOM website. Common ones: BSES Delhi, MSEDCL, TANGEDCO, BESCOM, KSEB.",
        'calculator': "Use our Electricity Bill Estimator in the Consumption section. Enter your appliance hours and get daily/monthly estimates instantly.",
        'unit': "1 unit = 1 kWh = running a 1000W appliance for 1 hour. Your bill = Total units × Rate per unit (typically ₹5-8).",
        'kwh': "1 unit = 1 kWh = running a 1000W appliance for 1 hour. Your bill = Total units × Rate per unit (typically ₹5-8).",
        'voltage': "Ideal voltage in India is 230V ± 10%. Use stabilizers for ACs and fridges. Voltage fluctuations damage appliances and waste energy.",
        'stabilizer': "Ideal voltage in India is 230V ± 10%. Use stabilizers for ACs and fridges. Voltage fluctuations damage appliances and waste energy.",
    }
    for key, resp in responses.items():
        if key in question:
            return resp
    return "Great energy question! Our assistant provides general guidance. For specific technical advice, consult a licensed electrician or visit mnre.gov.in. For billing issues, contact your state DISCOM."

# ============================================
# WATER MANAGEMENT ROUTES
# ============================================

# @app.route('/water')
# def water_home():
#     return render_template('water/index.html')

@app.route('/water/conservation')
def water_conservation():
    return render_template('water/conservation.html')

@app.route('/water/rainwater')
def water_rainwater():
    return render_template('water/rainwater.html')

@app.route('/water/usage')
def water_usage():
    return render_template('water/usage.html')

@app.route('/water/quality')
def water_quality():
    return render_template('water/quality.html')

@app.route('/water/irrigation')
def water_irrigation():
    return render_template('water/irrigation.html')

@app.route('/water/reuse')
def water_reuse():
    return render_template('water/reuse.html')

@app.route('/water/resources')
def water_resources():
    return render_template('water/resources.html')

@app.route('/water/assistant', methods=['GET', 'POST'])
def water_assistant():
    water_response = None
    water_question = None
    if request.method == 'POST':
        water_question = request.form.get('question', '').strip().lower()
        
        # Simple rule-based responses (no database needed)
        responses = {
            'rainwater': 'Rainwater harvesting captures rain from rooftops and stores it for reuse. Start with gutters, a first-flush diverter, and a storage tank. Visit the Rainwater page for a full guide and calculator.',
            'harvest': 'Rainwater harvesting captures rain from rooftops and stores it for reuse. Start with gutters, a first-flush diverter, and a storage tank. Visit the Rainwater page for a full guide and calculator.',
            'drip': 'Drip irrigation delivers water directly to plant roots with 85-95% efficiency. It can save 40-60% water compared to flood irrigation and increase yields by 20-50%. Check the Smart Irrigation page for details.',
            'irrigation': 'Drip irrigation delivers water directly to plant roots with 85-95% efficiency. It can save 40-60% water compared to flood irrigation and increase yields by 20-50%. Check the Smart Irrigation page for details.',
            'save water': 'Top ways to save water: fix leaks, use bucket baths, install tap aerators, run appliances only on full load, and reuse RO reject water for gardening. See the Conservation page for more tips.',
            'conservation': 'Top ways to save water: fix leaks, use bucket baths, install tap aerators, run appliances only on full load, and reuse RO reject water for gardening. See the Conservation page for more tips.',
            'quality': 'Safe drinking water should have TDS under 500 mg/L, pH between 6.5-8.5, and zero coliform bacteria. Use the Quality page to learn about home checks and when to get lab testing.',
            'leak': 'A dripping tap wastes 20+ litres/day. Check under sinks, behind toilets, and in common pipes. Add food colouring to the toilet tank — if colour appears in the bowl without flushing, you have a leak.',
            'jal jeevan': 'Jal Jeevan Mission aims to provide tap water to every rural household. Over 12 crore connections have been made. Visit jaljeevanmission.gov.in for more information.',
            'ro': 'RO purifiers reject 2-3 litres for every 1 litre purified. Collect this reject water for mopping, gardening, or flushing. Use the Reuse page calculator to see how much you can recover.',
            'reuse': 'Greywater from sinks and showers can be reused for gardening and flushing. Never drink reused water without advanced treatment. See the Reuse page for safety guidelines.',
            'groundwater': 'Groundwater levels are falling in many parts of India. Recharge pits and rainwater harvesting help replenish aquifers. Visit the Rainwater page for recharge pit designs.',
        }
        
        # Find matching response
        water_response = "I'm here to help with water conservation, harvesting, irrigation, and quality questions. Try asking about rainwater, drip irrigation, saving water, or water quality."
        for key, resp in responses.items():
            if key in water_question:
                water_response = resp
                break
                
    return render_template('water/index.html', water_response=water_response, water_question=water_question)


# ============================
# ERROR HANDLERS
# ============================

@app.errorhandler(404)
def page_not_found(e):
    """Shows a friendly message if a page doesn't exist."""
    return render_template('index.html', scroll_to='home'), 404





# ============================
# RUN THE APP
# ============================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)