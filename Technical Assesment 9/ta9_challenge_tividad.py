import json
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_folder, "JEOPARDY_QUESTIONS1.json")

with open(json_path, "r") as json_file:
    all_questions = json.load(json_file)

print("total questions: " + str(len(all_questions)))

# removes duplicates
unique_questions = []
seen_lookup = {}
for item in all_questions:
    question_text = item["question"]
    if question_text not in seen_lookup:
        seen_lookup[question_text] = True
        unique_questions.append(item)

print("after removing duplicates: " + str(len(unique_questions)))

# cleans text
def clean_text(raw_text):
    # lowercase everything
    text = raw_text.lower()

    # remove html tags first (some clues have links like <a href=...>)
    text = re.sub("<[^>]+>", " ", text)

    # remove punctuation, digits, and special characters
    text = re.sub("[^a-z]", " ", text)

    # remove extra spaces
    text = re.sub("\\s+", " ", text)
    return text.strip()


for item in unique_questions:
    item["clean_question"] = clean_text(item["question"])

# stop words
stop_words = ["is", "you", "your", "and", "the", "to", "from", "or", "for", "do",
              "get", "not", "here", "in", "have", "on", "this", "that", "of", "a",
              "an", "as", "it", "its", "by", "with", "was", "were", "be", "are",
              "at", "his", "her", "he", "she", "their", "they", "one", "which",
              "who", "what", "when", "where", "name", "known", "called", "about",
              "than", "has", "had", "but", "into", "out", "these", "those", "can",
              "been", "also", "more", "most", "said", "say", "s", "t"]

# words that are only in this dataset and are not useful (found by looking at the first clouds)
# "clue" and "crew" come from the "Clue Crew" video clues
jeopardy_stop_words = ["clue", "crew", "seen", "like", "called", "jeopardy"]

# builds the wordcloud
def make_word_cloud(question_list, title, file_name, extra_stop_words):
    # join all the cleaned questions into one big string
    # (we put them in a list first and join once, because adding to a string
    # one by one is very slow when there are almost 100,000 questions)
    all_clean_questions = []
    for item in question_list:
        all_clean_questions.append(item["clean_question"])
    big_text = " ".join(all_clean_questions)

    all_stop_words = set(stop_words + extra_stop_words)

    word_cloud = WordCloud(width=800, height=800, background_color="black",
                           stopwords=all_stop_words, max_words=100,
                           min_font_size=10).generate(big_text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(word_cloud)
    plt.title(title)
    plt.axis("off")
    plt.savefig(file_name, dpi=120, bbox_inches="tight")
    plt.close()
    print("saved " + file_name + " (" + str(len(question_list)) + " questions)")

# comparison of categories: science, literature, and sports
science_questions = []
literature_questions = []
sports_questions = []
for item in unique_questions:
    if item["category"] == "SCIENCE":
        science_questions.append(item)
    elif item["category"] == "LITERATURE":
        literature_questions.append(item)
    elif item["category"] == "SPORTS":
        sports_questions.append(item)

make_word_cloud(science_questions, "SCIENCE", "cloud_science.png", jeopardy_stop_words)
make_word_cloud(literature_questions, "LITERATURE", "cloud_literature.png", jeopardy_stop_words)
make_word_cloud(sports_questions, "SPORTS", "cloud_sports.png", jeopardy_stop_words)