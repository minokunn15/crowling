# クローリングの方法使い方

### 概要
- Pythonで行う
- クローリング対象サイトを変える場合は、各自コードをいじることで対応する
- Python、pipの環境は構築済みを前提とする
- pip install scrapy
- pip install beautifulsoup4

### 起動方法
- scrapy crawl webspider -o result.csv
	- webspider：webspider.pyの14行目に指定してある変数名
	- result.csv：出力したいファイル名

### サイトに合わせたコード変更

1. Chromeでそのサイトに行き、サイト構造の把握
2. クローリングをstartしたいページに行ったら、右クリック⇨「検証」をクリック⇨右上の方にある「画面に矢印マーク」をactiveにして、欲しい情報部分に矢印を当てる
3. 青くなるので、その部分のリンクの `class=×××××` という部分の×××××をコピーなりして取っておく
4. 3で取っておいた部分をwebspider.pyの23行目の `{'class':×××××}`の×××××のとこに当てはめる
5. 次へボタンがある場合、3,4の手続き通りに対応する
6. 個別のページに行き、欲しい情報を2の手順で青くし、右クリック⇨「Copy」⇨「Copy XPath」をクリックする
7. その情報をwebspider.pyの53行目以降の変数名にそれぞれ指定する。（追加や消去は適宜行う）


