#スクレイピング用
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import re
import ssl
#Gmail作成用
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


ssl._create_default_https_context = ssl._create_unverified_context


#------------------------------------
#HTMLソースをbeautifulsoupで取得
def htmlAccess(url):
	#urlにアクセスして、html取得
	html = urllib.request.urlopen(url);
	#htmlをbeautifulsoupで操作
	soup = BeautifulSoup(html, "html.parser");
	return soup;

#Gmailのメッセージを作成
def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg

#Gmailアカウントから送信
def send(from_addr, to_addrs, my_password, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, my_password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()
#------------------------------------


today = datetime.now(timezone('Asia/Tokyo'));#現在年月日時分秒曜日取得
year = today.year;
year = str(year);
month = today.month;
day = today.day;
day = str(day);
weekday = today.weekday();#曜日を数字で取得

#曜日を数字から英語に変換
weekdays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun');
weekday = weekdays[weekday];
#月を数字から英語に変換
months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
month = months[month-1];

#アーカイブページにアクセス
url_recent = "https://arxiv.org/list/astro-ph.EP/recent/";
soup = htmlAccess(url_recent);


#h3タグを日付でフィルタリング
filter_today = weekday + ", " + day + " " + month + " " + year;
#filter_today = "Fri, 1 Jun 2018"
h3_tag = soup.h3;
if filter_today in h3_tag:
	url_articles = h3_tag.find_next("dl").find_all(href=re.compile("/abs/"));#指定日の論文URLタグを取得
	url_articles = str(url_articles);#strに変換

	pattern = r'<a href=\"(\/abs\/[0-9]{1,}\.[0-9]{1,})\"\s';
	pattern_comp = re.compile(pattern);
	resultList = pattern_comp.findall(url_articles);

	urlList = [];#各論文へのアクセスURLを格納するリスト
	for value in resultList:
		url_article = "https://arxiv.org" + value;
		urlList.append(url_article);

	articleDict = {};#著者などの各論文の情報を格納
	articles = "";
	title_l = "[<h1 class=\"title mathjax\"><span class=\"descriptor\">Title:</span>";
	title_r = "</h1>]";
	pattern_author = r'<a href=".*">(.*)</a>';
	abstract_l = "[<blockquote class=\"abstract mathjax\">\n<span class=\"descriptor\">Abstract:</span>";
	abstract_r = "</blockquote>]";

	for index, value in enumerate(urlList):
		soup_article = htmlAccess(value);
		articleDict['Title'] = soup_article.select('.title.mathjax');#タイトル取得
		articleDict['Authors'] = soup_article.select('.authors');#著者取得
		articleDict['Abstract'] = soup_article.select('.abstract.mathjax');#アブスト取得
		articleDict['Title'] = str(articleDict['Title']);
		articleDict['Authors'] = str(articleDict['Authors']);
		articleDict['Abstract'] = str(articleDict['Abstract']);
		articleDict['Title'] = articleDict['Title'].lstrip(title_l).rstrip(title_r);
		articleDict['Authors'] = re.findall(pattern_author,articleDict['Authors']);
		articleDict['Authors'] = str(articleDict['Authors']).lstrip("[").rstrip("]");
		articleDict['Abstract'] = articleDict['Abstract'].lstrip(abstract_l).rstrip(abstract_r);
		tmp = "【"+str(index+1)+"】"+"Title:"+articleDict['Title']+"\n\n"+"Author:"+articleDict['Authors']+"\n\n"+"Abstract:"+articleDict['Abstract']+"\n\n\n";
		articles = articles + tmp;

	#メールで送信部分
	fromAddress = '';
	myPassword = '';#二段階認証をオンにした後、生成されたアプリパスワードを使用
	toAddress = '';
	bccAddress = "";
	Subject = '本日のアーカイブ' + '（' + year + '/' + month + '/' + day + '/' + weekday + '）';
	Body = articles;

	if __name__ == '__main__':
		message = create_message(fromAddress, toAddress, bccAddress, Subject, Body);
		send(fromAddress, toAddress, myPassword, message);










