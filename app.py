from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify, send_from_directory, session, has_request_context, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv # type: ignore
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import uuid
import os
from markupsafe import Markup
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


# ChatGPT
load_dotenv()

db = SQLAlchemy()
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    # Typically we would store the secret key locally, export FLASK_SECRET_KEY='your_persistent_secret_key'
    # and grab it using os.environ.get('FLASK_SECRET_KEY', 'default_secret_key'). Skipping for now.
    app.config['SECRET_KEY'] = 'd8fef143894de656d1820481a401960d'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.session_key = str(uuid.uuid4())
    db.init_app(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(120), nullable=False)
        profile_picture = db.Column(db.String(120), nullable=True)

        def set_password(self, password):
            self.password = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password, password)
        
    class PokerRound(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        date = db.Column(db.Date, nullable=False)
        buy_in = db.Column(db.Float, nullable=False)
        take_home = db.Column(db.Float, nullable=False)
        times_all_in = db.Column(db.Integer, nullable=False)
        additional_buy_in = db.Column(db.Float, nullable=False)
        times_nit_loss = db.Column(db.Integer, nullable=False)
        seat_position = db.Column(db.Integer, nullable=False)
    
    # ChatGPT
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ChatGPT
    with app.app_context():
        db.create_all()

    # ChatGPT
    @app.before_request
    def check_session():
        if 'user_id' in session and session.get('session_key') != app.session_key:
            session.clear()
            # flash("Session invalidated. Please log in again.", "warning")
            return redirect(url_for('sign_in'))
    
    # ChatGPT
    @app.teardown_appcontext
    def clear_session(exception=None):
        if has_request_context():
            session.clear()

    # ChatGPT
    @app.route("/", methods=["GET"])
    def index():
        profile_picture = url_for('static', filename='empty_user.png')
        show_plot = False
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user and user.profile_picture:
                profile_picture = url_for('uploaded_file', filename=user.profile_picture)
            else:
                profile_picture = url_for('static', filename='empty_user.png')

            poker_rounds_count = PokerRound.query.filter_by(user_id=user.id).count()
            if poker_rounds_count > 0:
                show_plot = True        

        return render_template("homepage.jinja2", profile_picture=profile_picture, show_plot=show_plot)

    @app.route("/sign-in", methods=["GET", "POST"])
    def sign_in():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.query.filter_by(email=email).first()

            # ChatGPT
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['session_key'] = app.session_key
                return redirect(url_for("index"))
            else:
                flash("Invalid email or password. Please try again...", "danger")

        return render_template("sign-in.jinja2")

    @app.route("/sign-up", methods = ["GET", "POST"])
    def sign_up():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("Passwords do not match!", "danger")
                return redirect(url_for("sign_up"))
            
            if not email or not password:
                flash("Email and password are required!", 'danger')
                return redirect(url_for("sign_up"))
            
            new_user = User(email=email)
            new_user.set_password(password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful!", "success")
                return redirect(url_for("sign_in"))
            # ChatGPT
            except IntegrityError:
                db.session.rollback()
                flash(Markup('There is already an account with this email address! \
                      Click <a href="/sign-in" class="alert-link">here</a> to login.'), "danger")
                return redirect(url_for("sign_up"))
        
        return render_template("sign-up.jinja2")
    
    # ChatGPT
    @app.route("/sign-out")
    def sign_out():
        session.pop('user_id', None)
        session.pop('session_key', None)
        flash("You have been logged out", "success")
        return redirect(url_for("index"))
    
    # ChatGPT
    @app.route("/check-email", methods=["POST"])
    def check_email():
        email = request.json.get("email")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"exists": True})
        return jsonify({"exists": False})

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            flash("Please log in to access settings", "danger")
            return redirect(url_for("sign_in"))

        # ChatGPT
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            if 'profile_picture' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            file = request.files['profile_picture']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                # Update user's profile picture in the database
                user.profile_picture = filename
                db.session.commit()
                # flash('Profile picture updated successfully!', 'success')
                return redirect(url_for('profile'))
            
        poker_rounds = PokerRound.query.filter_by(user_id=user.id).all()
        # print(poker_rounds)

        return render_template('profile.jinja2', user=user, poker_rounds=poker_rounds)

    # ChatGPT
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/new_round', methods=['GET', 'POST'])
    def new_round():
        if 'user_id' not in session:
            flash('Please log in to record a new round', "danger")
            return redirect(url_for("sign_in"))
        
        if request.method == "POST":
            date = request.form.get('date')
            buy_in = float(request.form.get("buy_in"))
            take_home = float(request.form.get("take_home"))
            times_all_in = int(request.form.get("times_all_in"))
            additional_buy_in = float(request.form.get("additional_buy_in"))
            times_nit_loss = int(request.form.get("times_nit_loss"))
            seat_position = int(request.form.get("seat_position"))

            new_round = PokerRound(
                user_id=session['user_id'],
                date=datetime.strptime(date, '%Y-%m-%d'),
                buy_in=buy_in,
                take_home=take_home,
                times_all_in=times_all_in,
                additional_buy_in=additional_buy_in,
                times_nit_loss=times_nit_loss,
                seat_position=seat_position
            )
            db.session.add(new_round)
            db.session.commit()

            flash("Round data recorded succesasfully!", "success")
            return redirect(url_for("index"))
        
        return render_template('new-round.jinja2') 
    
    @app.route('/delete_round/<int:round_id>', methods=['POST'])
    def delete_round(round_id):
        if 'user_id' not in session:
            flash('Please log in to perform this action', "danger")
            return redirect(url_for("sign_in"))

        # ChatGPT
        round_to_delete = PokerRound.query.get_or_404(round_id)
        if round_to_delete.user_id != session['user_id']:
            flash('You do not have permission to delete this round', "danger")
            return redirect(url_for("profile"))

        # ChatGPT
        db.session.delete(round_to_delete)
        db.session.commit()
        flash("Round deleted successfully!", "success")
        return redirect(url_for("profile"))

    @app.route('/plot')
    def plot():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'plot_div': ''})

        user = User.query.get(user_id)
        if not user:
            return jsonify({'plot_div': ''})

        poker_rounds = PokerRound.query.filter_by(user_id=user.id).all()

        dates = [pr.date for pr in poker_rounds]
        buy_ins = [pr.buy_in for pr in poker_rounds]
        take_homes = [pr.take_home for pr in poker_rounds]
        times_all_in = [pr.times_all_in for pr in poker_rounds]
        additional_buy_ins = [pr.additional_buy_in for pr in poker_rounds]
        total_buy_ins = [pr.buy_in + pr.additional_buy_in for pr in poker_rounds]
        times_nit_loss = [pr.times_nit_loss for pr in poker_rounds]
        seat_positions = [pr.seat_position for pr in poker_rounds]

        if not dates:
            return jsonify({'plot_div': ''})
        
        combined = list(zip(dates, buy_ins, take_homes, total_buy_ins, additional_buy_ins, seat_positions, times_nit_loss, times_all_in))
        combined.sort(key=lambda x: x[0])
        dates, buy_ins, take_homes, total_buy_ins, additional_buy_ins, seat_positions, times_nit_loss, times_all_in = zip(*combined)

        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=(
            'Gains/Losses and Buy-Ins Over Time',
            'Seat Position Over Time',
            'Nit Loss/All-In Count'))

        # ChatGPT
        # First plot: Gains/Losses and Buy-Ins
        fig.add_trace(go.Scatter(x=dates, y=buy_ins, mode='lines+markers', name='Buy-In', line=dict(color='rgb(136, 190, 238)')), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=take_homes, mode='lines+markers', name='Take Home'), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=total_buy_ins, mode='lines+markers', name='Total Buy-In', line=dict(dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=additional_buy_ins, mode='lines+markers', name="Add'l Buy-In", line=dict(dash='dot')), row=1, col=1)

        # ChatGPT
        # Second plot: Seat Position Over Time
        fig.add_trace(go.Scatter(x=dates, y=seat_positions, mode='lines+markers', name='Seat Position', line=dict(color='rgb(47, 190, 83)')), row=2, col=1)

        # ChatGPT
        # Third plot: Nit Loss/All-In Count
        fig.add_trace(go.Scatter(x=dates, y=times_nit_loss, mode='lines+markers', name='Nit Loss Count', line=dict(color='red')), row=3, col=1)
        fig.add_trace(go.Scatter(x=dates, y=times_all_in, mode='lines+markers', name='Times All-In', line=dict(color='purple')), row=3, col=1)

        fig.update_layout(
            height=800, 
            width=1000, 
            showlegend=True,
            plot_bgcolor='rgba(159, 159, 219, 0.3)',  # transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # transparent background
            font=dict(color='aliceblue'),
            margin=dict(t=20, b=40),  # adjust top and bottom margins
            title_x=0.5  # center the title
        )

        fig.update_xaxes(tickangle=45, color='aliceblue')
        fig.update_yaxes(title_text='Amount ($)', row=1, col=1, color='aliceblue')
        fig.update_yaxes(title_text='Seat Position', row=2, col=1, tickmode='linear', tick0=1, dtick=1, color='aliceblue')
        fig.update_yaxes(title_text='Count', row=3, col=1, color='aliceblue')

        plot_div = fig.to_html(full_html=False)
        return jsonify({'plot_div': plot_div})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
