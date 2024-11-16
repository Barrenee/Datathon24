import json
import participant


directory = "./data/datathon_participants.json"

participants = participant.load_participants(directory)
print(len(participants))

print(participants[1])
