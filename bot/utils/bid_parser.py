def parse_bid(text):
    text = text.lower().replace(',', '.').replace(' ', '')
    
    if text.endswith('jt'):
        try:
            return int(float(text[:-2]) * 1000000)
        except:
            return None
    elif text.endswith('rb'):
        try:
            return int(float(text[:-2]) * 1000)
        except:
            return None
    else:
        try:
            return int(text)
        except:
            return None