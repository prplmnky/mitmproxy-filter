from passthrough_addon import Passthrough
from uplynk_addon import Uplynk
from unicornmedia_addon import UnicornMedia

passthrough_addon = Passthrough()
addons = [
    passthrough_addon,
    Uplynk(),
    UnicornMedia()
]