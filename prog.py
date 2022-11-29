import requests

f = open("./getRecordings.xml", "r")    # XML to read from
fout = open("out.csv", "w")             # File to write to

fileXML: str = f.read()

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

outputTitles = getInTags(fileXML, '<bbb-context-label>', '</bbb-context-label>')    # Title
outputStart = getInTags(fileXML, '<startTime>', '</startTime>')                     # Start Timestamp
outputEnd = getInTags(fileXML, '<endTime>', '</endTime>')                           # End Timestamp
outputLink = getInTags(fileXML, '<url>', '</url>')                                  # Url

temp:str = '\"Name\"\t\"Link\"\t\"Start\"\t\"Ende\"\n'                              # Header for CSV

fout.write(temp) # Write the headers first

for i in range(len(outputTitles)):
    mini: str = outputTitles[i] + '\t' + outputLink[i] + '\t' + outputStart[i] + '\t' + outputEnd[i] + '\n' # format each column accordingly (we use Tabs for this)
    fout.write(mini) # write each line

f.close()
fout.close()
