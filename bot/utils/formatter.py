def format_rupiah(amount):
    if amount >= 1000000:
        return f"Rp{amount / 1000000:.1f}jt".replace('.0', '')
    elif amount >= 1000:
        return f"Rp{amount / 1000:.0f}rb"
    return f"Rp{amount:,}".replace(',', '.')