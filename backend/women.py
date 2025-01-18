from flask import Blueprint, render_template, jsonify, send_file, make_response
from flask_login import LoginManager, login_required
import io
from models import db, Shirts, ShirtImagesDetail  # Pastikan Anda mengimpor model yang sesuai

# Inisialisasi Blueprint
women = Blueprint(
    'women',
    __name__,
    template_folder='../frontend/women',
    static_folder='../frontend/women'
)

login_manager = LoginManager()
login_manager.init_app(women)

#Fungsi untuk menyajikan gambar berdasarkan shirt_id dan id 
@women.route('/serve_image/<int:shirt_id>/<int:id>')
def serve_image(shirt_id, id):
    # Ambil data gambar berdasarkan shirt_id dan id dari tabel ShirtImagesDetail
    image = ShirtImagesDetail.query.filter_by(shirt_id=shirt_id, id=id).first()
    if image and image.image_data:
        # Kirim data gambar (image_data) sebagai respons
        return send_file(
            io.BytesIO(image.image_data),
            mimetype='image/jpeg',  # Sesuaikan tipe gambar jika perlu (misalnya image/png)
            as_attachment=False
        )
    else:
        # Jika gambar tidak ditemukan
        return make_response('Image not found', 404)


    
@women.route('/women_shirts', methods=['GET'])
@login_required
def show_women_shirts():
    try:
        # Query dengan INNER JOIN untuk mendapatkan data dari tabel
        women_shirts = db.session.query(
            Shirts.name,
            ShirtImagesDetail.color,
            ShirtImagesDetail.size_s,
            ShirtImagesDetail.size_m,
            ShirtImagesDetail.size_l,
            ShirtImagesDetail.size_xl,
            ShirtImagesDetail.price,
            ShirtImagesDetail.shirt_id,
            ShirtImagesDetail.id,
            ShirtImagesDetail.image_data
        ).join(ShirtImagesDetail, Shirts.id == ShirtImagesDetail.shirt_id) \
         .filter(Shirts.type == 'women') \
         .order_by(ShirtImagesDetail.price.asc()).all()

        # Debug: print the result to ensure data is fetched correctly
        # print(women_shirts)
        
        # Kirim data ke template HTML
        return render_template('women_shirts.html', women_shirts=women_shirts)

    except Exception as e:
        # Tampilkan pesan error di halaman
        return render_template('error.html', error=str(e)), 500
    

@women.route('/women_shirts/<string:shirt_name>', methods=['GET'])
@login_required
def show_product_detail_shirt(shirt_name):
    try:
        # Ubah shirt_name menjadi format yang lebih mudah di-query
        formatted_shirt_name = shirt_name.replace('-', ' ')  # Ganti '-' kembali menjadi spasi

        # Query untuk mendapatkan detail produk berdasarkan shirt_name
        product_detail_shirt = db.session.query(
            Shirts.name,
            ShirtImagesDetail.color,
            ShirtImagesDetail.size_s,
            ShirtImagesDetail.size_m,
            ShirtImagesDetail.size_l,
            ShirtImagesDetail.size_xl,
            ShirtImagesDetail.price,
            ShirtImagesDetail.shirt_id,
            ShirtImagesDetail.id,
            ShirtImagesDetail.image_data
        ).join(ShirtImagesDetail, Shirts.id == ShirtImagesDetail.shirt_id) \
         .filter(Shirts.type == 'women', Shirts.name.like(f"%{formatted_shirt_name}%")).all()
         
         # Debug: Cetak hasil query
        print("Query Results:", product_detail_shirt)
        print("Original shirt_name:", shirt_name)
        print("Formatted shirt_name:", formatted_shirt_name)


        # Jika produk tidak ditemukan
        if not product_detail_shirt:
            return render_template('error.html', error="Product not found"), 404

        # Kirim data ke template HTML untuk menampilkan detail
        return render_template('product_detail/product_detail.html', product_detail_shirt=product_detail_shirt)

    except Exception as e:
        return render_template('error.html', error=str(e)), 500

