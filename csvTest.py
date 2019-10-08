import csv

with open('musicInfo.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    musicInfo = []
    for row in csv_reader:
        musicInfo.append(row)
musicInfo = musicInfo[2:]

musicDict = {}
def decode(s):
    if s == "None":
        return None
    if "; " in s:
        s1, s2 = s.split("; ")
        return (decode(s1), decode(s2))
    else:
        lst = s.split(",")
        return [int(lst[0])*10, int(lst[1])*10]

name = "Hold It Down"
def findMusic(name):
    for row in musicInfo:
        musicDict["name"] = row[1]
        musicDict["artist"] = row[2]
        musicDict["intro"] = decode(row[3])
        musicDict["verse"] = decode(row[4])
        musicDict["buildup"] = decode(row[5])
        musicDict["drop"] = decode(row[6])
        musicDict["break"] = decode(row[7])
        musicDict["outro"] = decode(row[8])
        musicDict["duration"] = musicDict["outro"][1]
        if musicDict["name"] == name:
            return musicDict

# print(findMusic(name))
s = u"Bonzo’s Juggling Show"
n = "music/" + s + ".ogg"
m = "music/Bonzo’s Juggling Show.ogg"
print(n == m)
# for i in range(len(n)):
#     if n[i] != m[i]:
#         print(n[i])

