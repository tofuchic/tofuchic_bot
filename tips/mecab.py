# pip install unidic-liteが前提
import MeCab
tagger = MeCab.Tagger("-Owakati")
text = 'とーふがいない'
print(tagger.parse(text).split())
