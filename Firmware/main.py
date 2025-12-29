# Kev's Macropad
import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from kmk.extensions.pegasus_oled_ssd1306 import PegasusOLEDSSD1306

from adafruit_mcp230xx.mcp23008 import MCP23008

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

i2c = busio.I2C(scl=board.D5, sda=board.D4)

mcp = MCP23008(i2c, address=0x20)

keyboard.col_pins = [
    mcp.get_pin(0), 
    mcp.get_pin(1), 
    mcp.get_pin(2), 
    mcp.get_pin(3)
]

keyboard.row_pins = [
    mcp.get_pin(4), # r1
    mcp.get_pin(5), # r2
    mcp.get_pin(6)  # r3
]

keyboard.diode_orientation = DiodeOrientation.ROW2COL

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.D0, board.D1, None, False),
    (board.D6, board.D7, None, False),
)

rgb = RGB(
    pixel_pin=board.D3, 
    num_pixels=16,
    val_limit=150,
    hue_default=160,
    sat_default=255,
    val_default=100,
)
keyboard.extensions.append(rgb)

oled_ext = PegasusOLEDSSD1306(
    i2c=i2c,
    width=128, height=32,
    display_offset=0
)
keyboard.extensions.append(oled_ext)

keyboard.keymap = [
    [
        KC.MUTE,  KC.NO,    KC.NO,    KC.ENT,
        
        KC.N7,    KC.N8,    KC.N9,    KC.BSPC,
        
        KC.N4,    KC.N5,    KC.N6,    KC.SPC,
    ]
]

encoder_handler.map = [
    ( (KC.VOLU, KC.VOLD), (KC.MW_UP, KC.MW_DN) ),
]

if __name__ == '__main__':
    keyboard.go()