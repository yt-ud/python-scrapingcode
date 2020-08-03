from datetime import datetime
from pytz import timezone

#現在の年月日を取得
def presentDay():
	today = datetime.now(timezone('Asia/Tokyo'));
	presentday = today.strftime("%Y%m%d");
	weekday = today.strftime("%a");
	return presentday, weekday;
