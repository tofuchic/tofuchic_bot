# tofuchic_bot
## key.py
* Twitterの認証情報を記述するファイル
* [key-sample.py](./key-sample.py)を参考にローカル環境で生成する
    * [.gitignore](./.gitignore)に記述しているためgitで管理されない

## trigger.log
* `trigger()`関数が呼び出された時刻を書き出すログファイル
* ストリームAPIを使っていないため、ツイートを重複して確認しないように時刻を参照して無駄に遡らないようにしている

## main.py
* `trigger()`関数に記述したロジックを`python main.py`でトリガーできる

### ToDo
* rubyで動かしていた時代のリスペクト
    * とうふぁぼ機能の実装
    * 固定ツイート機能の実装