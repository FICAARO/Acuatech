def total_carro(request):
    total=0
    """
    if request.user.is_authenticated:
        try:
            for key, value in request.session["carro"].items():
                total=total+float(value["precio"])
        except:
            pass
    else:
        total="No hay productos" 
    """
    try:
        for key, value in request.session["carro"].items():
            total=total+float(value["precio"])
    except:
        total="No hay productos"
    return {"total_carro":total}
    