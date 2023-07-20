import datetime
import re

from socialnetwork.models import ConnectionRequest, Connection


def check_request_allowed(from_id):
    current_time = datetime.datetime.now()
    min_minute_latter = current_time - datetime.timedelta(minutes=1)
    time_range = (min_minute_latter, current_time)
    connection_count = ConnectionRequest.number_of_request(from_id, time_range)
    return connection_count


def check_connection_request_already_sent(from_user, to_user):
    try:
        connection_request_instance = ConnectionRequest.check_request_already_send(from_user, to_user)
        if connection_request_instance:
            return True
    except Exception:
        return False


def already_connected(from_id, to_id):
    try:
        relation = Connection.check_connection_present(from_id, to_id)
        if relation:
            return True
    except Exception as e:
        return False


def send_new_connection_request(from_user, to_user):
    try:
        connection_request_instance = ConnectionRequest.create_connection_request(from_user, to_user)
        msg = f'Request Send from {connection_request_instance.sender_user} to {connection_request_instance.receiver_user}'
    except Exception as e:
        msg = f'Error while sending connection request from {from_user} to {to_user}'
    return msg


def check_valid_email(search_field):
    pattern = r'^[\w\.]+@[\w\.]+\.(com|in)$'
    return re.match(pattern, search_field) is not None
