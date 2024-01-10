from PIL import Image # equal "import PIL.Image", you can't import PIL then invoke PIL.Image
from PIL.ExifTags import TAGS
import piexif
import os
from unidecode import unidecode
import shutil
SCRIPT_ABS_PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

IN_IMG_DIR = SCRIPT_ABS_PATH + "/IN_DIR/"
if not (os.path.isdir(IN_IMG_DIR)):
    print("Image dir does not exist!")
    exit(-1)
OUT_IMG_DIR = SCRIPT_ABS_PATH + "/OUT_DIR/"
if not (os.path.isdir(OUT_IMG_DIR)):
    print("Creating output directory " + OUT_IMG_DIR)
    os.mkdir(OUT_IMG_DIR)
elif len(os.listdir(OUT_IMG_DIR)) != 0:
    print("Empty out dir")
    print(os.listdir(OUT_IMG_DIR))
    for _dir in os.listdir(OUT_IMG_DIR):
        # print(_dir)
        shutil.rmtree(OUT_IMG_DIR + _dir)


class all_image_stuff:
    def __init__(self):
        self.all_dir = []
        _tmp_all_dir = os.listdir(IN_IMG_DIR)
        for _dir in _tmp_all_dir:
            # print(_dir, os.path.isdir(IN_IMG_DIR + _dir))
            if (os.path.isdir(IN_IMG_DIR + _dir)):
                # print(f"{_dir} is dir")
                self.all_dir.append(_dir)
                pass
            else:
                # self.all_dir.remove(_dir)
                # print(f"{_dir} is not dir")
                pass
        if len(self.all_dir) == 0:
            print("Input dir is empty!!!")
            exit(-1)
        # self.all_dir_minus =  [unidecode(x.replace(" ", "-")).lower() for x in self.all_dir]
        pass
    def list_all_image(self):
        self.all_img_in_dir = []
        for _dir in self.all_dir:
            try:
                self.all_img_in_dir.append(os.listdir(IN_IMG_DIR + _dir))
                if not os.path.isdir(OUT_IMG_DIR + _dir):
                    os.mkdir(OUT_IMG_DIR + _dir)
                else:
                    print("Output directory should be empty!!!")
                    exit(-1)
            except NotADirectoryError:
                pass
            except Exception as tmp:
                print("Something wrong!!!")
                print(tmp)
                exit(-1)
    def _resize_img_sub(self, _dir_name, in_file, out_file):
        # print(in_file, out_file)
        image = Image.open(in_file)
        if image.mode != "RGB":
            rgb_img = image.convert("RGB")
        else:
            rgb_img = image
        rgb_img.thumbnail((750,750))

        img_des = {
            270: "Title", # Title and subject encode utf-8
            40095: "Subject", # Subject
            18246: "Rating", # Rating1 int
            18249: "RatingPercent", # Rating2 int
            40094: "Keywords", # Tags encode utf-16
            40092: "Comment", #Commentsencode utf-16
        }

        try:
            exifdata = piexif.load(rgb_img.info["exif"])
        except KeyError:
            exifdata = {'0th': {}, 'Exif': {}, 'GPS': {}, 'Interop': {}, '1st': {}, 'thumbnail': None}
        except:
            print("Something wrong with exif!!!")
            exit(-1)
        # print(exifdata['Exif'])
        # exit()
        exifdata['Exif'] = {}

        exifdata['0th'][270] = str.encode(_dir_name) # Set both title and subject
        exifdata['0th'][18246] = 5  # Set rating
        exifdata['0th'][18249] = 99 # Set rating, need both
        # Getutf-16 of string
        table_word_16 = []
        for item in _dir_name:
            table_word_16.append(item.encode('utf-16').hex().replace('fffe',''))

        table_word_8 = []
        for word16 in table_word_16:
            table_word_8.append(word16[0:2])
            table_word_8.append(word16[2:])

        table_result = []
        for word8 in table_word_8:
            table_result.append(int(word8, 16))
        # Append ending to  table_result
        table_result.extend((0, 0))
        exifdata['0th'][40094] = table_result
        exifdata['0th'][40092] = table_result

        exif_bytes = piexif.dump(exifdata)
        # rgb_img.save(out_file)
        rgb_img.save(out_file, exif=exif_bytes)
        image.close()
        rgb_img.close()
        # exit(-1)
    def _resize_img_in_a_dir(self, _dir_name, _full_relative_input_dir, _full_relative_output_dir):
        for _img in os.listdir(_full_relative_input_dir):
            _in = _full_relative_input_dir + "/" + _img
            _out = _full_relative_output_dir + "/" + unidecode(_dir_name.replace(" ", "-").lower()) + " (" + _img.split(".")[0] + ")." + _img.split(".")[1]
            self._resize_img_sub(_dir_name, _in, _out)
    def _resize_all(self):
        for _dir_name in self.all_dir:
            _full_relative_input_dir = IN_IMG_DIR + _dir_name
            _full_relative_output_dir = OUT_IMG_DIR + _dir_name
            self._resize_img_in_a_dir(_dir_name, _full_relative_input_dir, _full_relative_output_dir)

if __name__ == '__main__':
    tmp = all_image_stuff()
    tmp.list_all_image()
    tmp._resize_all()
