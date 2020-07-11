from attendance.models import (
    Personnel, 
    Absence, 
    Status, 
    Parade
)
import logging
import sys

class ParadeStateHandler:
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
        for i in Absence.objects.filter(parade_id=self.parade_id):
            current_strength -= 1
        # return ('{}/{}'.format(current_strength,total_strength))
        return current_strength
    
    def calc_comd_strength(self):
        total_comd_strength = 0
        for i in Personnel.objects.filter(is_commander = True):
            total_comd_strength += 1
        current_comd_strength = total_comd_strength
        absent_comds = Absence.objects.filter(
            parade_id=self.parade_id).filter(personnel__is_commander=True)
        for i in absent_comds:
            current_comd_strength -= 1
        return current_comd_strength

    def calc_trpr_strength(self):
        total_trpr_strength = 0
        for i in Personnel.objects.filter(is_commander = False):
            total_trpr_strength += 1
        current_trpr_strength = total_trpr_strength
        absent_trprs = Absence.objects.filter(
            parade_id=self.parade_id).filter(personnel__is_commander=False)
        for i in absent_trprs:
            current_trpr_strength -= 1
        return current_trpr_strength

    def calc_absence(self):
        absentees = Absence.objects.filter(
            parade_id=self.parade_id).values()
        self.logger.info('ABSENTEES %s', absentees)
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
            'total_absent': int(self.parade.total_strength) - int(self.parade.current_strength),
            'total_attc': total_attc,
            'total_ma': total_ma,
            'total_leave': total_leave,
            'total_off': total_off,
            'total_other': total_other,
        }
        return data

    def get_parade_overview(self):
        absentees = Absence.objects.filter(
            parade_id=self.parade_id).values()
        card_data = []
        for abs in absentees:
            personnel = Personnel.objects.get(
                        id=int(abs['personnel_id']))
            data = {
                'name': personnel.name,
                'rank': personnel.rank,
                'platoon': personnel.platoon,
                'is_mc': abs['is_MC'],
                'is_ma': abs['is_MA'],
                'is_leave': abs['is_leave'],
                'is_off': abs['is_off'],
                'is_other': abs['is_other'],
                'remarks': abs['remarks'],
            }
            self.logger.info('DATA %s', data )
            card_data.append(data)
            self.logger.info('CARD DATA %s', card_data )
        return card_data

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


def add_new_card(parade_id, name, remarks, reason):
    logger = logging.getLogger(__name__)
    # transaction.set_autocommit(False)
    try:
        try:
            personnel_obj = Personnel.objects.get(
                name = name
            )
        except:
            raise Exception('Personnel does not exist in database')

        if name == '' or name == None:
            raise Exception('Name not provided')
        if reason == '' or reason == None:
            raise Exception('Reason for absence not provided')
        
        absentee = Absence(
            personnel = personnel_obj,
            parade_id = parade_id,
            remarks = remarks,
        )
        if reason == 'MA':
            absentee.is_MA = True
        elif reason == 'MC':
            absentee.is_MC = True
        elif reason == 'Off':
            absentee.is_off = True
        elif reason == 'Leave':
            absentee.is_leave = True
        elif reason == 'Others':
            absentee.is_other = True
        else:
            pass
        logger.info('SAVING NOW')
        absentee.save()
        logger.info('ABSENTEE INSTANCE %s', absentee)

        parade_instance = ParadeStateHandler(parade_id)
        parade_instance.update_parade_instance()

    except Exception as identifier:
        raise Exception(identifier.args[0])