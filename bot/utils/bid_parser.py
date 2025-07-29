def parse_bid(text):
    text = text.lower().replace(',', '.').replace(' ', '')
    
    try:
        if text.endswith('jt'):
            return int(float(text[:-2]) * 1000000)
        elif text.endswith('rb'):
            return int(float(text[:-2]) * 1000)
        else:
            return int(text.replace('.', ''))
    except ValueError:
        return None