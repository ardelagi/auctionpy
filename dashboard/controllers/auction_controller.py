from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from models.auction import AuctionModel

auction_bp = Blueprint('auction', __name__)

@auction_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if (username == current_app.config['ADMIN_USERNAME'] and 
            password == current_app.config['ADMIN_PASSWORD']):
            session['logged_in'] = True
            return redirect(url_for('auction.dashboard'))
        
        return render_template('login.html', error='Kredensial salah!')
    
    return render_template('login.html')

@auction_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('auction.login'))

@auction_bp.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('auction.login'))
    
    auctions = AuctionModel.get_active_auctions()
    return render_template('index.html', auctions=auctions)

@auction_bp.route('/auction/<auction_id>')
def auction_detail(auction_id):
    if not session.get('logged_in'):
        return redirect(url_for('auction.login'))
    
    auction = AuctionModel.get_auction(auction_id)
    if auction:
        return render_template('auction_detail.html', auction=auction)
    return "Lelang tidak ditemukan", 404

@auction_bp.route('/stop_auction/<auction_id>', methods=['POST'])
def stop_auction(auction_id):
    if not session.get('logged_in'):
        return redirect(url_for('auction.login'))
    
    AuctionModel.stop_auction(auction_id)
    return redirect(url_for('auction.dashboard'))