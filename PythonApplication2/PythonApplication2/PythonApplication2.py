import pandas as pd

a = pd.Series([1,2,3,4])
print(a)

b = pd.DataFrame([[1,2], [3,4], [5,6], [7, 8]], columns = ["col1", "col2"], index=['a', 'b', 'c', 'd'])
print(b)
print(b.shape)

c = pd.read_csv("k:/test/sample.csv")

print(c['Country'])
print(c.columns)
print(c.describe())
print(c.info())