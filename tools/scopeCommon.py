import re

__all__ = [
    "suffix2tmFilename", "suffix2LowercaseName", "getValueListBase", "getValueListOther",
    "getScopeBase", "getScopeOther"
]


def suffix2tmFilename(suffix):  # type: (str) -> str
    return tmLanguageFilename[suffix]


def suffix2LowercaseName(suffix):  # type: (str) -> str
    return languageLowercaseName[suffix]


def getValueListBase(languageList,
                     scopeFolder="out",
                     scopeFilenameTag="AllScope"):  # type: (list, str, str) -> list
    """获取多个语言的Scope数据.

    :param languageList: 语言源文件后缀列表
    :param scopeFolder: Scope文件目录
    :param scopeFilenameTag: Scope文件名标签

    :return: [[(lang1,scope1),...],[(lang2,scope1),...],...]
    """
    valueList = []
    for suffix in languageList:
        with open(f"{scopeFolder}/{suffix2tmFilename(suffix)}-{scopeFilenameTag}.txt",
                  "r",
                  encoding="utf-8") as f:
            scopeList = f.read().split("\n")
        valueList.append([(suffix, scopeList[i]) for i in range(len(scopeList))])
    return valueList


def getValueListOther(syntaxFilename,
                      langrageSuffix,
                      scopeFolder="out",
                      scopeFilenameTag="AllScope"):  # type: (str, str, str, str) -> list
    """获取单个语言文件的Scope数据.

    :param syntaxFilename: .tmLanguage.json文件名称
    :param langrageSuffix: 从属语言的语言源文件后缀
    :param scopeFolder: Scope文件目录
    :param scopeFilenameTag: Scope文件名标签

    :return: [(lang,scope1),(lang,scope2),...]
    """
    with open(f"{scopeFolder}/{syntaxFilename}-{scopeFilenameTag}.txt", "r", encoding="utf-8") as f:
        scopeList = f.read().split("\n")
    return [(langrageSuffix, scopeList[i]) for i in range(len(scopeList))]


def getScopeBase(languageSuffix,
                 syntaxFolder="syntaxes",
                 outputFolder="out",
                 outputFilenameTag="AllScope"):  # type: (list, str, str, str) -> None
    """获取基本tmLanguage文件的范围(Scope).

    :param languageSuffix: 语言源文件后缀列表
    :param syntaxFolder: .tmLanguage.json文件目录
    :param outputFolder: 输出目录
    :param outputFilenameTag: 输出文件名标签
    """
    for language in languageSuffix:
        language = suffix2tmFilename(language)
        inputFilePath = f"{syntaxFolder}/{language}.tmLanguage.json"
        outputFilePath = f"{outputFolder}/{language}-{outputFilenameTag}.txt"
        with open(inputFilePath, "r", encoding="utf-8") as f:
            fileText = f.read()
        out = []
        for key in ["name", "contentName"]:
            out += re.findall(rf'"{key}": "(.*?\..*?)"', fileText)
        out = [out[i].split(" ")[-1] for i in range(len(out))]
        out = list(set(out))
        out.sort()
        with open(outputFilePath, "w", encoding="utf-8") as f:
            f.write("\n".join(out))


def getScopeOther(syntaxFilename,
                  syntaxFolder="syntaxes",
                  outputFolder="out",
                  outputFilenameTag="AllScope"):  # type: (str, str, str, str) -> None
    """获取其它tmLanguage文件的范围(Scope).

    :param syntaxFilename: .tmLanguage.json文件名称
    :param syntaxFolder: .tmLanguage.json文件目录
    :param outputFolder: 输出目录
    :param outputFilenameTag: 输出文件名标签
    """
    language = syntaxFilename
    inputFilePath = f"{syntaxFolder}/{language}.tmLanguage.json"
    outputFilePath = f"{outputFolder}/{language}-{outputFilenameTag}.txt"
    with open(inputFilePath, "r", encoding="utf-8") as f:
        fileText = f.read()
    out = []
    for key in ["name", "contentName"]:
        out += re.findall(rf'"{key}": "(.*?\..*?)"', fileText)
    out = [out[i].split(" ")[-1] for i in range(len(out))]
    out = list(set(out))
    out.sort()
    with open(outputFilePath, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


tmLanguageFilename = {
    "html": "html",
    "css": "css",
    "js": "JavaScript",
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "py": "MagicPython",
    "xml": "xml",
    "md": "markdown",
    "json": "JSON"
}
languageLowercaseName = {
    "html": "html",
    "css": "css",
    "js": "javascript",
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "py": "python",
    "xml": "xml",
    "md": "markdown",
    "json": "json"
}

if __name__ == "__main__":
    languageList = ["html", "css", "js", "c", "cpp", "java", "py", "xml", "md", "json"]
    getScopeBase(languageList)
