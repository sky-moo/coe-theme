"""获取tmLanguage文件中带有'$'的scope, 并将其与所有可能的值拼接为完整的scope.
"""
import re
import json


def searchScope(data):
    """递归搜索scope.
    """

    def doSearch(d):
        """在字典中搜索.
        """
        for k in d.keys():
            if "name" in k and "$" in d[k]:
                global out
                out.append(json.dumps(d))
            elif type(d[k]) == dict or type(d[k]) == list:
                searchScope(d[k])

    if type(data) == list:
        for d in data:
            doSearch(d)
    elif type(data) == dict:
        doSearch(data)
    else:
        print("wrong")
        exit()


def calMatch(obj):
    """拼接匹配.
    """
    value = '"name' + str(i) + '": ' + obj.group(2) + ',' + obj.group(1)
    # print(obj.group(0))
    # print(value)
    return value


# config
language = "html"
inputFile = f"syntaxes/{language}.tmLanguage.json"
outputFile = f"{language}Output.json"
# 是否提升capture中的name
up = True

with open(inputFile, "r", encoding="utf-8") as f:
    fileText = f.read()
# 提升的captures中的name至外面一层
if up:
    i = 0
    #  name是第一项
    regObj1 = re.compile(r'("(?:begin|end)?[cC]aptures": \{[ \n]*?)' + r'(?:"[0-9]+": \{[ \n]*?' +
                         r'"name": ("[a-zA-Z\d.\{\}/:-]+\$[a-zA-Z\d.\{\}/:-]+")[ \n]*?\},?[ \n]*?)')
    # name不是第一项
    regObj2 = re.compile(r'("(?:begin|end)?[cC]aptures": \{[ \n]*?' + r'"[0-9]+": \{[ \n]*?' +
                         r'(?:"name": "[a-zA-Z\d.\{\}/:-]+"|"patterns": \[(?:[^\]]|\n)*?\])' +
                         r'[ \n]*?\}' + r'(?:,[ \n]*?"[0-9]+": \{[ \n]*?' +
                         r'(?:"name": "[a-zA-Z\d.\{\}/:-]+"|"patterns": \[(?:[^\]]|\n)*?\])' +
                         r'[ \n]*?\})*?)' + r'(?:,[ \n]*?"[0-9]+": \{[ \n]*?' +
                         r'"name": ("[a-zA-Z\d.\{\}/:-]+\$[a-zA-Z\d.\{\}/:-]+")[ \n]*?\},?[ \n]*?)')
    while regObj1.search(fileText):
        fileText = regObj1.sub(calMatch, fileText)
        i += 1
    while regObj2.search(fileText):
        fileText = regObj2.sub(calMatch, fileText)
        i += 1
fileJson = json.loads(fileText)
out = []
for v in fileJson["repository"].values():
    if "$" in json.dumps(v):
        searchScope(v)
with open(f"out/{outputFile}", "w", encoding="utf-8") as f:
    # json
    # f.write('{"arr":[')
    # f.write(",".join(set(out)))
    # f.write(']}')
    # print(f"File out/{outputFileName}.json add")
    # txt
    f.write("\n".join(set(out)))
