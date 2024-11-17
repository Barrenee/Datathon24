import re
from typing import Dict

def preprocess_prog_skills(dict_: Dict[str, int]) -> Dict[str, int]:
    '''Preprocesses the programming skills of a participant'''
    processed_dict = {}
    for key, value in dict_.items():
        if re.match(r'.*[ios|swift].*', key, re.IGNORECASE):
            processed_dict['ios'] = value
        elif re.match(r'.*[android|kotlin].*', key, re.IGNORECASE):
            processed_dict['android'] = value
        elif re.match(r'.*java.*script.*', key, re.IGNORECASE):
            processed_dict['javascript'] = value
        elif re.match(r'.*java.*', key, re.IGNORECASE):
            processed_dict['java'] = value
        elif key == 'data analyss':
            processed_dict['data analysis'] = value 
        else:
            processed_dict[key.lower()] = value
    return processed_dict

def print_group(group):
    # Print just the basics so to understand de merge
    print("----------------")
    print(group.name)
    print(group.roles_fullfilled)
    print(group.objective_abs)
    print(group.interest_in_challenges)

    