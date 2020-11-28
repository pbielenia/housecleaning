import subprocess


def format_arp_result(result):
    formatted_records = list()

    arp_records = result.decode('utf-8').split('\n')[1:]
    expected_parameters_length = 5

    for record in arp_records:
        parameters = record.split()
        if len(parameters) == expected_parameters_length:
            formatted_records.append(ArpReturnData(parameters))

    return formatted_records


class ArpReturnData:
    def __init__(self, result):
        if len(result) != 5:
            raise Exception(f'Expected exactly 5 elements, got {len(result)}')

        self.ip_address = result[0]
        self.hw_type = result[1]
        self.hw_address = result[2]
        self.flags_mask = result[3]
        self.interface = result[4]


def get_mac_address_of_ip_address(ip_address):
    process = subprocess.Popen(['arp', '-n'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    results, err = process.communicate()

    if err:
        raise Exception(err.decode('utf-8'))

    formatted_results = format_arp_result(results)
    related_host = next(
        (host for host in formatted_results if host.ip_address == ip_address), None)
    return related_host.hw_address.upper() if related_host else None
