# OCR postprocessing with Pyspellcheck and Latin frequency data.
from nltk import word_tokenize
import string
from progress.bar import Bar
import re

file_name = "pro_patria_transcription"
from spellchecker import SpellChecker
spell_lat = SpellChecker(local_dictionary="latin_freq.json")
with open(f"orig/{file_name}.txt", "r", encoding="utf-8") as text_file:
    text = text_file.read()
spell_checked = []
tokens = word_tokenize(text)
with Bar("Processing...", max=len(tokens)) as bar:
    for token in tokens:
        if token in string.punctuation:
            spell_checked.append(token)
        else:
            token_corrected = spell_lat.correction(token)
            spell_checked.append(token_corrected)
        bar.next()
spell_checked = " ".join(spell_checked)
spell_checked = re.sub(" (\.|,|;|:|'|\"|!|\?)", "\g<1>", spell_checked)
spell_checked = re.sub(" (\.|,|;|:|!|\?)", "\g<1>", spell_checked)
spell_checked = re.sub("(\d+)", "\g<1>\n", spell_checked)

with open(f"texts/{file_name}_spellchecked.txt", "w", encoding="utf-8") as output_file:
    output_file.write(spell_checked)
print("Finished!\a")