from Group import Group
from typing import List


class Table(dict):
    def __init__(self, keys, preference_type: callable):
        self.table = {}
        self.group_prefs = {}
        self.keys_ = keys
        self.preference_type = preference_type
        for key in keys:
            self.table[key] = []


    def initialize(self, allgroups: List[Group]):
        for key in self.keys_:
            for group in allgroups:
                self.group_prefs[group] = []
                if key in self.preference_type(group):
                    self.table[key].append(group)
                    self.group_prefs[group].append(key)
        return self.table


    def update(self, group1: Group, group2: Group):
        """
        group1: Group: the dominant group that will stay in the table 
        group2: Group: the group that will be erased from the table and merged into group1
        new_keys: List[keys]: List of new keys for the new merged group 
        """
        for key in self.group_prefs[group2]:
            self.table[key].remove(group2)
        del self.group_prefs[group2]
        for key in self.group_prefs[group1]:
            if not key in self.preference_type(group1):
                self.table[key].remove(group1)
