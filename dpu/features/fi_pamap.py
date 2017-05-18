"""
The PAMAP dataset has various features, this outlines the ones who are
most important in determining the final accuracy (this is done for excluding 
the ones which are irrelevant). subject108 was chosen as sample because his
actions covers the most activities (check details/PerformedActivitySummary.pdf)
"""
import matplotlib.pyplot as plt
from xgboost import plot_importance

from pamap_processor import PamapProcessor

test_url = '../ds/pamap2/Protocol/subject106.dat'

pp = PamapProcessor(url=test_url, impute=True, size=53)
print(pp.run())

# plot feature importance
m = pp.get_model

plot_importance(m)
plt.show()

# Conclusion: this plots shows that the most important results are the time frame
# which is measured in seconds (so it can be correlated with time) and
# heart rate. The various measure from sensors didn't seem to affect (position and temperature)
# final results too much but the one who had the highest importance was
# the chest tracker