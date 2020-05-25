from attendance.models import (
    Personnel, 
    Absence, 
    Status, 
    Parade
)


def calc_coy_total():
    strength = 0
    for i in Personnel.objects.all():
        strength += 1
    return strength

def calc_coy_current(parade_id):
    total_strength = calc_coy_total()
    current_strength = total_strength
    for i in Absence.objects.all().filter(id=parade_id):
        current_strength -= 1
    return ('{}/{}'.format(current_strength,total_strength))


def calc_plt_total(platoon):
    strength = 0 
    for i in Personnel.objects.all().filter(platoon=platoon):
        strength += 1

def calc_plt_current(platoon, parade_id):
    total_strength = calc_plt_total(platoon)
    current_strength = total_strength
    for i in Absence.objects.all().filter(id=parade_id).filter(trooper__platoon=platoon):
        current_strength -= 1
    return ('{}/{}'.format(current_strength,total_strength))



