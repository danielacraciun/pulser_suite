import numpy as np
from pandas import scatter_matrix

from constants import PAMAP_HEADERS
from pamap_processor import PamapProcessor
import matplotlib.pyplot as plt

test_url = '../ds/pamap2/Optional/subject106.dat'
pp = PamapProcessor(url=test_url, size=53)
data = pp.get_data(url=test_url)
# Univariate Histograms
# data.hist()
# plt.show()

# Univariate Density Plots
# data.plot(kind='density', subplots=True, layout=(8, 8), sharex=False)
# plt.show()

# Boxplot
# data.plot(kind='box', subplots=True, layout=(8, 8), sharex=False, sharey=False)
# plt.show()

# Correction Matrix Plot
correlations = data.corr()

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlations, vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,9,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(PAMAP_HEADERS)
ax.set_yticklabels(PAMAP_HEADERS)
plt.show()

# Scatterplot Matrix
scatter_matrix(data)
plt.show()