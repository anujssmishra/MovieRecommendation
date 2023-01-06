# Import those libraries
import pandas as pd
from scipy.stats import pearsonr

# Import your data into Python
df = pd.read_csv("Data_JPM.csv")

# Convert dataframe into series
list1 = df['Gross Worldwide (inflation adjusted)']
list2 = df['IMDB Rating']

# Apply the pearsonr()
corr, _ = pearsonr(list1, list2)
print('Pearsons correlation: %.3f' % corr)