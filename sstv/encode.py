from JotaJoti.sstv.constants import M1, Color
from JotaJoti.sstv.sstv import SSTV


class MartinM1(SSTV):
    COLOR_SEQ = (Color.green, Color.blue, Color.red)
    VIS_CODE = M1.VIS_CODE
    WIDTH = M1.LINE_WIDTH
    HEIGHT = M1.LINE_COUNT
    SYNC = M1.SYNC_PULSE * 1000
    SCAN = M1.SCAN_TIME * 1000
    INTER_CH_GAP = M1.SEP_PULSE * 1000

    def before_channel(self, color):
        if color is Color.green:
            yield M1.FREQ_BLACK, self.INTER_CH_GAP

    def after_channel(self, color):
        yield M1.FREQ_BLACK, self.INTER_CH_GAP
