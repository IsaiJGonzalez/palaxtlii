from django.shortcuts import render,redirect
from core.decorators import gerente_required, ventas_required, cajero_required
import firebase_service as fs
from django.http import JsonResponse

@gerente_required
# Create your views here.
def codigos(request):
    
    codigos_dict = fs.obtener_codigos()
    categorias_dict = fs.obtener_categorias()

    codigos = list(codigos_dict.values()) if codigos_dict else []
    categorias = list(categorias_dict.values()) if categorias_dict else []


    if request.method == 'POST':
        codigo = int(request.POST.get('codigo'))
        fs.agregar_codigos(codigo)
        return redirect('codigos')
    
    context = {
        'codigos' : codigos,
        'cats' : categorias,
    }

    return render(request,'codigo.html',context)


@gerente_required
def agregar_cat(request):
    
    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        fs.add_cat(categoria)
        return JsonResponse({'mensaje': 'Categoría añadida correctamente'}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)