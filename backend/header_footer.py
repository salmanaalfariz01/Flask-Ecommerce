# header_footer/__init__.py
from flask import Blueprint, render_template

# Definisikan blueprint untuk header dan footer
header_footer = Blueprint(
    'header_footer',
    __name__,
    template_folder='frontend/header_footer',  # Folder template
    static_folder='frontend/header_footer'         # Folder file statis (CSS, JS, dll)
)

def show_header_footer():
    return render_template('header_footer.html')
