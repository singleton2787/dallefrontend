from django.shortcuts import render
from openai import AzureOpenAI
import json
from django.conf import settings
from .models import GeneratedImage

def generate_image(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        style = request.POST.get('style')
        
        client = AzureOpenAI(
            api_version="2024-05-01-preview",
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
        )

        full_prompt = f"{style} style: {prompt}"  # Fixed string literal

        try:
            result = client.images.generate(
                model="dall-e-2",
                prompt=full_prompt,  # Use the full_prompt here
                n=1
            )

            image_url = result.data[0].url  # Simplified access to image URL
            
            GeneratedImage.objects.create(prompt=full_prompt, image_url=image_url)
            
            return render(request, 'image_generator/result.html', {'image_url': image_url, 'prompt': full_prompt})
        except Exception as e:
            # Log the error (you might want to use Python's logging module for this)
            print(f"Error generating image: {str(e)}")
            return render(request, 'image_generator/form.html', {'error': 'An error occurred while generating the image.'})
    
    return render(request, 'image_generator/form.html')