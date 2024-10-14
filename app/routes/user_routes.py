from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
# 'db' importunu burada değil, fonksiyon içerisinde yapacağız.

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # 'db' burada import ediliyor, döngüsel bağımlılığı kırmak için
    from app import db

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Kullanıcı oluşturma işlemi
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        # Kullanıcıyı veritabanına kaydetme
        new_user.save()

        flash('Kayıt başarılı, giriş yapabilirsiniz!')
        return redirect(url_for('user.login'))

    return render_template('user/signup.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.objects(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Hoş geldin, {user.username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Geçersiz giriş bilgileri.', 'danger')
            return redirect(url_for('user.signup'))

    return render_template('user/login.html')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('user.login'))

@user_bp.route('/profile')
def profile():
    if current_user.is_authenticated:
        username = current_user.username
        return f'Hoş geldin, {username}!'
    else:
        return redirect(url_for('user.login'))