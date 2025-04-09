"""The main class that enables annotation of the full-text while processing a stemmed version of it.
"""

import regex as re
from typing import Dict, List, Union

from tqdm import tqdm

from stemmers import stemmers, sent_stemmers
from persistence import tokenize_values

from util import tokenizer, sent_tokenizer

# language = "english"

from template import span_templ

cleanup_map = {
    # "-\n": "",
    # "ſ": "s",
}


class Annotator:
    def __init__(self, tokenizer_name, fulltext: str, values_br: Dict[str, str] = {}):
        self.token_func = stemmers[tokenizer_name]
        self.sent_token_funct = sent_stemmers[tokenizer_name]
        self.func_name = tokenizer_name
        # label->value dict
        self.values = values_br if values_br else tokenize_values(tokenizer_name)[1]
        self.fulltext = fulltext
        for k, v in cleanup_map.items():
            self.fulltext = self.fulltext.replace(k, v)

    def rich_text(self):
        """
        TODO: reuse tokenisation from util.py
        """
        values_count = {v: 0 for v in set(self.values.values())}
        result = []
        sentences = sent_tokenizer(self.fulltext)

        sent_spans = []
        sent_start = 0
        for sent in sentences:
            # sent_spans += [(sent_start, sent_start + len(sent))]
            # sent_start = sent_start + len(sent) + 1
            match = self.fulltext[sent_start:].find(sent)
            sent_spans += [(sent_start + match, sent_start + match + len(sent))]
            sent_start += match + len(sent)
        annotated_text = self.fulltext

        for i, sentence in reversed(list(enumerate(sentences))):
            print(sentence)
            tokenized = sent_stemmers[self.func_name](self.fulltext)
            annotated_sentence = sentence

            ranges = []
            word_start = 0
            for word, lemma in tokenized:
                word_start = sentence.find(word, word_start)
                ranges += [(word_start, word_start + len(word))]
                word_start += len(word)

            for j, (word, lemma) in reversed(list(enumerate(tokenized))):
                # for j, t in reversed(list(enumerate(doc))):   
                if lemma in self.values.keys():
                    value = self.values[lemma]
                    sid = f"{value}-{values_count[value]}"
                    stype = f"{lemma} {value}"
                    title = value
                    # title = annotated_sentence[ranges[j][0] : ranges[j][1]]
                    annotated_sentence = (
                        annotated_sentence[: ranges[j][0]]
                        + span_templ.format(
                            id=sid,
                            type=stype,
                            title=title,
                            content=word,
                        )
                        + annotated_sentence[ranges[j][1] :]
                    )
            # print(annotated_sentence)
            annotated_text = (
                annotated_text[: sent_spans[i][0]]
                + annotated_sentence
                + annotated_text[sent_spans[i][1] :]
            )
        # if annotated_text:
        result = annotated_text

        result = result.replace("\n\n\n", "\n\n")
        result = result.replace("\n\n", "</p><p>")
        result = result.replace("\n", "<br/>")
        result = f"<p>{result}</p>"
        # return "<p>" + "</p><p>".join(result) + "</p>"
        return result

    def tokens(self, fulltext) -> List[List[str]]:
        """get the text of the story and returns a list of lemmas"""
        return [[t[1] for t in self.sent_token_funct(fulltext)]]


if __name__=="__main__":
    sin_psal = " Въѹші бж҃е молітвѫ моѭ:. Ї не прѣзърі моленъѣ моего:  Вонъмі ї ѹслꙑші мѩ:--"

    # Въскръбѣхъ печальѭ моеѭ ї съмѩ сѩ:  Ѡтъ гласа вражьѣ отъ сътѫжаньѣ грѣшьніча:-- """
    #Ѣко ѹклонішѩ на мѩ безаконнъе: Ї вь гнѣвѣ вражьдовахѫ мнѣ:--  Ср҃дце мое съмѩте сѩ во мнѣ: И страхъ съмрътьнꙑі нападе на мѩ:--  Боѣзнъ і трепетъ пріде на мѩ:. и покрꙑ мѩ тъма:--  И рѣхъ къто дастъ мнѣ крілѣ ѣко голѫби:  Се ѹдалихъ сѩ бѣгаѩ: ї въдворихъ сѩ въ пѹстꙑні:  Чаахъ б҃а сп҃аѭщаго мѩ:. Ѡтъ прѣнемаганьѣ дх҃а и бѹрѩ:-  Потопи г҃і і раздѣлі ѩзꙑ ихъ:. Ѣко видѣхъ безаконенье і прѣрѣканъе въ градѣ:--  Денъ і нощъ обідетъ тѩ по стѣнамъ его: Безаконнъе і трѹдъ посрѣдѣ его неправъда:-  И не оскѫдѣ отъ пѫті его ліхва и льстъ:  Ѣко аще мі би врагъ поносілъ прѣтръпѣлъ ѹбо бимъ:- И аще бі ненавідѩі мне на мѩ велърѣчевалъ: Оукрꙑлъ сѩ бимъ ѹбо отъ него:--  Тꙑ же чв҃че равьнодш҃ьне: Вл҃ко моі знанъе мое --  Їже кѹпьно насаділъ мнѣ брашьна: Въ храмѣ бж҃ы ходіховѣ іномъшленьемъ:-  Да прідетъ съмръть на нѩ сънідѫтъ въ адъ живи:- Ѣко зълоба въ жиліщіхъ іхъ посрѣдѣ їхъ:--  Азъ къ б҃ѹ возьвахъ і г҃ъ ѹслъша мѩ:  Вечеръ ї ютро и полѹдъне повѣмъ: Възвѣщѫ ѣко ѹслꙑша гласъ моі:-  Нѣстъ бо імъ измѣненьѣ: Ѣко и не ѹбоѣшѩ сѩ б҃а:---  Прострѣтъ рѫкѫ своѭ на въздание:. Оскврънішѩ на земи завѣтъ его:--  Раздѣлішѩ сѩ отъ гнѣва ліца его: Ї прібліжішѩ сѩ ср҃дца іхъ:.-- Оумѩкнѫшѩ словеса іхъ паче олѣа: И та сѫтъ стрѣлꙑ:.  тꙑ же бж҃е нізъведеши ѩ въ стѹденецъ истълѣньѣ:--- "
    stemmer = "dummy"
    values_br = {'бог': 'бог', 'слово': 'слово', 'истина': 'истина', 'вера': 'вера', 'моего': 'моего'}
    a = Annotator(stemmer, sin_psal, values_br)
    print(a.rich_text())