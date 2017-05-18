import matplotlib.pyplot as plt
from xgboost import plot_tree

from processors.pamap_processor import PamapProcessor
test_url = '../ds/pamap2/Optional/subject106.dat'

pp = PamapProcessor(url=test_url, impute=True, size=53)
pp.run()
model = pp.get_model
plot_tree(model)
plt.show()