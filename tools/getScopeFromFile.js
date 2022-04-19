/*
根据tmLangrage获取所有标记的scope
*/
const fs = require("fs")
const path = require("path")
const vsctm = require("vscode-textmate")
const oniguruma = require("vscode-oniguruma")

const grammarList = {
    "ext.html.basic": "html.tmLanguage.json",
    "source.css": "css.tmLanguage.json",
    "source.js": "JavaScript.tmLanguage.json",
    "source.json": "JSON.tmLanguage.json",
}
const scopeName = {
    "html": "ext.html.basic",
    "css": "source.css",
    "js": "source.js",
    "json": "source.json",
}

// config
const inputFilePath = "test/show.css"
const syntaxFolder = "syntaxes"
const outputFolder = "out"
// 完整信息: info, 仅scope信息: scope, 仅最小scope信息: scopemin
const outputContentType = "scopemin"

// Utility to read a file as a promise
function readFile(path) {
    return new Promise((resolve, reject) => {
        fs.readFile(path, (error, data) =>
            error ? reject(error) : resolve(data)
        )
    })
}
const wasmBin = fs.readFileSync(
    path.join("node_modules/vscode-oniguruma/release/onig.wasm")
).buffer
const vscodeOnigurumaLib = oniguruma.loadWASM(wasmBin).then(() => {
    return {
        createOnigScanner(patterns) {
            return new oniguruma.OnigScanner(patterns)
        },
        createOnigString(s) {
            return new oniguruma.OnigString(s)
        },
    }
})
// Create a registry that can create a grammar from a scope name.
const registry = new vsctm.Registry({
    onigLib: vscodeOnigurumaLib,
    loadGrammar: (scopeName) => {
        if (typeof grammarList[scopeName] !== "undefined") {
            let grammarPath = syntaxFolder + "/" + grammarList[scopeName]
            return readFile(grammarPath).then((data) =>
                vsctm.parseRawGrammar(data.toString(), grammarPath)
            )
        } else {
            return null
        }
    },
})
// Load the JavaScript grammar and any other grammars included by it async.
const grammarScope =
    scopeName[inputFilePath.slice(inputFilePath.indexOf(".") + 1)]
registry.loadGrammar(grammarScope).then((grammar) => {
    const fileText = fs.readFileSync(path.join(inputFilePath), "utf8")
    const lines = fileText.split(/\n/)
    const fileNameSuffix = new Date().getTime().toString()
    let ruleStack = vsctm.INITIAL
    for (let i = 0; i < lines.length; i++) {
        const lineTokens = grammar.tokenizeLine(lines[i], ruleStack)
        for (let j = 0; j < lineTokens.tokens.length; j++) {
            const token = lineTokens.tokens[j]
            let s
            if (outputContentType == "info") {
                // 完整信息
                s =
                    `${token.scopes.join(",")}` +
                    `,;${lines[i].substring(
                        token.startIndex,
                        token.endIndex
                    )};\n`
            } else if (outputContentType == "scope") {
                // 仅scope信息
                s = `${token.scopes.join(",")}\n`
            } else if (outputContentType == "scopemin") {
                // 仅最小scope信息
                s = `${token.scopes[token.scopes.length - 1]},;${lines[
                    i
                ].substring(token.startIndex, token.endIndex)};\n`
            }
            // console.log(s)
            fs.writeFileSync(
                outputFolder +
                    "/" +
                    grammarScope.slice(grammarScope.lastIndexOf(".") + 1) +
                    "Scope" +
                    outputContentType +
                    fileNameSuffix +
                    ".txt",
                s,
                {
                    encoding: "utf8",
                    flag: "a",
                }
            )
        }
        ruleStack = lineTokens.ruleStack
    }
})
