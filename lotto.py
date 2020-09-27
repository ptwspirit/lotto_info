import pandas as pd
import requests
import json

def getLottoWinInfo(minDrwNo, maxDrwNo):
    lottoRound = []
    drwtNo1 = []
    drwtNo2 = []
    drwtNo3 = []
    drwtNo4 = []
    drwtNo5 = []
    drwtNo6 = []
    bnusNo = []
    totSellamnt = []
    drwNoDate = []
    firstAccumamnt = []
    firstPrzwnerCo = []
    firstWinamnt = []
    
    for i in range(minDrwNo, maxDrwNo+1, 1):
        req_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)
        req_lotto = requests.get(req_url)        
        lottoNo = req_lotto.json()

        lottoRound.append(lottoNo['drwNo'])
        drwtNo1.append(lottoNo['drwtNo1'])
        drwtNo2.append(lottoNo['drwtNo2'])
        drwtNo3.append(lottoNo['drwtNo3'])
        drwtNo4.append(lottoNo['drwtNo4'])
        drwtNo5.append(lottoNo['drwtNo5'])
        drwtNo6.append(lottoNo['drwtNo6'])
        bnusNo.append(lottoNo['bnusNo'])
        totSellamnt.append(lottoNo['totSellamnt'])
        drwNoDate.append(lottoNo['drwNoDate'])
        firstAccumamnt.append(lottoNo['firstAccumamnt'])
        firstPrzwnerCo.append(lottoNo['firstPrzwnerCo'])
        firstWinamnt.append(lottoNo['firstWinamnt'])
        
        lotto_dict = {"회차":lottoRound, "추첨일":drwNoDate, "번호1":drwtNo1, "번호2":drwtNo2, "번호3":drwtNo3, "번호4":drwtNo4, "번호5":drwtNo5, "번호6":drwtNo6,
                      "보너스번호":bnusNo, "총판매금액":totSellamnt, "총1등당첨금":firstAccumamnt, "1등당첨인원":firstPrzwnerCo, 
                      "1등수령액":firstWinamnt}
        
        df_lotto = pd.DataFrame(lotto_dict)
        print("STATUS : " + str(lottoRound[-1]))

    return df_lotto


if __name__ == '__main__':
    start = 1
    end = 930
    df = getLottoWinInfo(start, end)
    print("SHAPE : " + str(df.shape))
    counter = end - start + 1
    print("ROW COUNT : " + str(len(df)))
    print("INPUT COUNTER : " + str(counter))
    if len(df) == counter :
        df.to_csv("lotto_win_info.csv", index=False, sep=",", line_terminator='\n', encoding='utf-8')
        print("CSV COMPLETED : " + str(len(df)) + " ROW")
    else :
        print("ERROR!")
