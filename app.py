"""
Gruha Alankara - Main Flask Application
Activity 4.1: Core routes, authentication, file uploads, and tool integration.
"""

import os
import uuid
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from extensions import db

# ──────────────────────────────────────────────
# 1. Initialize Flask App
# ──────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

# Ensure required directories exist
db_dir = os.path.join(os.path.dirname(__file__), 'database')
os.makedirs(db_dir, exist_ok=True)
os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)

# ──────────────────────────────────────────────
# 2. Initialize Database
# ──────────────────────────────────────────────
db.init_app(app)

# ──────────────────────────────────────────────
# 3. Import Models and Tools
# ──────────────────────────────────────────────
from models import User, Design, Furniture, Booking

from tools.room_analyzer import RoomAnalyzer
from tools.style_suggester import StyleSuggester
from tools.furniture_optimizer import FurnitureOptimizer
from tools.budget_planner import BudgetPlanner
from tools.design_catalog import DesignCatalog

# Initialize tool instances (available for route handlers)
room_analyzer = RoomAnalyzer()
style_suggester = StyleSuggester()
furniture_optimizer = FurnitureOptimizer()
budget_planner = BudgetPlanner()
design_catalog = DesignCatalog()


# ──────────────────────────────────────────────
# 4. File Upload Validation Helper
# ──────────────────────────────────────────────
def allowed_file(filename):
    """
    Check if the uploaded file has a valid extension.
    Returns True if the filename contains a '.' and its
    extension is in the ALLOWED_EXTENSIONS set.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config.get('ALLOWED_EXTENSIONS', set())


# ──────────────────────────────────────────────
# 5. Homepage Route
# ──────────────────────────────────────────────
@app.route('/')
def index():
    """Render the landing page."""
    return render_template('index.html')


# ──────────────────────────────────────────────
# 6. User Registration Route
# ──────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # --- Validation ---
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please log in.', 'error')
            return redirect(url_for('register'))

        # Check if username is already taken
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('This username is already taken.', 'error')
            return redirect(url_for('register'))

        # --- Create new user with hashed password ---
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# ──────────────────────────────────────────────
# 7. User Login Route
# ──────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login with email and password."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Query the database for a matching user
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            # Store user ID in session
            session['user_id'] = user.id
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('design'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


# ──────────────────────────────────────────────
# 8. Logout Route
# ──────────────────────────────────────────────
@app.route('/logout')
def logout():
    """Log the user out by clearing the session."""
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ──────────────────────────────────────────────
# 9. Design Interface Route (Protected)
# ──────────────────────────────────────────────
@app.route('/design', methods=['GET', 'POST'])
def design():
    """Render the design studio page. Requires authentication."""
    if 'user_id' not in session:
        flash('Please log in to access the Design Studio.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle design form submission
        room_type = request.form.get('room_type', 'living_room')
        style = request.form.get('style', 'modern')
        budget_str = request.form.get('budget', '0')
        budget = float(budget_str) if budget_str else 0.0

        # Handle optional image upload
        image_path = ''
        if 'room_image' in request.files:
            file = request.files['room_image']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_name = f"{uuid.uuid4().hex}.{ext}"
                safe_name = secure_filename(unique_name)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
                file.save(save_path)
                image_path = save_path

                # Save design record
                new_design = Design(
                    user_id=session['user_id'],
                    image_path=safe_name,
                    selected_style=style,
                    created_at=datetime.utcnow()
                )
                db.session.add(new_design)
                db.session.commit()

        flash('Design request submitted successfully!', 'success')
        return render_template('design.html')

    return render_template('design.html')


# ──────────────────────────────────────────────
# 10. Image Upload Route
# ──────────────────────────────────────────────
@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle image uploads from authenticated users.
    Validates the file, saves it with a unique name,
    and creates a Design record in the database.
    """
    # Require authentication
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required.'}), 401

    # Check that a file was included in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    # Validate file extension
    if not allowed_file(file.filename):
        allowed = ', '.join(app.config.get('ALLOWED_EXTENSIONS', set()))
        return jsonify({'error': f'Invalid file type. Allowed: {allowed}'}), 400

    # Generate a unique, secure filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    safe_name = secure_filename(unique_name)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

    # Save the file
    file.save(save_path)

    # Get optional style selection from form data
    selected_style = request.form.get('style', '')

    # Create a Design record in the database
    new_design = Design(
        user_id=session['user_id'],
        image_path=safe_name,
        selected_style=selected_style,
        created_at=datetime.utcnow()
    )
    db.session.add(new_design)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Image uploaded successfully.',
        'design_id': new_design.id,
        'filename': safe_name
    }), 200


# ──────────────────────────────────────────────
# Additional Page Routes
# ──────────────────────────────────────────────
@app.route('/catalog')
def catalog():
    """Render the furniture catalog page."""
    return render_template('catalog.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Render the room analysis page and handle image uploads."""
    analysis = None

    if request.method == 'POST':
        if 'room_image' in request.files:
            file = request.files['room_image']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_name = f"analyze_{uuid.uuid4().hex}.{ext}"
                safe_name = secure_filename(unique_name)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
                file.save(save_path)

                # Run room analysis
                analysis = room_analyzer.analyze(save_path)
                flash('Room analysis complete!', 'success')
            else:
                flash('Please upload a valid image file (JPG, JPEG, PNG).', 'error')
        else:
            flash('No image file provided.', 'error')

    return render_template('analyze.html', analysis=analysis)


@app.route('/ar-viewer')
def ar_viewer():
    """Render the AR furniture viewer page."""
    return render_template('ar_viewer.html')


@app.route('/live-ar-camera')
def live_ar_camera():
    """Render the live AR camera page."""
    return render_template('live_ar_camera.html')


@app.route('/upload-image', methods=['POST'])
def upload_image():
    """Handle image uploads from the AR camera capture."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
    unique_name = f"capture_{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_name)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

    file.save(save_path)

    return jsonify({
        'success': True,
        'message': 'Image captured successfully.',
        'filename': safe_name
    }), 200


# ──────────────────────────────────────────────
# Database Test Route
# ──────────────────────────────────────────────
@app.route('/test-db')
def test_db():
    """Test route to verify database connectivity."""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'success',
            'message': 'Database connection is working!'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}'
        }), 500


# ──────────────────────────────────────────────
# 13. Application Entry Point
# ──────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
