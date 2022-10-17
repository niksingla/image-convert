from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import FileUploadForm
from .models import FileUpload
from PIL import Image
import os

def index(request):
    return render(request, 'index.html', {'form':FileUploadForm()})

def type_validation():
    pass

def png_to_jpg(file,name):
    print('COnverting image from PNG to JPG')
    im = Image.open(file)
    image = im.convert('RGB')
    new_name = name.replace('.png', '.jpg')
    image.save(f"media/uploads/converted/{new_name}")
    im_path = f'/uploads/converted/{new_name}'
    return im_path
def jpg_to_png(file,name):
    print('COnverting image from JPG to PNG')
    im = Image.open(file)
    image = im.convert('RGB')
    new_name = name.replace('.jpg', '.png')
    image.save(f"media/uploads/converted/{new_name}")
    im_path = f'/uploads/converted/{new_name}'
    return im_path
def jpeg_to_png(file,name):
    print('COnverting image from JPEG to PNG ', name)
    im = Image.open(file)
    image = im.convert('RGB')
    new_name = name.replace('.jpeg', '.png')
    image.save(f"media/uploads/converted/{new_name}")
    im_path = f'/uploads/converted/{new_name}'
    return im_path
def unknown_to_png(file,name, content_type):
    print(f'Converting image from {content_type} to PNG ')
    im = Image.open(file)
    image = im.convert('RGB')
    new_name = name.replace(f'.{content_type}', '.png')
    image.save(f"media/uploads/converted/{new_name}")
    im_path = f'/uploads/converted/{new_name}'
    return im_path
def unknown_to_jpg(file,name, content_type):
    print(f'Converting image from {content_type} to JPG ')
    im = Image.open(file)
    image = im.convert('RGB')
    new_name = name.replace(f'.{content_type}', '.jpg')
    image.save(f"media/uploads/converted/{new_name}")
    im_path = f'/uploads/converted/{new_name}'
    return im_path
def unknown_to_webp(file,name, content_type):
    print(f'Converting image from {content_type} to WEBP ')
    im = Image.open(file)
    image = im.convert('RGB')
    new_name = name.replace(f'.{content_type}', '.webp')
    image.save(f"media/uploads/converted/{new_name}")
    im_path = f'/uploads/converted/{new_name}'
    return im_path


def ajax_req(request):
    if request.method == 'POST':
        print('desired type: ', request.POST['convert_to'])
        print('File type: ',(request.FILES['file_field'].content_type))
        try:
            file = request.FILES['file_field'].file
            isImage = ((request.FILES['file_field'].content_type).split('/')[0] == 'image')
            print('Image validity: ',isImage)
            
            isImage = True
            if not isImage:
                return HttpResponse('Uploaded file is not a valid image...')
            else:
                desired_type = request.POST['convert_to']
                try:
                    content_type = (os.path.splitext(str(request.FILES['file_field'].name))[1]).split('.')[1]
                except:
                    content_type = (request.FILES['file_field'].content_type).split('/')[1]
                name = str(request.FILES['file_field'].name)
                if content_type == 'png' and desired_type == 'jpg':
                    rendered_image = png_to_jpg(file, name)
                    to_type = 'jpg'
                elif content_type == 'jpg' and desired_type == 'png':
                    rendered_image = jpg_to_png(file, name)
                    to_type = 'png'
                elif content_type == 'jpeg' and desired_type == 'png':
                    rendered_image = jpeg_to_png(file, name)
                    to_type = 'png'
                elif desired_type=='png':   
                    rendered_image = unknown_to_png(file, name, content_type)
                    to_type = 'png'
                elif desired_type=='jpg':   
                    rendered_image = unknown_to_jpg(file, name, content_type)
                    to_type = 'jpg'
                elif desired_type=='webp':   
                    rendered_image = unknown_to_webp(file, name, content_type)
                    to_type = 'webp'

                image_in_db = FileUpload.objects.filter(image_name=name) 
                if image_in_db.exists():
                    image_in_db.update(image_name=name)
                    print('DB Updated!')
                else:
                    FileUpload.objects.create(image_name=name) 
                    print('DB Created!')
                ins = FileUpload.objects.get(image_name=name)
                form = FileUploadForm(request.POST, instance=ins, initial={"file_field":rendered_image})
                if form.is_valid:
                    form.save()
                    rendered_path = '/media' + rendered_image
                    json_data = {'success':{'file':rendered_path, 'from':content_type, 'to':to_type}}
                    return JsonResponse(json_data)
        except Exception as e:
            print('Exception occured: ', e)
            return HttpResponse('Convert Failed!')