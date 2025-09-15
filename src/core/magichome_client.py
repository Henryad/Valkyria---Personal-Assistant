from flux_led import WifiLedBulb


class MagicHome:
def __init__(self, ip: str, model: str="RGB"):
self.ip = ip
self.model = model
self.bulb = WifiLedBulb(ip)


def on(self):
self.bulb.turnOn()


def off(self):
self.bulb.turnOff()


def set_brightness(self, value:int):
value = max(1, min(100, value))
self.bulb.setBrightness(int(value/100*255))


def set_color_rgb(self, r:int, g:int, b:int):
self.bulb.setRgb(r, g, b)
