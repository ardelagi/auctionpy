import os
from flask import Flask, render_template
from controllers.auction_controller import auction_bp
from config import Config

# Dapatkan path absolut ke folder views
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'views', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'views', 'static')

app = Flask(__name__,
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)

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

# Filter untuk format datetime
@app.template_filter('datetimeformat')
def datetimeformat_filter(timestamp, format='%H:%M:%S'):
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime(format)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    
    print(f"Template path: {app.template_folder}")
    print(f"Static path: {app.static_folder}")
    

    if os.path.exists(app.template_folder):
        print("Files in template folder:")
        for f in os.listdir(app.template_folder):
            print(f"- {f}")
    else:
        print("Template folder not found!")
    
    app.run(host='0.0.0.0', port=3002, debug=True)