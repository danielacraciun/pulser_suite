"""
This file generates the whole PAMAP2 data brought together
with the main attributes selected
"""
import pandas
from pandas import DataFrame

from constants import pamap_details
from processors.pamap_processor import PamapProcessor

final = "ds/pamap2/spare_test.csv"
# paths = {
#     101: "ds/pamap2/Protocol/subject101.dat",
#     102: "ds/pamap2/Protocol/subject102.dat",
#     103: "ds/pamap2/Protocol/subject103.dat",
#     106: "ds/pamap2/Protocol/subject106.dat",
#     108: "ds/pamap2/Protocol/subject108.dat",
# }
paths = {
105: "ds/pamap2/Protocol/subject105.dat"
}
pp = PamapProcessor(url=paths[105])

frames = []
for subject in paths.keys():
    print("fetching {}".format(subject))
    url = paths[subject]
    details = pamap_details[subject]

    print("reading csv of {}".format(subject))
    df = pp.get_data(url)

    # Get the activity id for prediction
    activities = DataFrame(columns=['activity'])
    activities['activity'] = df[1]

    # Remove unused columns:
    # 0 - timestamp
    # 1 - activity id, this is to predict
    # 3 - body temperature, no way to fetch this
    # 8-10 - inaccurate accel measurements, using the 16g ones
    df.drop(df.columns[[0, 1, 3, 7, 8, 9]], axis=1, inplace=True)

    # insert other details
    print("inserting more detail about {}...".format(subject))
    for k, v in zip(["weight", "height", "age", "sex"], details):
        df.insert(0, k, [v] * df.shape[0])

    df = df.fillna(0)
    # add activity id at the end
    df.insert(0, "activity", activities['activity'])
    print("all set up! appending {} to group of data frames!".format(subject))
    frames.append(df.iloc[:,range(15)])

print("concatenating all {} frames".format(len(frames)))
df = pandas.concat(frames)

print("moving all of them to csv")
df.to_csv(final, sep=',',
          header=['activity', 'weight', 'height', 'age',
                  'sex', 'hr', 'accelx', 'accely', 'accelz',
                  'gyrox', 'gyroy', 'gyroz',
                  'magnetox', 'magnetoy', 'magnetoz', ],
          index=False)
