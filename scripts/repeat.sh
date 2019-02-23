# Usage - sh repeat.sh "message for commit"
python preprocess.py
python manualCorrection.py
cp ../derivedFiles/cataloguev006.tsv ../ShivadattaShuklaPrakashanandanatha.tsv
git add ../derivedFiles/
git add ../ShivadattaShuklaPrakashanandanatha.tsv
git commit -m "$1"
git push origin master
