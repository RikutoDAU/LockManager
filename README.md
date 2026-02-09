# LockManager

*リグクリーン化のアシストすることを目的としたツール。<br>
*主にリグのアトリビュートのロックや非表示化、ワイヤー色の変更を指定した範囲を一括で行えるもの。<br>
*maya2025以降のversionに対応。(pySide6を使用している関係)<br>

*実装方法<br>
AttributeSetter_logic.pyファイルをMayaが標準で参照するスクリプトのディレクトリの元に置く。<br>
基本例)'C:\Users\%USERNAME%\Documents\maya\2025\ja_JP\scripts\AttributeSetter_logic.py'<br>

*使用方法<br>
AttributeSetter_Gui.pyのスクリプトをMAYAのスクリプトエディタにコピペやシェルフに登録して呼び出す。<br>
<img width="457" height="685" alt="image" src="https://github.com/user-attachments/assets/8d74ed12-b5df-463f-85b3-bd3ecb4c0291" /> <br>
画像のようなウィンドウが出るため、「選択状態 + 語尾の入力」でオブジェクトを指定する。<br>
アトリビュートのロック、ワイヤー色変更をそれぞれ行うものにチェックして"実行"ボタンを押す。<br>
ロック解除や色のリセットは、操作したいオブジェクト（複数でも可)を選択状態にしておき、それぞれのボタンを押す。
