from flask import Flask, render_template
from controllers.auction_controller import auction_bp
from config import Config
from models.auction import AuctionModel

template_dir = os.path.abspath('views/templates')
static_dir = os.path.abspath('views/static')

app = Flask(__name__, 
            template_folder=template_dir,
            static_folder=static_dir)

@app.template_filter('format_rupiah')
def format_rupiah_filter(value):
    if value >= 1000000:
        return f"Rp{value / 1000000:.1f}jt".replace('.0', '')
    elif value >= 1000:
        return f"Rp{value / 1000:.0f}rb"
    return f"Rp{value:,}".replace(',', '.')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002, debug=True)