from Constants import \
    CYAN_MIN, CYAN_MAX, YELLOW_GREEN_FACTOR, \
    HUE_RANGE, VALUE_RANGE, SATURATION_RANGE, \
    MIN_RATIO


class HSVRatio:

    def __init__(self, hue = 0.0, saturation = 0.0, value = 0.0, ratio = 0.0):
        self.h     = hue
        self.s     = saturation
        self.v     = value
        self.ratio = ratio


    def average(self, h, s, v):
        self.h = (self.h + h) / 2
        self.s = (self.s + s) / 2
        self.v = (self.v + v) / 2


    def average_value(self, overall_value):
        if self.ratio > MIN_RATIO:
            ratio = self.ratio
        else:
            ratio = MIN_RATIO
        self.v = self.v * ratio + overall_value * (1 - ratio)


    def hue(self, full_spectrum):
        if not full_spectrum and self.s > 0.01:
            if self.h < 0.5:
                # yellow-green correction
                self.h *= YELLOW_GREEN_FACTOR
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


    def __repr__(self):
        return 'h: {!s} s: {!s} v: {!s} ratio: {!s}'.format(
                 self.h, self.s, self.v, self.ratio)
