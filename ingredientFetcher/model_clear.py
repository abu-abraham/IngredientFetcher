import models

def clear_all():
    p = models.Ingredients.objects.all()
    p.delete();
    p.save();

def view_all():
    p = models.Ingredients.objects.all()
    print p

clear_all()