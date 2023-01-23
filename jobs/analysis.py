import pandas as pd
import matplotlib.pyplot as plt

data = "jobs.csv"

df = pd.read_csv(data)

number_of_jobs = df.shape[0]

#print(df)
print(f"Total number of jobs: {number_of_jobs}")

# Dictionary containing the frequency that each language has appeared in the job search
language_count = df.astype(bool).sum(axis=0).to_dict()
language_count_sorted = dict(sorted(language_count.items(), key=lambda item: item[1]))
del [language_count_sorted["title"], language_count_sorted["location"], language_count_sorted["url"]]


print(language_count_sorted)

plt.barh(range(len(language_count_sorted)), list(language_count_sorted.values()), align="center")
plt.yticks(range(len(language_count_sorted)), list(language_count_sorted.keys()))

plt.show()