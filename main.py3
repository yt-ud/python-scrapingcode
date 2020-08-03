import sys
sys.path.append("/app");
import myFunc as mf
import subprocess


with open('logScraping.txt', 'r') as f:#ログファイルの読み込み
	lines = f.readlines();#テキストファイルを一行ごとにリストに読み込み

presentday = mf.presentDay();#今日の年月日を取得


cntLog = 0;#ログ項目の数
#検索対象のログ項目がいくつ作られているか
for line in lines:
	if presentday[0] in line:
		cntLog += 1;
#ログ項目がない場合は作る
if cntLog == 0:
	subprocess.run(['python3', 'makeLog.py3'], check=True);


numCheck = "0";
#スクレイピングコードの実行
for i, val in enumerate(lines):
	if presentday[0] in val:
		val = val.lstrip(presentday[0]);
		val = val.lstrip("=");
		val = val.rstrip("\n");
		if val == numCheck:
			subprocess.run(['python3', 'scrapeArxiv.py3'], check=True);
			lines[i] = presentday[0] + "=1\n";


#スクレイピング部分の実行をログに残す
#fin = open('logScraping.txt', 'w');
#for y in lines:
#	fin.write(y);
#fin.close();



