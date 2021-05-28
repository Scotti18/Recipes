import nltk
from nltk import tokenize
from nltk.stem import wordnet, WordNetLemmatizer
from nltk.tokenize.api import StringTokenizer
import re

stringlist = [
    "400 g pasta of choice ((spaghetti, fettucini, bucantini, or gluten-free if preferred))",
    "1/2 cup sun-dried tomatoes (the dry kind, not in oil), (sliced )",
    "1 Prise Oregano, getrocknet",
    "½ tsp freshly ground black pepper",
    "3/4 teaspoon black salt ((also called kala namak), use regular salt if preferred)",
]

# remove all that is in between brackets
newlist = [re.sub("[\(\[].*?[\)\]]", "", string) for string in stringlist]

# remove all punctuation except inbetween numbers
regex = r"(?<!\d)[.,;:](?!\d)"
reducedlist = [re.sub(regex, "", string, 0) for string in newlist]

# remove remaining commass, brackets, whitespaces and tokenize
tokenlist = [
    string.replace(",", "").replace(")", "").rstrip().split(" ") for string in newlist
]

# lemmatize words to base form
word_lem = WordNetLemmatizer()
lemlist = []
for ingredient in tokenlist:
    lem_ing = [word_lem.lemmatize(word) for word in ingredient]
    lemlist.append(lem_ing)


print(lemlist)
