import os
from PIL import Image

SITE_TITLE = 'Mountain Quest Massachusetts'
UP_INDEX = '../index.html'
IMAGE_PATH = 'img'
THUMBNAIL_PATH = 'thumbs'


def gen_thumbs():
    base_width = 300
    for path in os.listdir('../' + IMAGE_PATH):
        img = Image.open('../' + IMAGE_PATH + '/'+path)
        w_percent = (base_width/float(img.size[0]))
        h_size = int((float(img.size[1])*float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
        img.save('../' + THUMBNAIL_PATH + '/' + path)

def gen_thumbs_2():
    base_height = 300
    for path in os.listdir('../' + IMAGE_PATH):
        img = Image.open('../' + IMAGE_PATH + '/'+path)
        h_percent = (base_height/float(img.size[1]))
        w_size = int((float(img.size[0])*float(h_percent)))
        img = img.resize((w_size, base_height), Image.ANTIALIAS)
        img.save('../' + THUMBNAIL_PATH + '/' + path)


def read_properties_file(path):
    props = {}
    with open(path, "rt") as f:
        for line in f:
            l = line.strip()
            if l:
                key_value = l.split("=")
                key = key_value[0].strip()
                value = "=".join(key_value[1:]).strip().strip('"')
                if not props.get(key):
                    props[key] = []
                    props[key].append(value)
                else:
                    props[key].append(value)
    return props


def get_font():
    return "<link href='https://fonts.googleapis.com/css?family=Lora' rel='stylesheet' type='text/css'>\n"


def get_css(up):
    if up:
        return '<link rel="stylesheet" href="../css/base.css">\n'
    else:
        return '<link rel="stylesheet" href="./css/base.css">\n'


def open_tag(tag):
    return '<' + tag + '>\n'


def close_tag(tag):
    return '</' + tag + '>\n'


def get_tag(tag, content=''):
    return open_tag(tag) + content + close_tag(tag)


def get_open_a_tag(href):
    return '<a href='+href+'>'


def get_link(href, content):
    return get_open_a_tag(href) + content + close_tag('a')


def get_place_img(img_name, place_name):
    thumb = img_name.replace(IMAGE_PATH, THUMBNAIL_PATH)
    return '<a href="' + img_name + '" target="blank"><img src="' + thumb + '" alt="'+place_name+'" class="thumbnail"/img></a>'


def get_head():
    return "<head>\n\
    <!-- Global site tag (gtag.js) - Google Analytics -->\n\
    <script async src='https://www.googletagmanager.com/gtag/js?id=UA-125169686-1'></script>\n\
    <script>\n\
    window.dataLayer = window.dataLayer || [];\n\
    function gtag(){dataLayer.push(arguments);}\n\
    gtag('js', new Date());\n\
    gtag('config', 'UA-125169686-1');\n\
    </script>\n\
    <title>" + SITE_TITLE + "</title>\n\
    </head>\n"

# def get_head():
#     return "<head>\n\
#     <!-- Global site tag (gtag.js) - Google Analytics -->\n\
#     <script async src='https://www.googletagmanager.com/gtag/js?id=UA-124818630-1'></script>\n\
#     <script>\n\
#     window.dataLayer = window.dataLayer || [];\n\
#     function gtag(){dataLayer.push(arguments);}\n\
#     gtag('js', new Date());\n\
#     gtag('config', 'UA-124818630-1');\n\
#     </script>\n\
#     <script async src='//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'></script>\n\
#     <script>\n\
#     (adsbygoogle = window.adsbygoogle || []).push({\n\
#     google_ad_client: 'ca-pub-8138649344789982',\n\
#     enable_page_level_ads: true\n\
#     });\n\
#     </script>\n\
#     <title>" + SITE_TITLE + "</title>\n\
#     </head>\n"


def write_line(f, line):
    f.write(line + '\n')


def write_index(all_props, name_to_images):
    with open("../index.html", 'w') as f:
        f.write(get_css(False))
        f.write(get_font())

        f.write(get_head())

        write_line(f, open_tag('body'))

        # Site title
        write_line(f, get_tag('h1', get_link('./', SITE_TITLE)))

        write_line(f, get_tag('p', 'Amy and Matt are going to hike every mountain and reach every peak in Massachusetts. This is where we are tracking our progress.'))



        counties_to_props_list = {}
        for props in all_props:
            county = props.get('county')[0]
            if not counties_to_props_list.get(county):
                counties_to_props_list[county] = []
                counties_to_props_list[county].append(props)
            else:
                counties_to_props_list[county].append(props)

        write_line(f, get_tag('h2', "Peaks We Have Hiked"))

        write_line(f, open_tag('ul'))
        for county, props_list in sorted(counties_to_props_list.items()):
            write_line(f, get_tag('li', county + ', MA'))

            write_line(f, open_tag('ul'))

            for props in props_list:
                if props.get('hiked')[0] == 'true':
                    write_line(f, get_tag('li', get_link('./m/'+props.get('fname'), props.get('name')[0] + ' ' + props.get('height')[0] + "'")))
            write_line(f, close_tag('ul'))
        write_line(f, close_tag('ul'))

        name_image_pairs = []
        for name, images in name_to_images.items():
            for image in images:
                name_image_pairs.append([name, image])

        write_line(f, '<div id="random_images" style="text-align: center;"></div>')
        write_line(f, '<script>')
        write_line(f, 'function getRandom(arr, n) { \
        var result = new Array(n), \
             len = arr.length, \
           taken = new Array(len); \
        if (n > len) \
            throw new RangeError("getRandom: more elements taken than available"); \
        while (n--) { \
            var x = Math.floor(Math.random() * len); \
            result[n] = arr[x in taken ? taken[x] : x]; \
            taken[x] = --len in taken ? taken[len] : len; \
        } \
        return result; \
        }')
        write_line(f, 'var name_image_pairs=getRandom('+str(name_image_pairs)+', 7);')
        write_line(f, 'var element=document.getElementById("random_images");')
        write_line(f, 'for (var i = 0; i < name_image_pairs.length; i++) {')
        write_line(f, 'var link = document.createElement("a");')
        write_line(f, 'var href = "m/"+name_image_pairs[i][0]+".html";')
        write_line(f, 'link.href = href')
        write_line(f, 'var image = document.createElement("img");')
        write_line(f, 'image.src = "thumbs/"+name_image_pairs[i][1];')
        write_line(f, 'image.classList.add("thumbnail")')
        write_line(f, 'link.appendChild(image);')
        write_line(f, 'element.appendChild(link);')
        write_line(f, '}')
        # write_line(f, 'var featured_haunting=featured_hauntings[Math.floor(Math.random()*featured_hauntings.length)];')
        # write_line(f, 'var link=document.createElement("a");')
        # write_line(f, 'link.href=featured_haunting.url;')
        # write_line(f, 'var title=document.createElement("h3");')
        # write_line(f, 'var node=document.createTextNode(featured_haunting.title + ", " + featured_haunting.place);')
        # write_line(f, 'link.appendChild(node);')
        # write_line(f, 'title.appendChild(link);')
        # write_line(f, 'var element=document.getElementById("featured_haunting");')
        # write_line(f, 'element.appendChild(title);')
        # write_line(f, 'var image_link=document.createElement("a");')
        # write_line(f, 'image_link.href=featured_haunting.url;')
        # write_line(f, 'var image_src="tgimg/"+featured_haunting.images[Math.floor(Math.random()*featured_haunting.images.length)];')
        # write_line(f, 'var image = document.createElement("img");')
        # write_line(f, 'image.src = image_src;')
        # write_line(f, 'image.height = "150";')
        # write_line(f, 'image_link.appendChild(image);')
        # write_line(f, 'element.appendChild(image_link);')
        write_line(f, '</script>')

        write_line(f, get_tag('h2', "Remaining Peaks"))

        write_line(f, open_tag('ul'))
        for county, props_list in sorted(counties_to_props_list.items()):
            write_line(f, get_tag('li', county + ', MA'))

            write_line(f, open_tag('ul'))

            for props in props_list:
                if props.get('hiked')[0] == 'false':
                    write_line(f, get_tag('li', get_link('./m/'+props.get('fname'), props.get('name')[0] + ' ' + props.get('height')[0] + "'")))
            write_line(f, close_tag('ul'))
        write_line(f, close_tag('ul'))

        write_line(f, get_tag('h2', 'All Peaks'))

        write_line(f, open_tag('ul'))
        for county, props_list in sorted(counties_to_props_list.items()):
            write_line(f, get_tag('li', county + ', MA'))

            write_line(f, open_tag('ul'))

            for props in props_list:
                write_line(f, get_tag('li', get_link('./m/'+props.get('fname'), props.get('name')[0] + ' ' + props.get('height')[0] + "'")))
            write_line(f, close_tag('ul'))
            # write_city(city, props_list)

        write_line(f, close_tag('ul'))

        write_line(f, open_tag('footer'))
        write_line(f, close_tag('footer'))

        write_line(f, close_tag('body'))


def write_page(f_name, props, images):
    f_name = f_name.replace('properties', 'html')
    with open("../m/" + f_name, 'w') as f:
        f.write(get_css(True))
        f.write(get_font())

        f.write(get_head())

        write_line(f, open_tag('body'))

        # Site title
        write_line(f, get_tag('h1', get_link(UP_INDEX, SITE_TITLE)))

        # Page title
        write_line(f, get_tag('h2', get_link('./'+f_name, props.get('name')[0])))

        # Location
        write_line(f, get_tag('p', props.get('county')[0] + ', MA'))

        if props.get('date'):
            write_line(f, get_tag('p', "Date Hiked: " + props.get('date')[0]))

        if props.get('description'):
            write_line(f, get_tag('h3', "Description"))
            for paragraph in props.get('description'):
                write_line(f, get_tag('p', paragraph))


        # Images
        if len(images) > 0:
            write_line(f, get_tag('h3', 'Images'))
            for image in images:
                write_line(f, get_place_img('../'+IMAGE_PATH+'/'+image, props.get('name')[0]))

        # Sources title
        # write_line(f, get_tag('h3', 'Sources'))

        # write_line(f, open_tag('ul'))

        # source_props = props.get("source")

        # for source in source_props:
        #    write_line(f, get_tag('li', get_link(source.split('>')[1], source.split('>')[0])))

        # write_line(f, close_tag('ul'))

        write_line(f, open_tag('footer'))
        write_line(f, open_tag('br'))
        write_line(f, get_link('..', 'Back to ' + SITE_TITLE))
        write_line(f, close_tag('footer'))

        write_line(f, close_tag('body'))


def write_city(city_name, all_location_props):
    with open("../c/" + city_name.lower() + '.html', 'w') as f:
        f.write(get_css(True))
        f.write(get_font())

        f.write(get_head())

        write_line(f, open_tag('body'))

        # Site title
        write_line(f, get_tag('h1', get_link(UP_INDEX, SITE_TITLE)))

        # Page title
        write_line(f, get_tag('h2', get_link('./'+city_name.lower() + '.html', city_name.title() + ', MA')))

        write_line(f, get_tag('h3', "Mountains"))

        write_line(f, open_tag('ul'))

        for props in all_location_props:
            write_line(f, get_tag('li', get_link('../m/'+props.get('fname'), props.get('title')[0])))

        write_line(f, close_tag('ul'))

        write_line(f, open_tag('footer'))
        write_line(f, open_tag('br'))
        write_line(f, get_link('..', 'Back to ' + SITE_TITLE))
        write_line(f, close_tag('footer'))

        write_line(f, close_tag('body'))

if __name__ == '__main__':
    gen_thumbs_2()
    all_props = []
    name_to_images = {}
    for name in os.listdir("../input"):
        name_to_images[name.replace('.properties', '')] = []
    for img_name in os.listdir('../'+IMAGE_PATH):
        for place_name in name_to_images.keys():
            if img_name.find(place_name) >= 0:
                name_to_images[place_name].append(img_name)

    for name in os.listdir("../input"):
        props = read_properties_file("../input/" + name)
        props['fname'] = name.replace('.properties', '.html')
        all_props.append(props);
        write_page(name, props, name_to_images[name.replace('.properties', '')])

    write_index(all_props, name_to_images)
