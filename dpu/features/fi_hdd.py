"""
The HDD dataset has various features and is not as sparse as the PAMAP dataset.
It 
"""
import matplotlib.pyplot as plt
from xgboost import plot_importance

from processors.hdd_processor import HddProcessor

pp = HddProcessor(size=57)
pp.run()

# plot feature importance
m = pp.get_model

plot_importance(m)
plt.show()

# Conclusion: this plots shows that the most important results are the time frame
# which is measured in seconds (so it can be correlated with time) and
# heart rate. The various measure from sensors didn't seem to affect
# final results too much but the one who had the highest importance was
# the chest tracker