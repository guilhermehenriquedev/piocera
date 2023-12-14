
def get_payment_status(status_pagseguro):
    status_map = {
        'AUTHORIZED': 'CONFIRMED',
        'PAID': 'CONFIRMED',
        'IN_ANALYSIS': 'PENDING',
        'DECLINED': 'DECLINED',
    }
    return status_map.get(status_pagseguro, 'CANCELED')
