import pandas as pd
from tabulate import tabulate
import PersInfo

YourId=PersInfo.YourId #Твой Рег.№ номер
ExamScore=PersInfo.ExamScore    #Баллы егэ
def DataProc(df):
    
    df["Рег.№"]=df["Рег.№"].astype(str)
    df.loc[df["Вступительные испытания по предметам"]=="Без вступительных испытаний","Сумма конкурсных баллов"]=310
    c=[
        "Образовательная/магистерская программа (институт/филиал)","Вступительные испытания по предметам",
        "Вступительные испытания по предметам.1","Вступительные испытания по предметам.2",
        "Вступительные испытания по предметам.3","Индивидуальные достижения"
    ]
    df=df.drop(columns =c ,axis = 1)

    df=df.dropna(subset=['Сумма конкурсных баллов'])

    d=['Выбыл из конкурса',
     'Выбыл из конкурса(Новое)',
     'Выбыл из конкурса(Рассмотрение заявления)',
     'Забрал документы',
     'Забрал документы(Отзыв заявления)',
     'Забрал документы(Рассмотрение заявления)',
     'Забрал документы(Отклонено)',
     "Выбыл из конкурса(Получено вузом)",
     ]
    df=df[~df['Состояние(статус госуслуг)'].isin(d)]
    df=df[~df['Сумма конкурсных баллов'].isin(d)]
    GreenP=list(df[(df["Заявление о согласии на зачисление"]=="Да") & (df["Оригинал документа об образовании"]=="Да")]["Рег.№"])
    df=df[df["Вид конкурса"]=="Общий конкурс"]
    df=df[df["Форма обучения"]=="Очная"]
    df=df[df["Бюджетная (контрактная) основа"]=="бюджетная основа"]
    MyDf=df[df["Рег.№"]==YourId]
    fp=list(MyDf["Направление (специальность)"])

    df["Сумма конкурсных баллов"]=df["Сумма конкурсных баллов"].astype(float)
    df["Сумма конкурсных баллов"]=df["Сумма конкурсных баллов"].astype(int)
    df=df.sort_values("Сумма конкурсных баллов",ascending=False)
    df=df.reset_index()
    df = df.loc[(df["Рег.№"].isin(GreenP) & (df["Заявление о согласии на зачисление"]=="Да")) | ~df["Рег.№"].isin(GreenP)]

    df2=df[df["Направление (специальность)"].isin(fp)]

    df2.to_csv("dataURFU_VS_ME.csv")

    dfW=df2[df2["Сумма конкурсных баллов"]>=ExamScore]
    dfL=df2[df2["Сумма конкурсных баллов"]<ExamScore]
    dfG=dfW[dfW["Рег.№"].isin(GreenP)]


    pL=dfL.groupby("Направление (специальность)")["Рег.№"].count()
    pW=dfW.groupby("Направление (специальность)")["Рег.№"].count()
    pG=dfG.groupby("Направление (специальность)")["Рег.№"].count()
    pM=df2.groupby("Направление (специальность)")["Сумма конкурсных баллов"]

    pM=pM.apply(lambda x:x.to_list())
    pM=pM.apply(lambda x:x[100])

    res=pd.DataFrame()
    res["Направление"]=pL.keys()
    res["Лучше меня"]=pW.values
    res["Хуже меня"]=pL.values
    res["Я лучше чем"]=((pL.values/(pL.values+pW.values))*100).round(1)
    res["Я лучше чем"]=res["Я лучше чем"]
    res["Зеленых лучше меня"]=pG.values
    res["Балл 100ого"]=pM.values
    print(tabulate(res,headers='keys', tablefmt='psql'))
    return res
