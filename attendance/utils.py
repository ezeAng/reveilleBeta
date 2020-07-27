from .models import (
    Personnel, 
    Absence, 
    Status, 
    Parade,
    ParadePersonnel
)
import logging
import sys
from django.db import transaction


class ParadeStateHandler:
    logger = logging.getLogger(__name__)
    def __init__(self, parade_id):
        try:
            self.parade = Parade.objects.get(id = parade_id)
        except:
            raise Exception('Invalid parade_id')
        self.parade_id = parade_id

    def calc_coy_total(self):
        return len(ParadePersonnel.objects.filter(
            parade_id = self.parade_id))

    def calc_coy_current(self):
        return len(ParadePersonnel.objects.filter(
            parade_id = self.parade_id,
            is_absent=False))
    
    def calc_comd_strength(self):
        present_personnel = ParadePersonnel.objects.filter(
            parade_id = self.parade_id,
            is_absent=False).values()
        current_comd_strength = 0
        for person in present_personnel:
            is_comd = Personnel.objects.get(id=person['personnel_id']).is_commander
            if is_comd:
                current_comd_strength += 1
            else:
                pass
        return current_comd_strength

    def calc_trpr_strength(self):
        present_personnel = ParadePersonnel.objects.filter(
            parade_id = self.parade_id,
            is_absent=False).values()
        current_trpr_strength = 0
        for person in present_personnel:
            is_comd = Personnel.objects.get(id=person['personnel_id']).is_commander
            if is_comd:
                pass
            else:
                current_trpr_strength += 1
        return current_trpr_strength

    def calc_absence(self):
        absentees = Absence.objects.filter(
            parade_id=self.parade_id).values()
        self.logger.info('ABSENTEES %s', absentees)
        no_absentees = False
        total_attc = 0
        total_ma = 0
        total_leave = 0
        total_off = 0
        total_other = 0
        attc = []
        ma = []
        leave = []
        off = []
        other = []
        if len(absentees) == 0:
            no_absentees = True
        else:
            
            for abs in absentees:
                if abs['is_MC']:
                    total_attc += 1
                    absentee = Personnel.objects.get(
                        id = abs['personnel_id']
                    )
                    attc.append(
                        str(absentee.rank) + " " + str(absentee.name))
                elif abs['is_MA']:
                    total_ma += 1
                    absentee = Personnel.objects.get(
                        id = abs['personnel_id']
                    )
                    ma.append(
                        str(absentee.rank) + " " + str(absentee.name))
                elif abs['is_leave']:
                    total_leave += 1
                    absentee = Personnel.objects.get(
                        id = abs['personnel_id']
                    )
                    leave.append(
                        str(absentee.rank) + " " + str(absentee.name))
                elif abs['is_off']:
                    total_off += 1
                    absentee = Personnel.objects.get(
                        id = abs['personnel_id']
                    )
                    off.append(
                        str(absentee.rank) + " " + str(absentee.name))
                elif abs['is_other']:
                    total_other += 1
                    absentee = Personnel.objects.get(
                        id = abs['personnel_id']
                    )
                    other.append(
                        str(absentee.rank) + " " + str(absentee.name))
                else:
                    pass
        data = { 
            'no_absentees': no_absentees,
            'total_absent': int(self.parade.total_strength) - int(self.parade.current_strength),
            'total_attc': {
                "count": total_attc,
                "personnel": attc
            },
            'total_ma': {
                "count": total_ma,
                "personnel": ma
            },
            'total_leave': {
                "count": total_leave,
                "personnel": leave
            },
            'total_off': {
                "count": total_off,
                "personnel": off
            },
            'total_other': {
                "count": total_other,
                "personnel": other
            },
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
                'absence_id': abs['id'],
                'personnel_id': personnel.id,
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
            card_data.append(data)
        return card_data

    def update_parade_strength(self):
        # parade = self.parade
        self.parade.commander_strength = int(self.calc_comd_strength())
        self.parade.personnel_strength = int(self.calc_trpr_strength())
        self.parade.current_strength = int(self.calc_coy_current())
        self.logger.info('COY CURRENT: %s', self.parade.current_strength)
        self.parade.total_strength = int(self.calc_coy_total())
        self.logger.info('COY TOTAL: %s', self.parade.total_strength)
        self.parade.save()


class CardHandler:
    logger = logging.getLogger(__name__)
    def __init__(self, parade_id=None, absence_id=None, id=None, remarks=None, reason=None):
        self.parade_id = parade_id
        if parade_id is not None:
            try:
                parade = Parade.objects.get(id = parade_id)
            except:
                raise Exception('Invalid parade_id')
        
        self.absence_id = absence_id
        if absence_id is not None: 
            try:
                self.absence_instance = Absence.objects.get(
                        id = absence_id
                    )
            except:
                raise Exception('Invalid absence_id')

        self.id = id
        self.remarks = remarks
        self.reason = reason

    def add_new_card(self, update=False):
        logger = logging.getLogger(__name__)
        id = self.id
        remarks = self.remarks
        reason = self.reason
        # transaction.set_autocommit(False)
        try:
            
            try:
                personnel_obj = Personnel.objects.get(
                    id = id,
                )
            except:
                raise Exception('Personnel does not exist in database')
            
            repeat_check = Absence.objects.filter(
                personnel = personnel_obj,
                parade_id = self.parade_id
            )

            if len(repeat_check) > 0:
                return False
            
            else:
                absentee = Absence(
                    personnel = personnel_obj,
                    parade_id = self.parade_id,
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
                
                parade_record = ParadePersonnelHandler(
                    parade_id=self.parade_id,
                    absence_id=absentee.id
                )
                parade_record.add_absence()
                parade_instance = ParadeStateHandler(self.parade_id)
                parade_instance.update_parade_strength()

        except Exception as identifier:
            raise Exception(identifier.args[0])

    def edit_card(self):
        absence_instance = self.absence_instance
        self.logger.info('ABSENETEE %s', absence_instance)
        remarks = self.remarks
        reason = self.reason

        try:
            
            absence_instance.remarks = remarks
            absence_instance.is_MA = False
            absence_instance.is_MC = False
            absence_instance.is_off = False
            absence_instance.is_leave = False
            absence_instance.is_other = False
            absence_instance.save()
            self.logger.info('1ST SAVE DONE')

            if reason == 'MA':
                absence_instance.is_MA = True
            elif reason == 'MC':
                absence_instance.is_MC = True
            elif reason == 'Off':
                absence_instance.is_off = True
            elif reason == 'Leave':
                absence_instance.is_leave = True
            elif reason == 'Others':
                absence_instance.is_other = True
            else:
                pass
            absence_instance.save()
            self.logger.info('2ND SAVE DONE')

        except Exception as identifier:
            raise Exception(identifier.args[0])
    
    def delete_card(self, update=False):
        logger = logging.getLogger(__name__)
        absence_instance = self.absence_instance
        parade_record = ParadePersonnelHandler(
            parade_id=self.parade_id,
            absence_id=absence_instance.id
        )
        parade_record.remove_absence()
        absence_instance.delete()
        parade_instance = ParadeStateHandler(self.parade_id)
        parade_instance.update_parade_strength()

class ParadePersonnelHandler():
    logger = logging.getLogger(__name__)
    def __init__(self, parade_id=None, absence_id=None):
        self.parade_id = parade_id
        if absence_id is not None:
            self.absence_id = absence_id
            self.personnel_id = Absence.objects.get(id=absence_id).personnel_id
            self.parade_personnel_obj = ParadePersonnel.objects.get(
                parade_id = self.parade_id,
                personnel_id = self.personnel_id
            )
    
    def populate(self):
        # populate ParadePersonnel
        all_personnel = Personnel.objects.filter(
            is_deleted = False
        ).values()
        self.logger.info('POPULATING PARADE-PERSONNEL')
        for person in all_personnel:
            parade_personnel = ParadePersonnel(
                parade_id = self.parade_id,
                personnel_id = person['id']
            )
            parade_personnel.save()
        self.logger.info('PARADE-PERSONNEL ADDED')
        return True
    
    def delete_parade_record(self):
        self.logger.info('DESTROYING PARADE-PERSONNEL')
        ParadePersonnel.objects.filter(
            parade_id = self.parade_id
        ).delete()

    def add_absence(self):
        self.logger.info('ABSENCE ADDED: personnel %s', self.personnel_id)
        self.parade_personnel_obj.is_absent = True
        self.parade_personnel_obj.save()
        return True

    def remove_absence(self):
        self.logger.info('ABSENCE REMOVED: %s', self.personnel_id)
        self.parade_personnel_obj.is_absent = False
        self.parade_personnel_obj.save()
        return True
    
    def update_absence(self):
        # BASED ON PARADE ID
        parade_personnel= ParadePersonnel.objects.filter(
            parade_id = self.parade_id
        ).values()
        for obj in parade_personnel:
            check_absence = Absence.objects.filter(
                parade_id = self.parade_id,
                personnel_id = obj['personnel_id']
            )
            if len(check_absence) == 0:
                pass
            else:
                parade_personnel_obj = ParadePersonnel.objects.get(
                    id = obj['id'])
                parade_personnel_obj.is_absent = True
                parade_personnel_obj.save()


    def check_discrepancy(self):
        #  ONLY FOR CREATED PARADE
        currentdb_personnel = Personnel.objects.filter(
            is_deleted=False).values_list('id', flat=True)
        self.logger.info('CURRENTDB PERSONNEL : %s', list(currentdb_personnel))
        parade_personnel = ParadePersonnel.objects.filter(
            parade_id = self.parade_id
        ).values_list('personnel_id', flat=True)
        self.logger.info('PARADE PERSONNEL : %s', list(parade_personnel))


        if sorted(list(currentdb_personnel)) == sorted(list(parade_personnel)):
            self.logger.info('NO DISCREPANCY')
            return False
        else:
            self.logger.info('YES DISCREPANCY')
            return True


def create_parade(date, time_of_day):
    logger = logging.getLogger(__name__)
    transaction.set_autocommit(False)
    try:
        # Check if db has personnel
        all_personnel = Personnel.objects.all().values()
        if len(all_personnel) == 0:
            raise Exception('Unable to create parade with no personnel')
        else:
            parade = Parade(
                date = date, 
                time_of_day = time_of_day
            )
            parade.save()
            parade_id = parade.id
            logger.info('PARADE SAVED ID: %s', parade_id)
            # populate ParadePersonnel
            parade_record = ParadePersonnelHandler(parade_id=parade_id)
            parade_record.populate()
            # update parade numbers
            parade_instance = ParadeStateHandler(parade_id)
            parade_instance.update_parade_strength()
            logger.info('PARADE Numbers updated')
            
    except Exception as identifier:
        transaction.rollback()
        raise Exception(identifier.args[0])
    transaction.commit()

def update_parade(parade_id):
        logger = logging.getLogger(__name__)
        transaction.set_autocommit(False)
        try:
            # Check if db has personnel
            all_personnel = Personnel.objects.all().values()
            if len(all_personnel) == 0:
                raise Exception('Unable to update parade with no personnel')
            else:
                parade = Parade.objects.get(
                    id = parade_id
                )
                logger.info('PARADE OBJ TO UPDATE: %s', parade)
                # REpopulate ParadePersonnel
                parade_record = ParadePersonnelHandler(parade_id=parade_id)
                parade_record.delete_parade_record()
                parade_record.populate()
                parade_record.update_absence()

                #  Delete removed personnel from Absence
                logger.info('CHECKING DELETED ABSENTEES')
                absentee_ids = Absence.objects.filter(
                    parade_id = parade_id
                ).values()
                parade_personnel = ParadePersonnel.objects.filter(
                    parade_id = parade_id
                ).values_list('personnel_id', flat=True)
                for i in absentee_ids:
                    if i['personnel_id'] not in parade_personnel:
                        remove_absence = Absence.objects.get(
                            id = i['id']
                        )
                        remove_absence.delete()
                        logger.info('ABSENTEE %s DELETED', 
                        Personnel.objects.get(id=i['personnel_id']).name)
                    else:
                        logger.info('NO DELETED ABSENTEES FOUND')

                # update parade numbers
                parade_instance = ParadeStateHandler(parade_id)
                parade_instance.update_parade_strength()
                logger.info('PARADE Numbers updated')
                
        except Exception as identifier:
            transaction.rollback()
            raise Exception(identifier.args[0])
        transaction.commit()



'''
MAIN FUNCTIONS

def calc_coy_total(self):
        strength = 0
        for i in Personnel.objects.filter(is_deleted=False):
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
        for i in Personnel.objects.filter(is_commander = True, is_deleted=False):
            total_comd_strength += 1
        current_comd_strength = total_comd_strength
        absent_comds = Absence.objects.filter(
            parade_id=self.parade_id).filter(personnel__is_commander=True)
        for i in absent_comds:
            current_comd_strength -= 1
        return current_comd_strength

    def calc_trpr_strength(self):
        total_trpr_strength = 0
        for i in Personnel.objects.filter(is_commander = False, is_deleted=False):
            total_trpr_strength += 1
        current_trpr_strength = total_trpr_strength
        absent_trprs = Absence.objects.filter(
            parade_id=self.parade_id).filter(personnel__is_commander=False)
        for i in absent_trprs:
            current_trpr_strength -= 1
        return current_trpr_strength

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