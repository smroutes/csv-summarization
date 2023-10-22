import pandas as pd
from lamini import getSummary
from flant5base import getSummary as getSummaryFromFlatT5

CSV_FILE = 'feedback.csv'

# import the csv file
df = pd.read_csv(CSV_FILE)

print(f"\n--- Total record found %d ---\n" % (len(df)))
feedbackText = ". ".join(df["What could be improved about this session?"])
topicsText = ". ".join(df['What other topics related to this topic would you like to see covered in future sessions?'])

# feedbackFile = open("feedback.txt", "x")
# feedbackFile.write(feedbackText)
# feedbackFile.close()

print("\n---- LAMINI -----\n")
print("\n Feedback Text \n")
summary = getSummary(feedbackText)
print(summary)

print("\n---- FLAN-t5-base -----\n")
print("\n Feedback Text \n")
summary = getSummaryFromFlatT5(feedbackText)
print(summary)

print("\n---- LAMINI -----\n")
print("\n Topics Text \n")
summary = getSummary(topicsText)
print(summary)

print("\n---- FLAN-t5-base -----\n")
print("\n Topics Text \n")
summary = getSummaryFromFlatT5(topicsText)
print(summary)