def total_carro(request):
    total=0
    if request.user.is_authenticated:
        try:
            for key, value in request.session["carro"].items():
                total=total+float(value["precio"])
        except:
            pass
    else:
        total="Debes hacer login" 
    return {"total_carro":total}
    