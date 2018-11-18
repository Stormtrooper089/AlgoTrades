import LoadTickData as fileLoader
import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
#filePath="/home/ashish/Desktop/JINDALSTEL.txt"
filePath = os.path.join(os.path.dirname(__file__), 'JINDALSTEL.txt')


def generateBuySignals(list):
    buyList=[]
    popen,pclose,pquantity=0,0,0
    for entry in list:
        buyEntry=[]
        if (popen<=float(entry[3]) and pclose<=float(entry[6]) and pquantity<=float(entry[7])):
            buyEntry.append(entry[2])
            buyEntry.append(entry[6])
            buyEntry.append("Buy")
            buyList.append(buyEntry)
        popen=float(entry[3])
        pclose=float(entry[6])
        pquantity=float(entry[7])
    return buyList

def generateSellSignals(list):
    sellList = []
    popen, pclose, pquantity = 0, 0, 0
    for entry in list:
        sellEntry = []
        if (popen >= float(entry[3]) and pclose >= float(entry[6]) and pquantity >= float(entry[7])):
            sellEntry.append(entry[2])
            sellEntry.append(entry[6])
            sellEntry.append("Sell")
            sellList.append(sellEntry)
        popen = float(entry[3])
        pclose = float(entry[6])
        pquantity = float(entry[7])
    return sellList


def jindalStel():
    list=fileLoader.loadTickData(filePath)
    #print(list)
    completeDataFrame=analyzeData(list)
    buyList=generateBuySignals(list)
    sellList=generateSellSignals(list)
    signalDataFrame=signalPlot(buyList,sellList)
    finalList=verifySignals(completeDataFrame,signalDataFrame)
    resultPlot(finalList)
    pass

def analyzeData(list):
    labels=['scrip','date','time','open','high','low','close','quantity','zero']
    df=pd.DataFrame.from_records(list,columns=labels)
    #print(df)
    return list



def verifySignals(cdf,sdf):
    #print(cdf)
    #print(sdf)
    # coefOfPatience is the time limit to wait to clear the trade, try it's varying value to see the effect
    coefOfPatience = 0.15
    finalList=[]
    for derived in sdf:
        val=str(derived[0])
        timeEntry=float(val.replace(":","."))+coefOfPatience
        timeEntry=str(timeEntry).replace(".",":")
        #print(timeEntry)
        finalProb=[]
        found=0
        for original in cdf:
            if timeEntry==original[2] and found==0:
                found=1
                if derived[2]=='Buy':
                    if derived[1]<=original[6]:
                        finalProb=derived
                        finalProb.append(original[6])
                        finalProb.append("Success")
                        #print("success")
                    else:
                        finalProb = derived
                        finalProb.append(original[6])
                        finalProb.append("Failure")
                        #print("Failure")

                else:
                    if derived[1]>=original[6]:
                        finalProb = derived
                        finalProb.append(original[6])
                        finalProb.append("Success")
                        #print("success")
                    else:
                        finalProb = derived
                        finalProb.append(original[6])
                        finalProb.append("Failure")
                        #print("Failure")

                finalList.append(finalProb)
    #print(finalList)
    return(finalList)

# def sellSignalPlot(sellList,list):
#     labels=['time','price','action']
#     df=pd.DataFrame.from_records(list,columns=labels)
#     print(df)
#     pass


def signalPlot(buyList,sellList):
    cummulativeSignalList=buyList+sellList
    SignalList=sorted(cummulativeSignalList,key=lambda time:time[0])
    labels=['time','price','action']
    df=pd.DataFrame.from_records(SignalList,columns=labels)
    df=df.drop_duplicates()
    print(df)
    return list(SignalList for SignalList,_ in itertools.groupby(SignalList))

def resultPlot(finalList):
    labels=['time','price','action','close_price','outcome']
    df=pd.DataFrame.from_records(finalList,columns=labels)
    print(df)
    calculatePercentSuccess(finalList)
    pass


def calculatePercentSuccess(finalList):
    success=0
    count=0
    winVal=0
    loseVal=0

    for i in finalList:
        if i[4]=='Success':
            success+=1
            winVal+=abs(float(i[1])-float(i[3]))
            print (i)
        else:
            loseVal += abs(float(i[1]) - float(i[3]))
        count+=1


    print("The probability of this strategy to Win" + "----" +str(float(success*100/count)))
    print("Wealth generated per lot of 2250 shares will be " + "----*   " + str(2250 * (winVal - loseVal)))
    pass
