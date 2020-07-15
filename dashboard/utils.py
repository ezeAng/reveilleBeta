from attendance.models import (
    Personnel, 
    Absence, 
    Status, 
    Parade
)
import logging
import sys
from attendance.utils import ParadeStateHandler

def get_all_personnel():
    logger = logging.getLogger(__name__)
    platoon_list = Personnel.objects.filter(
        is_deleted = False
    ).order_by('platoon').values_list('platoon', flat=True).distinct()
    logger.info('PLT LIST %s', platoon_list)
    data = {}
    company = []
    for platoon in platoon_list:
        plt_object = {
            'plt_number': int(platoon)
        }
        person_list = []
        personnel = Personnel.objects.filter(
            platoon = int(platoon)
        ).order_by('-created_at').values()
        for person in personnel:
            person_data = {
                'id': person['id'],
                'rank': person['rank'],
                'name': person['name']
            }
            person_list.append(person_data)
        plt_object['personnel'] = person_list
        company.append(plt_object)
    data['company'] = company
    logger.info(data)
    return data

def add_personnel(name, rank, platoon):
    man = ['REC', 'PTE', 'LCP', 'CPL', 'CFC']
    if rank in man:
        is_commander = False
    else:
        is_commander = True
    new_person = Personnel(
        name = name,
        rank = rank,
        platoon = int(platoon),
        is_commander = is_commander,
        company = 'Test'
    )
    new_person.save()

def edit_personnel(id, name, rank, platoon):
    try:
        personnel = Personnel.objects.get(id=id)
    except:
        raise Exception('Personnel does not exist in database.')
    personnel.name = name
    personnel.rank = rank
    personnel.platoon = platoon
    personnel.save()

def delete_personnel(id):
    try:
        personnel = Personnel.objects.get(id=id)
    except:
        raise Exception('Personnel does not exist in database.')
    personnel.is_deleted = True
    personnel.save()
    