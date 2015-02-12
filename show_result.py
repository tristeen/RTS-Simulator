from PIL import Image
import os
import time

dirnum = 0

#dot -Tsvg result/dir1/1 -o 1.svg
while True:
	dirnum += 1
	dirname = './result/dir%d'%dirnum
	if not os.path.isdir(dirname):
		break
	filenum = 0
	while True:
		try:
			filenum += 1
			filename = './%s/%d.png'%(dirname, filenum)
			im = Image.open(filename)
			im.show(title=filename)
			time.sleep(0.5)
		except IOError:
			break
	print 'press any key to continue'
	raw_input()
