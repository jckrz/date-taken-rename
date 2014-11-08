from sys import argv
from os import listdir
from os.path import isfile, join
from PIL import Image
from datetime import datetime, timedelta
from shutil import copyfile

if len(argv) not in [3, 4]:
	print 'Usage: python {0} <src dir> <dst dir> [<shift seconds>]'.format(argv[0])
	exit(1)

src   = argv[1]
dst   = argv[2]
shift = timedelta(0, int(argv[3]) if len(argv) is 4 else 0)

for f in [f for f in listdir(src) if isfile(join(src,f))]:
	exif = Image.open(join(src,f))._getexif()
	try:
		taken = exif[36867]
	except:
		print '{0}: no exif info. Stopping.'.format(f)
		exit(2)
	taken = datetime.strptime(taken, '%Y:%m:%d %H:%M:%S') 
	taken += shift;
	taken = taken.strftime('%Y-%m-%d_%H-%M-%S')
	outpath = join(dst, '{0}_{1}'.format(taken, f))
	print '{0} --> {1}'.format(f, outpath)
	copyfile(join(src,f), outpath)
