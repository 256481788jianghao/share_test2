from PIL import ImageGrab

box = (10,10,500,500)
im = ImageGrab.grab(box)

im.save('test.png')
