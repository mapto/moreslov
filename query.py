from customtypes import TokenToClassMap, ClassToTokenMap

from sqlalchemy import func, distinct
from sqlalchemy.sql import expression, functions

from db import Session

from corpora import corpora as global_corpora
from stemmers import stemmers

from model import Token, Text, Sentence, Word


def tokenize_values(
    s: Session, stemmer: str
) -> tuple[ClassToTokenMap, TokenToClassMap]:
    """Get the two directional dictionaries between values and labels.
    As a byproduct make a stemmed version of the values list in the corresponding folder.

    Args:
    :param Session s: SQL session
    :param str stemmer: stemmer name as in stemmers.py

    Returns:
        Tuple[Dict[str, List[str]], Dict[str, str]]: returns two dictionaries:
            value->list_labels and label->value
    """
    data = (
        s.query(Token.token, func.lower(Token.token_class))
        .filter(Token.stemmer == stemmer)
        .all()
    )
    values: ClassToTokenMap = {}
    valuesbackref = dict(data)
    for k, v in valuesbackref.items():
        values[v] = values.get(v, []) + [k]
    return values, valuesbackref


def flat_tokenize_values(
    s: Session, stemmer: str
) -> tuple[ClassToTokenMap, TokenToClassMap]:
    """Get the two directional dictionaries between values and labels.
    As a byproduct make a stemmed version of the values list in the corresponding folder.

    Args:
    :param Session s: SQL session
    :param str stemmer: stemmer name as in stemmers.py

    Returns:
        Tuple[Dict[str, List[str]], Dict[str, str]]: returns two dictionaries:
            value->list_labels and label->value
    """
    data = (
        s.query(Token.token, Token.token_class).filter(Token.stemmer == stemmer).all()
    )
    values: ClassToTokenMap = {}
    valuesbackref = dict(data)
    for k, v in valuesbackref.items():
        values[v] = values.get(v, []) + [k]
    return values, valuesbackref


def load_source(
    s: Session, stemmer="dummy", corpora: list[str] = []
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, list[list[str]]]]]:
    """loads the sources from the specified directory structure

    Args:
        token_func (_type_): the used stemmer as a function. Defaults to None leads to use of dummy stemmer.
        corpora (List[str]): a list of subdirectories. Corresponds to corpora.corpora.
        Defaults to empty list, which leads to reading all subdirectories of corpora/

    Returns:
        Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, List[List[str]]]]]: returns two dictionaries:
            corpora->text_name->fulltext and corpora->text_name->list of tokenized sentences
    """
    if not corpora:
        corpora = global_corpora

    fulltexts: dict[str, dict[str, str]] = {}
    tokenized: dict[str, dict[str, list[list[str]]]] = {}
    for corpus in corpora:
        # print(corpus)
        data = s.query(Text.name, Text.fulltext).filter(Text.corpus == corpus).all()
        fulltexts[corpus] = dict(data)
        tokenized[corpus] = {}
        for textname in fulltexts[corpus].keys():
            # print(textname)
            tokenized[corpus][textname] = []
            data = (
                s.query(Word, Sentence, Text)
                .filter(
                    Word.sentence_id == Sentence.id,
                    Sentence.text_id == Text.id,
                    Text.name == textname,
                    Word.stemmer == stemmer,
                )
                .order_by(Sentence.order, Word.order)
                .all()
            )
            sent_id = None
            sent: list[str] = []
            for w, sentence, t in data:
                if sentence.id != sent_id:
                    sent_id = sentence.id
                    if sent:
                        tokenized[corpus][textname] += [sent]
                    sent = [w.word]
                else:
                    sent += [w.word]
            tokenized[corpus][textname] += [sent]

    return fulltexts, tokenized


def calc_occurences(
    s: Session, stemmer: str = "dummy", flat: bool = False
) -> tuple[
    dict[tuple[str, str], int], dict[str, dict[str, int]], dict[str, dict[str, int]]
]:
    """_Calculate occurences of words_

    Args:
        values (Dict[str, List[str]]): the dictionary mapping values to list of synonym labels, e.g. produced by tokenize_values()
        tokenized (Dict[str, Dict[str, List[List[str]]]]): the tokenized text content, produced by load_source()
        stemmer (str, optional): The used stemmer, notice that stemmer is an idempotent function,
        i.e. applying it twice produces the same result. Defaults to "dummy".

    Returns:
        Tuple[ Dict[Tuple[str, str], int], Dict[str, Dict[str, int]], Dict[str, Dict[str, int]] ]: returns three counting dictionaries:
            (text_name, value): count, text_name: (value: count), value: (text_name: count),
            where text_name is in the format <corpus>/<chapter>_<text> (no extension)
    """
    # print(tokenized)
    token_func = stemmers[stemmer]
    occurences: dict[tuple[str, str], int] = {}  # (text_name, value): count)
    occurences_tv: dict[str, dict[str, int]] = {}  # text_name: (value: count)
    occurences_backref: dict[str, dict[str, int]] = {}  # value: (text_name:count)

    token_col = Token.token if flat else Token.token_class
    data = (
        s.query(
            Text.corpus + expression.literal("/") + Text.name,
            func.lower(token_col),
            func.count(distinct(Word.id)).label("cnt"),
        )
        # s.query(func.concat(Text.corpus, expression.literal("/"), Text.name), func.lower(Token.token_class), func.count(distinct(Word.id)).label('cnt'))
        .join(Sentence, Sentence.text_id == Text.id)
        .join(Word, Word.sentence_id == Sentence.id)
        .filter(
            Word.word == Token.token,
            Word.stemmer == Token.stemmer,
            Word.stemmer == stemmer,
        )
        .group_by(Text.name, token_col)
        .all()
    )

    occurences = dict(((text, value), count) for text, value, count in data)

    for text, value, count in data:
        if text in occurences_tv:
            assert value not in occurences_tv[text]
            occurences_tv[text][value] = count
        else:
            occurences_tv[text] = {value: count}

        if value in occurences_backref:
            assert text not in occurences_backref[value]
            occurences_backref[value][text] = count
        else:
            occurences_backref[value] = {text: count}

    return occurences, occurences_tv, occurences_backref


def get_stemmer2vocab(s: Session):
    q = """SELECT count(words.id), words.stemmer, token_class  FROM words, tokens
    WHERE words.word = tokens.token AND words.stemmer = tokens.stemmer
    GROUP BY words.stemmer, token_class;"""
    data = s.execute(q)
    result: dict[str, dict[str, int]] = {}
    for cnt, stem, token in data:
        if token not in result:
            result[token] = {}
        assert stem not in result[token], "Two records with repeated data"
        result[token][stem] = cnt

    return result


if __name__ == "__main__":
    s = Session()
    stem = "wnl"
    # values, valuesbackref = tokenize_values(s, stem)
    # print(values)
    # print(valuesbackref)
    # fulltexts, tokenized = load_source()
    # print(tokenized["full"])
