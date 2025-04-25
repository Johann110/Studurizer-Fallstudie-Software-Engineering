import os

from django.http import JsonResponse

from material.models import Material

# Quelle: Codegenerierung mit ChatGPT
def delete_material(request, materialId):
    print("Received delete request for ID:", materialId)
    try:
        material = Material.objects.get(pk=materialId)
        if material.file:
            file_path = material.file.path
            if os.path.isfile(file_path):
                os.remove(file_path)
        material.delete()
        return JsonResponse({'success': True})
    except Material.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
# Ende der Generierung