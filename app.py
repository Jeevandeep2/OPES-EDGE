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
    return render_template('education.html')


@app.route('/healthcare')
def healthcare():
    """Healthcare module placeholder."""
    return render_template('healthcare.html')


@app.route('/community')
def community():
    """Community Services module placeholder."""
    return render_template('community.html')


@app.route('/energy')
def energy():
    """Energy Management module placeholder."""
    return render_template('energy.html')


@app.route('/water')
def water():
    """Water Management module placeholder."""
    return render_template('water.html')


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