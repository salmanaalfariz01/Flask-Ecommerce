from flask import Blueprint, render_template, jsonify, send_file, make_response, request

from flask_login import LoginManager, login_required
import io
from models import db, Cart

# Inisialisasi Blueprint
cart = Blueprint(
    'cart',
    __name__,
    template_folder='../frontend/cart',
    static_folder='../frontend/cart'
)

login_manager = LoginManager()
login_manager.init_app(cart)

@cart.route('/cart', methods=['GET'])
def show_cart():
    try:
        # Ambil semua item di keranjang dari database
        cart_items = Cart.query.all()
        print("Cart items:", cart_items)  # Debug: Periksa data dari database

        # Siapkan data untuk dikirim ke template
        cart_data = [{
            'image': item.image,
            'name': item.name,
            'color': item.color,
            'size': item.size,
            'price': item.price,
            'qty': item.qty,
            'total_price': item.total_price
        } for item in cart_items]

        # Render template cart.html dengan data
        return render_template('cart.html', cart_items=cart_data)
    except Exception as e:
        print("Error:", str(e))  # Debug: Cetak error jika ada
        return f"Error: {str(e)}", 500




