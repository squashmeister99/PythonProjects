{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# this notebook contains helper functions useful for plotting and feature engineering\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "%matplotlib inline\n",
    "\n",
    "def columnsWithMissingData(X, threshold = 0.9):\n",
    "    # check for null items\n",
    "    null_df = X.columns[X.isnull().any()]\n",
    "    null_count = X[null_df].isnull().sum()/len(X.index)\n",
    "    null_count_above_threshold = null_count.loc[null_count > threshold]\n",
    "    null_count_above_threshold\n",
    "    \n",
    "    #percentage of zero values for each numeric variable\n",
    "    zero_df = X.columns[(X == 0).any()]\n",
    "    zero_count = (X[zero_df] == 0).sum()/len(X.index)\n",
    "    zero_count_above_threshold = zero_count.loc[zero_count > threshold]\n",
    "    missingDataDF = pd.concat([null_count_above_threshold, zero_count_above_threshold])\n",
    "    print(missingDataDF.describe())\n",
    "    return missingDataDF\n",
    "\n",
    "def plotHeatmap(df):\n",
    "    corrmat = df.corr()\n",
    "    f, ax = plt.subplots(figsize=(12, 9))\n",
    "    sns.heatmap(corrmat, vmax=.8, square=True);\n",
    "    plt.show()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
