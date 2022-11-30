### INITS ###

f001 = open("./recordings/getRecordings001.xml", "r") # XML to read from
f002 = open("./recordings/getRecordings002.xml", "r") # XML to read from
f003 = open("./recordings/getRecordings003.xml", "r") # XML to read from
fScalelite = open("./recordings/scalelite.xml", "r") # XML to read from
fout = open("out.csv", "w")             # File to write to

bbb001: str = f001.read()
bbb002: str = f002.read()
bbb003: str = f003.read()
fileScalelite: str = fScalelite.read()
# We add these to a list to avoid atleast SOME boilerplating
files = {
    "bbb001": bbb001, 
    "bbb002": bbb002, 
    "bbb003": bbb003
}

# Date from which to start from
checkFrom:int = 1668384000000 # 1668384000000 = 14.11.2022 in Unix-Milliseconds

### FUNCTIONS ###

def find_all(a_str, sub): # to find all and put into a list
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def getInTags(input, tag_a:str, tag_b:str): # to find string between two tags
    output = list()

    firstIndex = list(find_all(input, tag_a))
    secondIndex = list(find_all(input, tag_b))

    for i in range(len(firstIndex)):
        mini: str = input[firstIndex[i]+len(tag_a): secondIndex[i]]
        output.append(mini)

    return output

### PROGRAM ###

# All recordings from the bbbs go in here
recordingList = dict()

for servername, content in files.items():
    # getting all the Entries
    outputRecordID = getInTags(content, '<recordID>', '</recordID>')                    # RecordID
    outputMeetingID = getInTags(content, '<meetingID>', '</meetingID>')                 # MeetingID
    outputInternalMeetingID = getInTags(content, '<internalMeetingID>', '</internalMeetingID>') # InternalMeetingID
    outputTitles = getInTags(content, '<bbb-context-label>', '</bbb-context-label>')    # Title
    outputStart = getInTags(content, '<startTime>', '</startTime>')                     # Start Timestamp
    outputEnd = getInTags(content, '<endTime>', '</endTime>')                           # End Timestamp
    outputLink = getInTags(content, '<url>', '</url>')                                  # Url
    outputServer = servername                                                           # Server

    print("Checking:",outputServer)

    for i in range(len(outputTitles)):
        if(int(outputStart[i]) > checkFrom): # check if the entries fit into the timeframe
            recordingList[outputRecordID[i]] = f"{outputRecordID[i]}\t{outputMeetingID[i]}\t{outputInternalMeetingID[i]}\t{outputTitles[i]}\t{outputStart[i]}\t{outputEnd[i]}\t{outputLink[i]}\t{servername}"
        
# we also do this with the scalelite entries, just once this time
scaleliteList = dict()
outputRecordID = getInTags(fileScalelite, '<recordID>', '</recordID>')                    # RecordID
outputMeetingID = getInTags(fileScalelite, '<meetingID>', '</meetingID>')                 # MeetingID
outputInternalMeetingID = getInTags(fileScalelite, '<internalMeetingID>', '</internalMeetingID>') # InternalMeetingID
outputTitles = getInTags(fileScalelite, '<bbb-context-label>', '</bbb-context-label>')    # Title
outputStart = getInTags(fileScalelite, '<startTime>', '</startTime>')                     # Start Timestamp
outputEnd = getInTags(fileScalelite, '<endTime>', '</endTime>')                           # End Timestamp
outputLink = getInTags(fileScalelite, '<url>', '</url>')                                  # Url
outputServer = "scaleLite"                                                           # Server

print("Checking:",outputServer)

for i in range(len(outputTitles)):
    if(int(outputStart[i]) > checkFrom): # check if the entries fit into the timeframe
        scaleliteList[outputRecordID[i]] = f"\"{outputRecordID[i]}\"\t\"{outputMeetingID[i]}\"\t\"{outputInternalMeetingID[i]}\"\t\"{outputTitles[i]}\"\t\"{outputStart[i]}\"\t\"{outputEnd[i]}\"\t\"{outputLink[i]}\"\t\"{servername}\""



print(len(recordingList.items()),"recordings on bbbs found")
print(len(scaleliteList.items()),"recordings on scalelite found")

# Formatting into lists to ease the difference
setBBBs = set(recordingList.keys())
setScalelite = set(scaleliteList.keys())
difference = setBBBs - setScalelite
print("Found",len(difference),"different entries")

# Adding a CSV Header
temp:str = '\"ID\"\t\"Meeting ID\"\t\"Internal Meeting ID\"\t\"Title\"\t\"Start\"\t\"End\"\t\"Link\"\t\"Server\"\t\n'                              # Header for CSV
fout.write(temp) # Write the headers first
for entry in difference: # Writing each entry in a new line
    mini:str = f"{recordingList[entry]}\n"
    fout.write(mini)

# close the streams to avoid leaks
f001.close()
f002.close()
f003.close()
fScalelite.close()
fout.close()
