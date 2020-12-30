import MeCab
tagger = MeCab.Tagger("-Owakati")
text = 'とーふがいない'
print(tagger.parse(text).split())
