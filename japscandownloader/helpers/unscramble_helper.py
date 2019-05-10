import settings.settings as settings

from PIL import Image

def unscramble_image(scrambled_image, image_full_path):
    input_image = Image.open(scrambled_image)
    temp = Image.new("RGB", input_image.size)
    output_image = Image.new("RGB", input_image.size)
    for x in range(0, input_image.width, 200):
        col1 = input_image.crop((x, 0, x + 100, input_image.height))
        if (x + 200) <= input_image.width:
            col2 = input_image.crop((x + 100, 0, x + 200, input_image.height))
            temp.paste(col1, (x + 100, 0))
            temp.paste(col2, (x, 0))
        else:
            col2 = input_image.crop((x + 100, 0, input_image.width, input_image.height))
            temp.paste(col1, (x, 0))
            temp.paste(col2, (x + 100, 0))
    for y in range(0, temp.height, 200):
        row1 = temp.crop((0, y, temp.width, y + 100))
        if (y + 200) <= temp.height:
            row2 = temp.crop((0, y + 100, temp.width, y + 200))
            output_image.paste(row1, (0, y + 100))
            output_image.paste(row2, (0, y))
        else:
            row2 = temp.crop((0, y + 100, temp.width, temp.height))
            output_image.paste(row1, (0, y))
            output_image.paste(row2, (0, y + 100))
    output_image.save(image_full_path)

def is_scrambled_scripts(page):
    scripts = page.find('head').find_all('script')

    if len(scripts) > 9:
        script = scripts[8]

        settings.logger.debug('script : %s', script)

        if '_' in str(script):
            settings.logger.debug('scrambled image')
            return True

    return False

# Old way to detect scrambling
def is_scrambled_clel(image_url):
    if 'clel' in image_url:
        settings.logger.debug('scrambled image')
        return True

    return False
