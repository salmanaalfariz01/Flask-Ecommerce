from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import db, Users
import sqlalchemy
from datetime import datetime
import pytz



# Tambahkan static_folder ke Blueprint
register = Blueprint(
    'register', 
    __name__, 
    template_folder='../frontend/register', 
    static_folder='../frontend/register'  # Menyertakan direktori static
)

# Zona waktu Indonesia (WIB)
indonesia_timezone = pytz.timezone('Asia/Jakarta')

# Waktu saat ini dalam zona waktu Indonesia
current_time = datetime.now(indonesia_timezone)

login_manager = LoginManager()
login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        nama = request.form['nama']  # Get nama from the form
        no_hp = request.form['no_hp']  # Get no_hp from the form
        alamat = request.form['alamat']  # Get alamat from the form
    
        # Validate required fields
        if username and email and password and confirm_password and nama and no_hp and alamat:
            if password == confirm_password:
                # Hash the password using pbkdf2:sha256 method
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                try:
                    # Create a new user with all fields
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                        nama=nama,
                        no_hp=no_hp,
                        alamat=alamat,
                        role=None,
                        created_at=current_time,  # Waktu dalam zona waktu Indonesia
                        deleted_at=None     
                    )

                    # Add and commit the new user to the database
                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    # Handle duplicate username or email
                    return redirect(url_for('register.show') + '?error=user-or-email-exists')

                # Redirect to login page with success message
                return redirect(url_for('login.show') + '?success=account-created')
            else:
                # Handle password mismatch
                return redirect(url_for('register.show') + '?error=password-mismatch')
        else:
            # Handle missing fields
            return redirect(url_for('register.show') + '?error=missing-fields')
    else:
        # Render the registration form
        return render_template('register.html')