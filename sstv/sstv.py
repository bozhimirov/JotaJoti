from __future__ import division, with_statement

from math import sin, pi
from random import random
from contextlib import closing
from itertools import cycle, chain
from array import array
import wave

from PIL import Image
from PIL.Image import Resampling

from JotaJoti.sstv.constants import M1, BITS_TO_STRUCT
from JotaJoti.sstv.helpers import byte_to_freq


class SSTV:

    def __init__(self, image, samples_per_sec, bits, n_channels=1):
        self.image = self._image_resize(image)
        self.samples_per_sec = samples_per_sec
        self.bits = bits
        self.n_channels = n_channels
        self.pixels = self.image.convert('RGB').load()

    @staticmethod
    def _image_resize(image: Image) -> Image:
        """
        This internal function resize the image to fit into the size of the coded audio file, adding a background.

        Return:
        Image: Returns the resized image.
        """
        base_width = 320
        base_height = 256
        while image.size[0] > base_width or image.size[1] > base_height:
            image = image.resize((int(image.size[0] * 0.99), int(image.size[1] * 0.99)),
                                 Resampling.LANCZOS)

        fill_color = (0, 0, 0, 0)
        new_im = Image.new('RGBA', (base_width, base_height), fill_color)
        new_im.paste(image, (int((base_width - image.size[0]) / 2), int((base_height - image.size[1]) / 2)))
        return new_im

    def write_wav(self, filename):
        """writes the whole image to a Microsoft WAV file"""
        fmt = BITS_TO_STRUCT[self.bits]
        data = array(fmt, self.gen_samples())
        if self.n_channels != 1:
            data = array(fmt, chain.from_iterable(
                zip(*([data] * self.n_channels))))
        with closing(wave.open(filename, 'wb')) as wav:
            wav.setnchannels(self.n_channels)
            wav.setsampwidth(self.bits // 8)
            wav.setframerate(self.samples_per_sec)
            wav.writeframes(data)

    def gen_samples(self):
        """generates discrete samples from gen_values()

           performs quantization according to
           the bits per sample value given during construction
        """
        max_value = 2 ** self.bits
        alias = 1 / max_value
        amp = max_value // 2
        lowest = -amp
        highest = amp - 1
        alias_cycle = cycle((alias * (random() - 0.5) for _ in range(1024)))
        for value, alias_item in zip(self.gen_values(), alias_cycle):
            sample = int(value * amp + alias_item)
            yield (lowest if sample <= lowest else
                   sample if sample <= highest else highest)

    def gen_values(self):
        """generates samples between -1 and +1 from gen_freq_bits()

           performs sampling according to
           the samples per second value given during construction
        """
        spms = self.samples_per_sec / 1000
        offset = 0
        samples = 0
        factor = 2 * pi / self.samples_per_sec
        sample = 0
        for freq, msec in self.gen_freq_bits():
            samples += spms * msec
            tx = int(samples)
            freq_factor = freq * factor
            for sample in range(tx):
                yield sin(sample * freq_factor + offset)
            offset += (sample + 1) * freq_factor
            samples -= tx

    def gen_freq_bits(self):
        """generates tuples (freq, msec) that describe a sine wave segment

           frequency "freq" in Hz and duration "msec" in ms
        """
        yield M1.FREQ_VIS_START, M1.MSEC_VIS_START
        yield M1.FREQ_SYNC, M1.MSEC_VIS_SYNC
        yield M1.FREQ_VIS_START, M1.MSEC_VIS_START
        yield M1.FREQ_SYNC, M1.MSEC_VIS_BIT  # start bit
        vis = self.VIS_CODE
        num_ones = 0
        for _ in range(7):
            bit = vis & 1
            vis >>= 1
            num_ones += bit
            bit_freq = M1.FREQ_VIS_BIT1 if bit == 1 else M1.FREQ_VIS_BIT0
            yield bit_freq, M1.MSEC_VIS_BIT
        parity_freq = M1.FREQ_VIS_BIT1 if num_ones % 2 == 1 else M1.FREQ_VIS_BIT0
        yield parity_freq, M1.MSEC_VIS_BIT
        yield M1.FREQ_SYNC, M1.MSEC_VIS_BIT  # stop bit
        yield from self.gen_image_tuples()


    def gen_image_tuples(self):
        for line in range(self.HEIGHT):
            yield from self.horizontal_sync()
            yield from self.encode_line(line)


    def horizontal_sync(self):
        yield M1.FREQ_SYNC, self.SYNC

    def encode_line(self, line):
        msec_pixel = self.SCAN / self.WIDTH
        image = self.pixels
        for color in self.COLOR_SEQ:
            yield from self.before_channel(color)
            for col in range(self.WIDTH):
                pixel = image[col, line]
                freq_pixel = byte_to_freq(pixel[color.value])
                yield freq_pixel, msec_pixel
            yield from self.after_channel(color)

    def before_channel(self, color):
        return []

    after_channel = before_channel

