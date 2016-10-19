from typing import Tuple
from Constants import 
    CYAN_MIN, CYAN_MAX, YELLOW_GREEN_FACTOR, 
    HUE_RANGE, VALUE_RANGE, SATURATION_RANGE


class HSVRatio:

    def __init__(self, hue = 0.0, saturation = 0.0, value = 0.0, ratio = 0.0):
        self.h     = hue
        self.s     = saturation
        self.v     = value
        self.ratio = ratio


    def average(self, h: float, s: float, v: float) -> None:
        self.h = (self.h + h) / 2
        self.s = (self.s + s) / 2
        self.v = (self.v + v) / 2


    def averageValue(self, overall_value: float) -> float:
        if self.ratio > 0.5:
            self.v = self.v * self.ratio + overall_value * (1 - self.ratio)
        else:
            self.v = (self.v + overall_value) / 2
    

    def hue(self, fullSpectrum: bool) -> Tuple[int, int, int]:
        if not fullSpectrum and self.s > 0.01:
            if self.h < 0.5:
                # yellow-green correction
                self.h = self.h * YELLOW_GREEN_FACTOR
                # cyan-green correction
                if  self.h > CYAN_MIN:
                    self.h = CYAN_MIN
            else:
                # cyan-blue correction
                if  self.h < CYAN_MAX:
                    self.h = CYAN_MAX

        h = int(self.h * HUE_RANGE)
        s = int(self.s * SATURATION_RANGE)
        v = int(self.v * VALUE_RANGE)
    
        if  v < hue.settings.ambilight_min:
            v = hue.settings.ambilight_min
        if  v > hue.settings.ambilight_max:
            v = hue.settings.ambilight_max
      
        return h, s, v


    def __repr__(self) -> str:
        return 'h: {!s} s: {!s} v: {!s} ratio: {!s}'.format(
                 self.h, self.s, self.v, self.ratio)
