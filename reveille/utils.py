from attendance.models import (
    Personnel, 
    Absence, 
    Status, 
    Parade
)
import logging
import sys

class ParadeStrengthCalculator:
    logger = logging.getLogger(__name__)
    def __init__(self, parade_id):
        parade = Parade.objects.get(id = parade_id)
        self.parade = parade
        self.parade_id = parade_id

    def calc_coy_total(self):
        strength = 0
        for i in Personnel.objects.all():
            strength += 1
        return strength

    def calc_coy_current(self):
        total_strength = self.calc_coy_total()
        current_strength = total_strength
        for i in Absence.objects.filter(id=self.parade_id):
            current_strength -= 1
        # return ('{}/{}'.format(current_strength,total_strength))
        return current_strength
    
    def calc_comd_strength(self):
        total_comd_strength = 0
        for i in Personnel.objects.filter(is_commander = True):
            total_comd_strength += 1
        current_comd_strength = total_comd_strength
        absent_comds = Absence.objects.filter(
            id=self.parade_id).filter(personnel__is_commander=True)
        for i in absent_comds:
            current_comd_strength -= 1
        return current_comd_strength

    def calc_trpr_strength(self):
        total_trpr_strength = 0
        for i in Personnel.objects.filter(is_commander = False):
            total_trpr_strength += 1
        current_trpr_strength = total_trpr_strength
        absent_trprs = Absence.objects.filter(
            id=self.parade_id).filter(personnel__is_commander=False)
        for i in absent_trprs:
            current_trpr_strength -= 1
        return current_trpr_strength

    def calc_absence(self):
        absentees = Absence.objects.all().filter(id=self.parade_id)
        no_absentees = True
        if len(absentees) == 0:
            no_absentees = False
        else:
            total_attc = 0
            total_ma = 0
            total_leave = 0
            total_off = 0
            total_other = 0
            for abs in absentees:
                if abs['is_MC']:
                    total_attc += 1
                elif abs['is_MA']:
                    total_ma += 1
                elif abs['is_leave']:
                    total_leave += 1
                elif abs['is_off']:
                    total_off += 1
                elif abs['is_other']:
                    total_other += 1
                else:
                    pass
        data = { 
            'no_absentees': no_absentees,
            'total_absent': int(self.calc_coy_total) - int(self.calc_coy_current),
            'total_attc': total_attc,
            'total_ma': total_ma,
            'total_leave': total_leave,
            'total_off': total_off,
            'total_other': total_other,
        }


    def update_parade_instance(self):
        parade = self.parade
        parade.commander_strength = int(self.calc_comd_strength())
        parade.personnel_strength = int(self.calc_trpr_strength())
        parade.current_strength = int(self.calc_coy_current())
        parade.total_strength = int(self.calc_coy_total())
        parade.save()
'''
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
'''

    