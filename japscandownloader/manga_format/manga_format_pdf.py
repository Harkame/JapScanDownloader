from PIL import Image
import glob

def create_pdf(path, file_name):
    images = []
    for filename in glob.glob(path + '*.jpg'):
        images.append(Image.open(filename))

    images_to_pdf(images);

def images_to_pdf(images):
        for image_index in range(len(images) - 1):
            print(image_index);

#    im1.save(file_name, "PDF" ,resolution=100.0, save_all=True, append_images=images)

create_pdf('./', 'toto')
