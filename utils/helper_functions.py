import json


def write_settings_to_json(settings_obj, debug=False):
    """"
    Writes the custom settings object to a dictionary
    """
    settings_dict={'button_img':settings_obj.show_image, 'button_time': settings_obj.show_time, 'button_cal':settings_obj.show_calendar, 'button_spot':settings_obj.show_spotify, 'slider_brightness':100}
    with open('temp/settings.json', 'w') as outfile:
        json.dump(settings_dict, outfile)

    if debug:
        print("Wrote settings to file")


def read_settings_json(settings_obj, debug=False):
    """"
    Writes the custom settings object to a dictionary
    """
    with open('temp/settings.json') as json_file:
        data = json.load(json_file)

    settings_obj.show_image = data['button_img']
    settings_obj.show_time = data['button_time']
    settings_obj.show_calendar = data['button_cal']
    settings_obj.show_spotify = data['button_spot']
    settings_obj.brightness = data['slider_brightness']

    if debug:
        print(f"Read settings", {data})

    return settings_obj

