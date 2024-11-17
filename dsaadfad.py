import re


key_ = "   ios java script"

if re.match(r'.*[ios|swift].*', key_, re.IGNORECASE):
    print("ios")

else:
    print("no match")