from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from openai import AzureOpenAI
import json
from django.conf import settings
from .models import GeneratedImage

def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        
        client = AzureOpenAI(
            api_version="2024-05-01-preview",
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
        )

        result = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1
        )

        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        
        GeneratedImage.objects.create(prompt=prompt, image_url=image_url)
        
        return render(request, 'image_generator/result.html', {'image_url': image_url})
    
    return render(request, 'image_generator/form.html')