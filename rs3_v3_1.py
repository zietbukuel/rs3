import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the data
df = pd.read_csv('normalized_data.csv')

# Extract the date from the 'title' column
df['date'] = df['title'].apply(lambda x: re.search(r'\d{1,2} [A-Za-z]+ \d{4}', x).group() if re.search(r'\d{1,2} [A-Za-z]+ \d{4}', x) else None)

# Check the new 'date' column
print(df.head())

# Plot the number of incidents over time
df.groupby('date')['title'].count().plot(kind='line')
plt.title('Number of Incidents Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Incidents')
plt.show()