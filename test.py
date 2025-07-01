from Dataset import DEvalDataset
from Dataset import WordAlignment
import pandas as pd

ds = DEvalDataset("data.csv")

ds.add_translations("en", pd.Series([
   "The manager liked the hairdresser because he liked the hairstyles offered.",
   "The Polish manager liked the hairdresser because he liked the hairstyles offered.",
   "The manager kissed his girlfriend.",
   "Kim is a manager."
   ])
)

