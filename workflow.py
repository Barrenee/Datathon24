from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from utils.matchesBasic import  roles_match, interests_match, programming_skills_match
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json



data = json.load(open("data/datathon_participants.json", "r"))


all_groups = []
for person in data:
    all_groups.append(init_participant(Participant(**person)))

challenges_table, objectives_table, languages_table = init_tables(all_groups)

for group in all_groups:
    compatible_groups = get_compatible_groups(group, challenges_table, objectives_table, languages_table)


    matched_roles = roles_match(group=group, compatible_groups=compatible_groups)
    matched_interests = interests_match(group=group, compatible_groups=compatible_groups)
    matched_skills = programming_skills_match(group=group, compatible_groups=compatible_groups)

