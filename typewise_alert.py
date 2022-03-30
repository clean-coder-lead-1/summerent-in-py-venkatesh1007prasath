#!/usr/bin/env python3


controller_present = True


def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    elif value > upper_limit:
        return 'TOO_HIGH'
    else:
        return 'NORMAL'


def classify_temperature_breach(cooling_type, temperature_in_celsius):
    temperature_breach = {
        "PASSIVE_COOLING": {"lower_limit": 0, "upper_limit": 35},
        "MED_ACTIVE_COOLING": {"lower_limit": 0, "upper_limit": 40},
        "HI_ACTIVE_COOLING": {"lower_limit": 0, "upper_limit": 45}
    }
    return infer_breach(
        temperature_in_celsius,
        temperature_breach[cooling_type]['lower_limit'],
        temperature_breach[cooling_type]['upper_limit'])


def check_and_alert(alert_target, battery_char, temperature_in_celsius):
    breach_type = classify_temperature_breach(battery_char['cooling_type'], temperature_in_celsius)
    alert_and_action = {'TO_CONTROLLER': send_to_controller, 'TO_EMAIL': send_to_email}
    alert_and_action[alert_target](breach_type)


def send_to_controller(breach_type):
    header = 0xfeed
    print(f'{header}, {breach_type}')


def send_to_email(breach_type):
    recipient = "a.b@c.com"
    temp_level = {"TOO_LOW": "too low", "TOO_HIGH": "too high"}
    if breach_type != 'NORMAL':
        if controller_present:
            send_to_controller(breach_type)
        print('To: {}'.format(recipient))
        print('Hi, the temperature is {}'.format(temp_level[breach_type]))
    else:
        print(breach_type)