# STEP 2: Generating a word cloud and analyzing the data

# If we saved the previous data, we can load it as follows:
whiskies_df = pd.read_csv("Whiskies.csv", index_col=0)
reviews_df = pd.read_csv("Reviews.csv", index_col=0)
major_distillery_df = pd.read_csv("Distilleries.csv", index_col=0)

# DataFrame joins with Pandas if we want to split by area, distillery etc.

whiskies_reviews_df = pd.merge( reviews_df, whiskies_df, left_on="Whisky", right_on="Whisky")
#whiskies_reviews_df.to_csv('Merged.csv')

#print([review for review in reviews_df.Review])
# Word count analysis to determine the major flavor profiles
# Will be conducted in general, per region, and per distillery

is_islay = whiskies_reviews_df.CountryOrRegion == "Scotland Islay"
whiskies_reviews_df_filtered = whiskies_reviews_df[is_islay]

all_reviews_text = " ".join(str(review).lower() for review in whiskies_reviews_df_filtered.Review)
print ("There are {} words in the combination of all review.".format(len(all_reviews_text)))


image=Image.open("img/glencairn_mask.png").convert("P")
glencairn_mask = np.array(image)


def transform_format(val):
    if val == 1:
        return 255
    else:
        return val


transformed_glencairn_mask = np.ndarray((glencairn_mask.shape[0],glencairn_mask.shape[1]), np.int32)

for i in range(len(glencairn_mask)):
    transformed_glencairn_mask[i] = list(map(transform_format, glencairn_mask[i]))


# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["note", "notes", "nose", "finish", "time", "like", "bit", "nan", "quite", "just"])

# Generate a word cloud image
wordcloud = WordCloud(max_words=100, stopwords=stopwords, background_color="white", mask = transformed_glencairn_mask, contour_width=3, contour_color='black').generate(all_reviews_text)

# Display the generated image:
# the matplotlib way:
#plt.figure( figsize=(20,10) )
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()




def get_top_n_words(corpus, n=None):
    # Props to Cristhian Boujon, https://medium.com/@cristhianboujon/how-to-list-the-most-common-words-from-text-corpus-using-scikit-learn-dad4d0cab41d
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.

    get_top_n_words(["I love Python", "Python is a language programming", "Hello world", "I love the world"]) ->
    [('python', 2),('world', 2),('love', 2),('hello', 1),('is', 1),('programming', 1),('the', 1),('language', 1)]
    """
    vec = CountVectorizer(stop_words= 'english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


common_words = get_top_n_words([str(review).lower() for review in reviews_df.Review])
common_words_df = pd.DataFrame(data = common_words, columns= ("Word", "Count"))
common_words_df.to_csv('MostCommonWordsIslay.csv')


print(common_words)

end_time = time.perf_counter()
print(f"Code executed in {end_time - zero_time:0.4f} seconds.")