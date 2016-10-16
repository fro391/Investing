import pandas

df1=pandas.read_csv('companylist.csv')
df2=pandas.read_csv('companylist (1).csv')
df3=pandas.read_csv('companylist (2).csv')
df4=pandas.read_csv('companylist (3).csv')
df5=pandas.read_csv('companylist (4).csv')
df6=pandas.read_csv('companylist (5).csv')
df7=pandas.read_csv('companylist (6).csv')
df8=pandas.read_csv('companylist (7).csv')
df9=pandas.read_csv('companylist (8).csv')
df10=pandas.read_csv('companylist (10).csv')
df11=pandas.read_csv('companylist (11).csv')
df12=pandas.read_csv('companylist (12).csv')

df1.to_csv('out.csv')
with open('out.csv','a') as f:
    df2.to_csv(f,header = False)
with open('out.csv','a') as f:
    df3.to_csv(f,header = False)
with open('out.csv','a') as f:
    df4.to_csv(f,header = False)
with open('out.csv','a') as f:
    df5.to_csv(f,header = False)
with open('out.csv','a') as f:
    df6.to_csv(f,header = False)
with open('out.csv','a') as f:
    df7.to_csv(f,header = False)
with open('out.csv','a') as f:
    df8.to_csv(f,header = False)
with open('out.csv','a') as f:
    df9.to_csv(f,header = False)
with open('out.csv','a') as f:
    df10.to_csv(f,header = False)
with open('out.csv','a') as f:
    df11.to_csv(f,header = False)
with open('out.csv','a') as f:
    df12.to_csv(f,header = False)