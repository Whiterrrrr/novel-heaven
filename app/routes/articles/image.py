from flask import  send_from_directory
from . import articles_bp
import os
from pathlib import Path

@articles_bp.route('/cover/<path:filename>')
def get_cover(filename):
    print(f'filename is {filename}')
    base_dir = Path(__file__).parent.parent.parent.parent / 'book_sample'
    print(base_dir)
    return send_from_directory(str(base_dir), filename)