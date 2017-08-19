# simple-conlang-generator

A word generator for your conlang in Python 3.

Reddit thread [here](https://www.reddit.com/r/conlangs/comments/6sdalz/simple_word_generator_written_in_python/)


## help

`set ph <typeOfPhoneme> <phonemes>` - set class of phonemes typed with a single string

`set ex <exception1> [exception2] [exception3] ... [exceptionN]` - add/remove forbidden phonemic sequences

`reset` - reset phonemic invertory

`load ph <filename>` - load phonemic invertory from file

`load ex <filename>` - load forbidden phonemic sequences from file

`save ph <filename>` - save phonemic invertory to file

`save ex <filename>` - save forbidden phonemic sequences to file

`gen <phonemicPattern> [amountOfWords]` - generate words

`savewords <filename>` - save wordlist to file

`exit` - close program

## testing

install requirements
```
pip install -r requirements-test.txt
```

```
coverage run -m unittest discover -s tests -t tests
coverage report
```