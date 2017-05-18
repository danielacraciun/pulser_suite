"""
The PAMAP dataset is sparse, and this file aims to
test how different ways of replacing nan values affect results
"""
import numpy as np
import matplotlib.pyplot as plt

from pamap_processor import PamapProcessor

test_url = '../ds/pamap2/Optional/subject106.dat'
# Replace not a number values with 0
pp1 = PamapProcessor(url=test_url, nan_replacement=0)
pp2 = PamapProcessor(url=test_url, nan_replacement=1)
pp3 = PamapProcessor(url=test_url, impute=True)

with_0 = pp1.run()
with_1 = pp2.run()
with_imp = pp3.run()
arr = [with_0, with_1, with_imp]

index = np.arange(3)
bar_width = 0.25
rects2 = plt.bar(index + bar_width / 2, arr)
plt.xlabel('Type of replacement')
plt.ylabel('Accuracy')
plt.title('Accuracy by NaN replacement method')
plt.xticks(index + bar_width / 2, ('0', '1', 'mean',))
axes = plt.gca()
axes.set_ylim([min(arr) - 0.1, max(arr) + 0.1 if max(arr) < 9.9 else 100])
plt.tight_layout()
plt.show()