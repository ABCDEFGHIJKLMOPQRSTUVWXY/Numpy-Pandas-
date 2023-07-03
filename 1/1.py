import numpy as np
import pandas as pd

df = pd.DataFrame({
    'Id': [202001, 202002, 202003, 202004, 202005, 202006, 202007, 202008, 202009, 202010],
    'Chinese': [98, 67, 84, 88, 78, 90, 93, 75, 82, 87],
    'Math': [92, 80, 73, 76, 88, 78, 90, 82, 77, 69],
    'English': [88, 79, 90, 73, 79, 83, 81, 91, 71, 78]
})

score = np.array(df)
score = np.column_stack((score, np.mean(score[:, 1:3], axis=1)))
score = np.column_stack((score, np.sum(score[:, 1:3], axis=1)))
score = np.column_stack((score, np.max(score[:, 1:3], axis=1)))
score = np.column_stack((score, np.min(score[:, 1:3], axis=1)))
score = np.column_stack((score, np.ptp(score[:, 1:3], axis=1)))
score = np.column_stack((score, np.var(score[:, 1:3], axis=1)))

result = pd.DataFrame(score, columns=['Id', 'Chinese', 'Math', 'English', 'Mean', 'Sum', 'Max', 'Min', 'Range', 'Variance'])

for i in range(len(result)):
    for j in range(4, len(result.columns)):
        result.iloc[i, j] = int(result.iloc[i, j])

print(result)
print(' ')
print(result['Chinese'])
print(' ')
cache = pd.concat([result['Id'], result['Min'], result['Range'], result['Variance']], axis=1)
print(cache)

result.to_csv('answer_1.csv', index=False, encoding='utf-8-sig')
