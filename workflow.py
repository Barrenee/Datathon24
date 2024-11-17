from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from utils.matchesBasic import  roles_match, interests_match, programming_skills_match
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json
from utils.k_best_tests import maikelfunction
from utils.utils import print_group


data = json.load(open("data/datathon_participants.json", "r"))


all_groups = []
for person in data[0:6]:
    all_groups.append(init_participant(ParticipantAbstract(Participant(**person))))
    
merged_group = all_groups[0].merge_group(all_groups[1])

for group in all_groups:
    print_group(group)
    print("\n")
pairs, values, positive, negative = maikelfunction(all_groups, 2)

for group1, group2 in pairs:
    print_group(group1)
    print_group(group2)
    
    merged_group = group1.merge_group(group2)
    print_group(merged_group)
    print("\n")
#print(pairs, values, positive, negative)