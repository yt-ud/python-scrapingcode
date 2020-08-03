import sys
sys.path.append("/app");
import myFunc as mf
import os
from datetime import datetime
from pytz import timezone

f = open('logScraping.txt', 'a');

#ログ項目名を作成
presentYMD = mf.presentDay();
logName = presentYMD[0] + "=";
f.write(logName + "0\n");

f.close();