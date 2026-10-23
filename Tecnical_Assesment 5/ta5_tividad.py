import csv
import string
from textblob import TextBlob 
from pathlib import Path

def first_activity():
    sentences = []
    for i in range(9):
        sentences.append(input("Enter an item: "))

    for sentence in sentences:
        s = TextBlob(sentence) 
        p = s.sentiment.polarity   
        
        # Negative p<0, Neutral p=0, Positive p>0 if p <0: 
        if p <0: 
            print("Negative") 

        elif p==0: 
            print("Neutral") 

        elif p>0 and p<=1: 
            print("Positive") 

def challenge():
    happy_words = set()
    sad_words = set()

    # gets the text file from the root folder
    dataset_path = (
        Path(__file__).resolve().parent/"NRC-Emotion-Lexicon-Wordlevel-v0.92.txt")

    # translates into a dataset the .txt file
    with open(dataset_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")

        for row in reader:
            if len(row) == 3:
                word = row[0].lower()
                emotion = row[1].lower()
                association = row[2].strip()

                if association == "1":
                    if emotion == "joy":
                        happy_words.add(word)
                    elif emotion == "sadness":
                        sad_words.add(word)

    # cleans and also counts how many happy words are in a sentence
    def number_happy(sentence):
        words = sentence.lower().split()
        count = 0

        for word in words:
            word = word.strip(string.punctuation)

            if word in happy_words:
                count += 1

        return count

    # same logic but with sadness :(
    def number_sad(sentence):
        words = sentence.lower().split()
        count = 0

        for word in words:
            word = word.strip(string.punctuation)

            if word in sad_words:
                count += 1

        return count

    sentence = input("Enter a sentence: ")

    happy_count = number_happy(sentence)
    sad_count = number_sad(sentence)

    print("Number of happy words:", happy_count)
    print("Number of sad words:", sad_count)

    if happy_count > sad_count:
        print("Tone: Positive")

    elif sad_count > happy_count:
        print("Tone: Negative")

    else:
        print("Tone: Neutral")

if __name__ == "__main__":

    # Just remove the comment on of these to try each of the activity
    #first_activity()
    challenge()



