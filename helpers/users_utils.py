from flask import request
from .arp import get_mac_address_of_ip_address


def get_user_name(users_mac_addresses):
    ip_address = request.remote_addr
    mac_address = get_mac_address_of_ip_address(ip_address)

    print(ip_address, mac_address)

    for key, val in users_mac_addresses.items():
        if mac_address in val:
            return key

    return 'Stranger'


def get_next_cleaner(name, cleaning_order):
    if name not in cleaning_order:
        raise Exception(f'Name \"{name}\" is not present in the cleaners list.')

    cleaner_id = cleaning_order.index(name)

    if cleaner_id + 1 == len(cleaning_order):
        return cleaning_order[0]
    else:
        return cleaning_order[cleaner_id + 1]
