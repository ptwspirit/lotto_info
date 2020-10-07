import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

#문자열에서 숫자을 찾아 return
def getNumberFrom(str):
    return int("".join(re.findall("\\d+", str)))
 
# 가장 최근 회차
def getLastLottoRound() :    
    url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=";
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    lastLottoNo = getNumberFrom(soup.select("div.win_result > h4 > strong")[0].get_text())
    return lastLottoNo

# 정보 가져오기
def getLottoData(start, lastLottoNo) :
    print(lastLottoNo)
    
    df = pd.DataFrame(columns=("회차", "추첨일", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6",
                      "보너스번호", "총판매금액",
                      "총1등당첨금", "1등당첨게임수", "1등게임당당첨금액",
                      "총2등당첨금", "2등당첨게임수", "2등게임당당첨금액",
                      "총3등당첨금", "1등당첨게임수", "3등게임당당첨금액",
                      "총4등당첨금", "4등당첨게임수", "4등게임당당첨금액",
                      "총5등당첨금", "5등당첨게임수", "5등게임당당첨금액",
                      "비고"))
    
    # start부터 마지막회차까지 정보 가져오기
    for i in range(start, lastLottoNo+1):        
        # 회차
        url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=";
        round = str(i)
        url = url + round
        

        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
     
        #추첨일
        announceDate = soup.select("div.win_result > p")[0].get_text()        
        dateStr = str(getNumberFrom(announceDate))
     
        #총판매금액
        totMoney = soup.select("div.content_wrap > ul.list_text_common > li > strong")[0].get_text()        
        moneyStr = str(getNumberFrom(totMoney))

        no1 = ""
        no2 = ""
        no3 = ""
        no4 = ""
        no5 = ""
        no6 = ""
        bonusNo = ""

        nos = soup.select("span.ball_645")
        winNo = ""
        bonus= ""
        idx = 0
        for no in nos:
            idx = idx + 1
            winNo = no.get_text()
            if idx == 1 : no1 = winNo
            if idx == 2 : no2 = winNo
            if idx == 3 : no3 = winNo
            if idx == 4 : no4 = winNo
            if idx == 5 : no5 = winNo
            if idx == 6 : no6 = winNo
            if idx == 7 : bonusNo = winNo

            
        winNo1TotalPrize = ""
        winNo1Count = ""
        winNo1PerPrize = ""
        
        winNo2TotalPrize = ""
        winNo2Count = ""
        winNo2PerPrize = ""

        winNo3TotalPrize = ""
        winNo3Count = ""
        winNo3PerPrize = ""

        winNo4TotalPrize = ""
        winNo4Count = ""
        winNo4PerPrize = ""

        winNo5TotalPrize = ""
        winNo5Count = ""
        winNo5PerPrize = ""

        remark = ""
        
        ranks = soup.select("table.tbl_data > tbody > tr")
        for rank in ranks:
            rankNum = getNumberFrom(rank.select("td:nth-of-type(1)")[0].get_text())
            rankTotalPrize = str(getNumberFrom(rank.select("td:nth-of-type(2)")[0].get_text()))
            rankWinNum = str(getNumberFrom(rank.select("td:nth-of-type(3)")[0].get_text()))
            rankPrizePerPeople = str(getNumberFrom(rank.select("td:nth-of-type(4)")[0].get_text()))

            if rankNum == 1 :
                winNo1TotalPrize = rankTotalPrize
                winNo1Count = rankWinNum
                winNo1PerPrize = rankPrizePerPeople

            if rankNum == 2 :
                winNo2TotalPrize = rankTotalPrize
                winNo2Count = rankWinNum
                winNo2PerPrize = rankPrizePerPeople

            if rankNum == 3 :
                winNo3TotalPrize = rankTotalPrize
                winNo3Count = rankWinNum
                winNo3PerPrize = rankPrizePerPeople

            if rankNum == 4 :
                winNo4TotalPrize = rankTotalPrize
                winNo4Count = rankWinNum
                winNo4PerPrize = rankPrizePerPeople

            if rankNum == 5 :
                winNo5TotalPrize = rankTotalPrize
                winNo5Count = rankWinNum
                winNo5PerPrize = rankPrizePerPeople
     
            if(len(rank.select("td")) == 6):
                gameInfo = re.sub("\\s+", "", re.sub("\\n", "^", rank.select("td:nth-of-type(6)")[0].text)) # 비고
                infos = gameInfo.split("^")
                remark = gameInfo
                remark = remark.replace("^", " ")
                remark = re.sub(' +', ' ', remark)
                remark = remark.replace(" ", "", 1)
                
                    
                    
        print("==============================================================")             
        print("회차 : " + round)       
        print("추첨일 : " + dateStr)
        print("총 판매금액 : " + moneyStr)     
        print("번호 : " + no1)
        print("번호 : " + no2)
        print("번호 : " + no3)
        print("번호 : " + no4)
        print("번호 : " + no5)
        print("번호 : " + no6)
        print("보너스번호 : " + bonusNo)
        print("1등 총 당첨금액 : " + winNo1TotalPrize)
        print("1등 총 당첨게임 수 : " + winNo1Count)
        print("1등 1게임당 당첨금액 : " + winNo1PerPrize)        
        print("2등 총 당첨금액 : " + winNo2TotalPrize)
        print("2등 총 당첨게임 수 : " + winNo2Count)
        print("2등 1게임당 당첨금액 : " + winNo2PerPrize)        
        print("3등 총 당첨금액 : " + winNo3TotalPrize)
        print("3등 총 당첨게임 수 : " + winNo3Count)
        print("3등 1게임당 당첨금액 : " + winNo3PerPrize)        
        print("4등 총 당첨금액 : " + winNo4TotalPrize)
        print("4등 총 당첨게임 수 : " + winNo4Count)
        print("4등 1게임당 당첨금액 : " + winNo4PerPrize)        
        print("5등 총 당첨금액 : " + winNo5TotalPrize)
        print("5등 총 당첨게임 수 : " + winNo5Count)
        print("5등 1게임당 당첨금액 : " + winNo5PerPrize)
        print("비고 : " + remark)

        lotto_dict = {"회차":round, "추첨일":dateStr, "번호1":no1, "번호2":no2, "번호3":no3, "번호4":no4, "번호5":no5, "번호6":no6,
                      "보너스번호":bonusNo, "총판매금액":moneyStr,
                      "총1등당첨금":winNo1TotalPrize, "1등당첨게임수":winNo1Count, "1등게임당당첨금액":winNo1PerPrize,
                      "총2등당첨금":winNo2TotalPrize, "2등당첨게임수":winNo2Count, "2등게임당당첨금액":winNo2PerPrize,
                      "총3등당첨금":winNo3TotalPrize, "1등당첨게임수":winNo3Count, "3등게임당당첨금액":winNo3PerPrize,
                      "총4등당첨금":winNo4TotalPrize, "4등당첨게임수":winNo4Count, "4등게임당당첨금액":winNo4PerPrize,
                      "총5등당첨금":winNo5TotalPrize, "5등당첨게임수":winNo5Count, "5등게임당당첨금액":winNo5PerPrize,
                      "비고":remark}        
        df.loc[i] = lotto_dict

    return df
        
if __name__ == '__main__':
    lastLottoRound = getLastLottoRound()
    start = 1
    counter = lastLottoRound - start + 1
    df = getLottoData(start, lastLottoRound)
    if len(df) == counter:
        df.to_csv("lotto_win_number_info.csv", index=False, sep=",", line_terminator='\n', encoding='utf-8')
        print("CSV COMPLETED : " + str(len(df)) + " ROW")
    else :
        print("counter : " + str(counter))
        print("len(df) : " + str(len(df)))
        print("ERROR!")
