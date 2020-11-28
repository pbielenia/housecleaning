from flask import request
from .arp import get_mac_address_of_ip_address


def get_user_id_from_mac_address(devices_details, mac_address):
    for device in devices_details:
        if mac_address in device:
            return device[2]
    return None


def get_users_names(db_cursor):
    result = db_cursor.execute('SELECT * FROM users')
    if result > 0:
        users_details = db_cursor.fetchall()
        return dict((x, y) for x, y in users_details)

    return None


def get_current_user_id(db_cursor):
    ip_address = request.remote_addr
    mac_address = get_mac_address_of_ip_address(ip_address)

    result = db_cursor.execute('SELECT * FROM devices')
    if result > 0:
        devices_details = db_cursor.fetchall()
        if mac_address:
            return get_user_id_from_mac_address(devices_details, mac_address)

    return None


class CleaningStatusIds:
    def __init__(self, cleaning_done, current_cleaner_id, previous_cleaner_id,
                 next_cleaner_id):
        self.cleaning_done = bool(cleaning_done)
        self.current_cleaner_id = int(current_cleaner_id)
        self.previous_cleaner_id = int(previous_cleaner_id)
        self.next_cleaner_id = int(next_cleaner_id)


class CleaningStatusNames:
    def __init__(self, cleaning_done=False, current_cleaner=None, previous_cleaner=None,
                 next_cleaner=None):
        self.cleaning_done = cleaning_done
        self.current_cleaner = current_cleaner
        self.previous_cleaner = previous_cleaner
        self.next_cleaner = next_cleaner


def get_cleaning_status(db_cursor):
    result = db_cursor.execute('SELECT * FROM cleaning_status')
    if result > 0:
        cleaning_status_details = db_cursor.fetchall()
        return CleaningStatusIds(
            cleaning_done=cleaning_status_details[0][0],
            current_cleaner_id=cleaning_status_details[0][1],
            previous_cleaner_id=cleaning_status_details[0][2],
            next_cleaner_id=cleaning_status_details[0][3])


def resolve_cleaning_status_names(cleaning_status_ids, users_names):
    names = CleaningStatusNames()

    if cleaning_status_ids.previous_cleaner_id in users_names:
        names.previous_cleaner = users_names[cleaning_status_ids.previous_cleaner_id]

    if cleaning_status_ids.current_cleaner_id in users_names:
        names.current_cleaner = users_names[cleaning_status_ids.current_cleaner_id]

    if cleaning_status_ids.next_cleaner_id in users_names:
        names.next_cleaner = users_names[cleaning_status_ids.next_cleaner_id]

    names.cleaning_done = cleaning_status_ids.cleaning_done

    return names
