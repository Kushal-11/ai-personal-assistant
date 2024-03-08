import os
import json

# now that i have the summaries, i need to define a criteria in a flat file in order to rank the summaries

"""
Reading the criteria

"""
with open("hw2_criteria.json", "r") as file:
    criteria = json.load(file)

"""
Looping through the folder containing summaries and ranking each file

"""
def get_score(file_path, keywords):
    score = 0
    with open(file_path, "r", encoding='utf-8') as file:
        content = file.read()
        for keyword in keywords:
            score += content.lower().count(keyword.lower())
    return score

# Scoring each file
file_scores = []

for filename in os.listdir("news_summaries"):
    if filename.endswith(".txt"):
        file_path = f"news_summaries/{filename}"
        score = get_score(file_path, criteria['keywords'])
        file_scores.append((filename, score))

# Sorting the files by score
file_scores.sort(key=lambda x: x[1], reverse=True)

"""
Printing the file names in order of priority

"""

print("File Scores")
print("-----------")
for file, score in file_scores:
    print(f"{file}: {score}")
print('\n')

"""
Selecting the best three text files, and for each of them, print the justification why they were selected

"""
print("Selected Files")
print("--------------")
for file, score in file_scores[:3]:
    print(f"Filename: {file}")
    print(f"Justification: This file has a score of {score} which is one of the highest scores among all the files.")
    print()