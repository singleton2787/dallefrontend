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

        if style == 'storyboard':
            num_images = int(request.POST.get('num_images', 2))  # Default to 2 if not provided
            num_images = min(max(num_images, 2), 6)  # Ensure it's between 2 and 6
            full_prompt = f"{prompt} and create a storyboard of {num_images} images with the same character or scene in different poses or situations"
        elif style == 'custom':
            custom_style = "and a seed of 8975398754985, the cinematic lighting and depth of field from a film noir, combined with the vibrant colors and features of a Disney film"
            full_prompt = f"{prompt}, {custom_style}"
        elif style == 'none':
            full_prompt = prompt  # Use the prompt as-is without any style prefix
        else:
            full_prompt = f"{style} style: {prompt}"

        try:
            result = client.images.generate(
                model="dall-e-3",
                prompt=full_prompt,
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