from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from utils.matchesBasic import  roles_match, interests_match, programming_skills_match
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json
from utils.k_best_tests import maikelfunction
from utils.utils import print_group, print_group_matches
import random

data = json.load(open("data/datathon_participants.json", "r"))

# INIT
all_groups = []
for person in data[0:6]:
    all_groups.append(init_participant(ParticipantAbstract(Participant(**person))))

# ITERATE
finished = False
groups_complete = []

while not finished:
    input("The groups are now created")
    for group in all_groups:
        print_group(group)
        print("\n")
    pairs, values, positive, negative = maikelfunction(all_groups, 2)
    input("Now the pairs are created")
    all_groups_new = []
    for group1, group2 in pairs:
        merged_group = group1.merge_group(group2)
        all_groups_new.append(merged_group)
        print_group_matches(group1,group2,merged_group)
        print("\n")

    all_groups = all_groups_new
    input("Now the merges are tried and the groups decide if they stay together")
    for group in all_groups:
        if random.random() > 0.7:
            satisfaction = True
        else:
            satisfaction = False
        print(f'{group.name} is satisfied: {satisfaction}')
        print("--------------------\n")
#print(pairs, values, positive, negative)