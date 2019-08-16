<<<<<<< HEAD
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")

tips = sns.load_dataset("tips")
sns.relplot(x="total_bill", y="tip", hue="smoker", data=tips);
plt.show()
||||||| merged common ancestors
=======
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
>>>>>>> 34671afa686fb0dadc724324fce8c14b8468835a
