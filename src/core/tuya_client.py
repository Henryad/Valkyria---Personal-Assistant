import tinytuya


class TuyaLAN:
def __init__(self, dev_id: str, local_key: str, ip: str, version: str="3.3", dps_switch: int=1):
self.dev = tinytuya.BulbDevice(dev_id, ip, local_key)
self.dev.set_version(float(version))
self.dps_switch = dps_switch


def on(self):
return self.dev.set_status(True, self.dps_switch)


def off(self):
return self.dev.set_status(False, self.dps_switch)


def set_brightness(self, value: int):
value = max(1, min(100, value))
return self.dev.set_brightness_percentage(value)


def set_color_rgb(self, r:int, g:int, b:int):
return self.dev.set_colour(r, g, b)
