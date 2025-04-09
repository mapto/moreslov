"""General functions without internal dependencies"""

from typing import Dict, List, Optional

import os
import string
import itertools
from glob import glob
import filecmp
import shutil
from datetime import datetime
import regex as re

regex_token_sep = r"[\s\.\-\:]+"


from settings import DATEFORMAT_LOG, VOCAB, CORPORA


# def clean_word(s: str) -> str:
#     return re.sub("")
def name2fname(name: str) -> str:
    return (
        name.replace(" ", "_")
        .replace("’", "_")
        .replace("'", "_")
        .replace(",", "_")
        .replace(".", "_")
        .replace("__", "_")
    )


def fname2name(fname: str) -> str:
    """_summary_

    Args:
        fname (str): _description_

    Returns:
        str: _description_
    >>> fname2name("four/Lansdowne_72-43_Transcription.html")
    'Lansdowne 72-43 Transcription'
    >>> fname2name("two/A29858_sec.html")
    'A29858 Sec'
    >>> fname2name("site/sb/variation/singles.html#Sammy")
    'Sammy'
    """
    # print(fname)
    name = (
        fname.split("/")[-1]
        .split("#")[-1]
        .replace("_s_", "'s ")
        .replace("_.", ".")
        .replace(".html", "")
        .replace(".txt", "")
    )
    assert name, f"Path {fname} is empty"
    if name.endswith("_"):
        name = name[:-1]
    name = " ".join(w[0].upper() + w[1:].lower() for w in name.split("_"))
    # print(name)
    return name


def fname2path(fname: str) -> str:
    """
    >>> fname2path("corpora/singles/Sammy.txt")
    'singles.html#sammy'
    """
    parts = fname.split("/")[-2:]
    parts[-1] = parts[-1].split(".")[0].lower()
    if parts[-1][-1] == "_":
        parts[-1] = parts[-1][:-1]
    name = ".html#".join(parts)

    return name


def path2corpus(path: str) -> str:
    """
    >>> path2corpus('site/sb2/clustering/bruce_marshall.html#la_ragazza_di_maggio')
    'bruce_marshall'
    """
    return path.split(".")[-2].split("/")[-1]


def path2name(path: str) -> str:
    """
    >>> path2name('site/sb2/clustering/bruce_marshall.html#la_ragazza_di_maggio')
    'La Ragazza Di Maggio'
    """
    return " ".join(w.capitalize() for w in path.split("#")[-1].split("_"))


def tokenizer(text: str) -> list[str]:
    return re.split(regex_token_sep, text)


def sent_tokenizer(text: str) -> list[str]:
    """In OCS sentences were not used much"""
    return text.split("\n\n")


def story_tokenize(story: str) -> list[list[str]]:
    """get the text of the story and returns a lists of sentences represented as list of lemmas."""
    tokens = []
    words = []

    sentences = [story]
    for i, sentence in enumerate(sentences):
        # doc = word_tokenize(sentence)
        doc = tokenizer(sentence)
        words += [[t for t in doc if t not in string.punctuation + "\n"]]
    return words


def word2tokens(token_func, story: list[list[str]]) -> list[list[str]]:
    return [[token_func(w.lower(), s) for w in s] for s in story]


def collect_tokens(
    tokenized: Dict[str, Dict[str, List[List[str]]]],
    corpus: Optional[str] = None,
) -> List[List[str]]:
    """
    >>> data = {'A': {'1': [['aa', 'bb'], ['cc']], '2':[['c', 'd']]}, 'B': {'I': [['a', 'b']], 'II': [['bd', 'ce', 'cf'], ['ff']]}}
    >>> collect_tokens(data, 'A')
    [['aa', 'bb'], ['cc'], ['c', 'd']]

    >>> collect_tokens(data, 'B')
    [['a', 'b'], ['bd', 'ce', 'cf'], ['ff']]

    >>> collect_tokens(data)
    [['aa', 'bb'], ['cc'], ['c', 'd'], ['a', 'b'], ['bd', 'ce', 'cf'], ['ff']]


    """
    result = []
    if corpus:
        # result = list(tokenized[corpus].values())
        result = list(itertools.chain(*list(tokenized[corpus].values())))
    else:
        for c in tokenized.keys():
            result += collect_tokens(tokenized, c)
    return result


def rmdirs():
    from stemmers import stemmers

    for s in stemmers.keys():
        stem_dir = f"vocab/{s}"
        if os.path.exists(stem_dir):
            shutil.rmtree(stem_dir)


def mkdirs():
    from stemmers import stemmers

    # from vocabulary import vocabulary
    # from corpora import corpora

    if not os.path.exists("vocab"):
        os.mkdir("vocab")
    for s in stemmers.keys():
        nxt = f"vocab/{s}"
        if not os.path.exists(nxt):
            os.mkdir(nxt)
        # nxt3 = f"{nxt}/values"
        # if not os.path.exists(nxt3):
        #     os.mkdir(nxt3)

        # for v in vocabulary:
        #     nxt4 = f"{nxt}/{v}"
        #     if not os.path.exists(nxt4):
        #         os.mkdir(nxt4)

        #     for c in corpora:
        #         nxt2 = f"{nxt4}/{c}"
        #         if not os.path.exists(nxt2):
        #             os.mkdir(nxt2)
        #         nxt3 = f"{nxt2}/values"
        #         if not os.path.exists(nxt3):
        #             os.mkdir(nxt3)


def get_dirs(path: str = "") -> List[str]:
    if not path:
        path = f"corpora.{CORPORA}/"
    print(f"Loading from path {path}...")
    result = [
        f.replace(path, "") for f in glob(f"{path}/*") if os.path.isdir(os.path.join(f))
    ]
    # TODO: remove
    assert len(set(c[0] for c in result)) == len(
        result
    ), "Each collection should start with a different letter"
    return result


def stats(fulltexts, tokenized: Dict[str, Dict[str, List[str]]]):
    symbols = {}
    texts = {}
    tokens = {}
    for c in get_dirs():
        texts[c] = len(fulltexts[c])
        symbols[c] = 0
        for tale in fulltexts[c].values():
            symbols[c] += len(tale)
        tokens[c] = 0
        for tale in tokenized[c].values():
            tokens[c] += sum(len(s) for s in tale)

    # print(f"texts: {texts}")
    # print(f"symbols: {symbols}")
    # print(f"tokens: {tokens}")
    return texts, symbols, tokens


def save_vocab(contents: str, vocab: str) -> None:
    ts = datetime.now().strftime(DATEFORMAT_LOG)
    fname = f"vocab/{vocab}.csv"
    backup = fname.replace(".", f".{ts}.")
    shutil.copy(fname, fname.replace(".", f".{ts}."))
    with open(fname, "w") as f:
        f.write(contents)
    if filecmp.cmp(fname, backup, False):
        os.remove(backup)
    else:
        os.remove(f"vocab/{vocab}.flat.csv")
        rmdirs()
        mkdirs()
