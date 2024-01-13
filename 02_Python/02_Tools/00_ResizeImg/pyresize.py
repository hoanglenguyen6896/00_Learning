from PIL import Image # equal "import PIL.Image", you can't import PIL then invoke PIL.Image
from PIL.ExifTags import TAGS
import piexif
import os
from unidecode import unidecode
import shutil
import argparse

TARGET_WIDTH = 750

IMG_EXIF_DES = {
    "Title":          270,   # Title and subject encode utf-8
    "Subject":        40095, # Subject
    "Rating":         18246, # Rating1 int
    "RatingPercent":  18249, # Rating2 int
    "Keywords":       40094, # Tags encode utf-16
    "Comment":        40092, # Commentsencode utf-16
    "Author_str":     315,   # Author string encode byte
    "Author_utf16":   40093, # Author string encode utf-16
}

SCRIPT_ABS_PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

IN_IMG_DIR = SCRIPT_ABS_PATH + "/IN_DIR/"
OUT_IMG_DIR = SCRIPT_ABS_PATH + "/OUT_DIR/"
class all_image_stuff:
    def __init__(self, input_dir, output_dir, author):
        self.author = author
        self.indir = input_dir
        if not (os.path.isdir(self.indir)):
            print("Image unput directory does not exist!")
            exit(-1)
        self.outdir = output_dir
        if not (os.path.isdir(self.outdir)):
            print("Creating output directory " + self.outdir)
            os.mkdir(self.outdir)
        elif len(os.listdir(self.outdir)) != 0:
            print("Empty", self.outdir)
            for _dir in os.listdir(self.outdir):
                # print(_dir)
                try:
                    shutil.rmtree(self.outdir + _dir)
                except NotADirectoryError as __tmp:
                    print("Skip", _dir)
                except Exception as _tmp:
                    print("Something wrong when clean", self.outdir, _tmp)
        self.all_dir = []
        # list all dir in input directory
        _tmp_all_dir = os.listdir(self.indir)
        for _dir in _tmp_all_dir:
            if (os.path.isdir(self.indir + _dir)):
                # Get subdir only
                self.all_dir.append(_dir)
                if not os.path.isdir(self.outdir + _dir):
                    os.mkdir(self.outdir + _dir)
                else:
                    print("Output directory should be empty!!!")
                    exit(-1)
                pass
            else:
                pass
        if len(self.all_dir) == 0:
            print("Input dir is empty!!!")
            exit(-1)
        pass

    def _convert_utf16_to_hex_exif(self, target_str):
        # Get utf-16 of string
        # Append ending to table_result fffeabcd > abcd
        table_word_16 = []
        for item in target_str:
            table_word_16.append(item.encode('utf-16').hex().replace('fffe',''))
        # Split into string size 2
        table_word_8 = []
        for word16 in table_word_16:
            table_word_8.append(word16[0:2])
            table_word_8.append(word16[2:])
        # Convert string size 2 to hex int
        table_result = []
        for word8 in table_word_8:
            table_result.append(int(word8, 16))
        return table_result


    # Add description (title, subject, rate, tags, comment) to image
    def _set_img_des_from_exif(self, _dir_name, _author, exifdata):
        # remove exif data if exist as some of them may contain can't parse info
        # print(exifdata)
        focus_key = self._convert_utf16_to_hex_exif(_dir_name)
        exifdata['Exif'] = {}
        exifdata['0th'][IMG_EXIF_DES["Title"]] = str.encode(_dir_name) # Set both title and subject
        exifdata['0th'][IMG_EXIF_DES["Rating"]] = 5  # Set rating
        exifdata['0th'][IMG_EXIF_DES["RatingPercent"]] = 99 # Set rating, need both
        focus_key.extend((0, 0))
        exifdata['0th'][IMG_EXIF_DES["Keywords"]] = tuple(focus_key)
        exifdata['0th'][IMG_EXIF_DES["Comment"]] = tuple(focus_key)
        author = self._convert_utf16_to_hex_exif(_author)
        author.extend((0, 0))
        exifdata['0th'][IMG_EXIF_DES["Author_str"]] = str.encode(_author)
        exifdata['0th'][IMG_EXIF_DES["Author_utf16"]] = tuple(author)
        # print(exifdata)
        return exifdata

    # Resize a single image
    def _resize_img_sub(self, _dir_name, in_file, out_file):
        # print(in_file, out_file)
        with Image.open(in_file) as image:
            image = Image.open(in_file)
            if image.mode != "RGB":
                rgb_img = image.convert("RGB")
            else:
                rgb_img = image
            # Enlarge
            if rgb_img.width < TARGET_WIDTH:
                _ratio = TARGET_WIDTH/rgb_img.width
                rgb_img = rgb_img.resize((TARGET_WIDTH, int(_ratio*rgb_img.height)), Image.Resampling.LANCZOS)
            # Reduce
            elif rgb_img.width > TARGET_WIDTH:
                rgb_img.thumbnail((TARGET_WIDTH, TARGET_WIDTH))

            try:
                exifdata = piexif.load(rgb_img.info["exif"])
            except KeyError:
                exifdata = {'0th': {}, 'Exif': {}, 'GPS': {}, 'Interop': {}, '1st': {}, 'thumbnail': None}
            except:
                print("Something wrong with exif!!!")
                exit(-1)
            # Dunp human readable exif to image exif
            exif_bytes = piexif.dump(self._set_img_des_from_exif(_dir_name, self.author, exifdata))
            # print(exif_bytes)
            # Save image with dumped exif
            rgb_img.save(out_file, exif=exif_bytes)

    # Resize all images in a single directory
    def _resize_img_in_a_dir(self, _dir_name, _full_relative_input_dir, _full_relative_output_dir):
        for _img in os.listdir(_full_relative_input_dir):
            _in = _full_relative_input_dir + "/" + _img
            _out = _full_relative_output_dir + "/" + unidecode(_dir_name.replace(" ", "-").lower()) + " (" + _img.split(".")[0] + ")." + _img.split(".")[1]
            self._resize_img_sub(_dir_name, _in, _out)

    # Resize all images in all subdirectories of input directory
    def _resize_all(self):
        for _dir_name in self.all_dir:
            _full_relative_input_dir = self.indir + _dir_name
            _full_relative_output_dir = self.outdir + _dir_name
            self._resize_img_in_a_dir(_dir_name, _full_relative_input_dir, _full_relative_output_dir)

if __name__ == '__main__':
    def argparse_init():
        parser = argparse.ArgumentParser(
                    prog=__file__,
                    description='Resize all images in subdir of IN_DIR, output to OUT_DIR')
        parser.add_argument('-i', '--input', default=IN_IMG_DIR,
                            help="Path to input directory where you save all images in subdirs")
        parser.add_argument('-o', '--output', default=OUT_IMG_DIR,
                            help="Path to output directory")
        parser.add_argument('-a', '--author', default="",
                            help="Author")
        return parser.parse_args()
    argv = argparse_init()

    tmp = all_image_stuff(argv.input, argv.output, argv.author)
    tmp._resize_all()
