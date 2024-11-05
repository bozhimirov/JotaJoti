

import PIL.Image
from encode import MartinM1 as m1
from decode import SSTVDecoder

image0 = PIL.Image.open('./original_images/1.jfif')
# image1 = PIL.Image.open('./original_images/logo2.png')
# image2 = PIL.Image.open('./original_images/15802g1_edited.jpg')
# image3 = PIL.Image.open('./original_images/japanese-painting-landscape-6.jpg')

m1(image0, 10000, 16, 1).write_wav('./audio/audio0.wav')
# m1(image1, 6900, 16).write_wav('./audio/audio1.wav')
# m1(image2, 6900, 16).write_wav('./audio/audio2.wav')
# m1(image3, 6900, 16).write_wav('./audio/audio3.wav')
audio0 = './audio/audio0.wav'
# audio0 = './audio/1.wav'
# audio1 = './audio/audio1.wav'
# audio2 = './audio/audio2.wav'
# audio3 = './audio/audio3.wav'
img0 = SSTVDecoder(audio0).decode().save('./images/image0.png')
# img1 = SSTVDecoder(audio1).decode().save('./images/image1.png')
# img2 = SSTVDecoder(audio2).decode().save('./images/image2.png')
# img3 = SSTVDecoder(audio3).decode().save('./images/image3.png')
print('done')
