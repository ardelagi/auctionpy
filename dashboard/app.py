from flask import Flask, render_template
from controllers.auction_controller import auction_bp
import os
from config import Config
from bson import ObjectId

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auction_bp)

# Jinja filter untuk format Rupiah
@app.template_filter('format_rupiah')
def format_rupiah_filter(value):
    try:
        value = int(value)
        if value >= 1000000:
            return f"Rp{value / 1000000:.1f}jt".replace('.0', '')
        elif value >= 1000:
            return f"Rp{value / 1000:.0f}rb"
        return f"Rp{value:,}".replace(',', '.')
    except:
        return f"Rp{value}"

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True)