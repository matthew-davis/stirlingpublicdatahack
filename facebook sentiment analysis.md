# Introduction

The bar charts produced indicate the positive/negative opinions the facebook users express when commenting about waste on Stirling Council’s facebook page (https://www.facebook.com/stirlingcouncil/).

The bar charts range from 2011 to 2017, for which facebook data is available. Each bar chart covers one year and is broken down by month. For each month, two columns are shown: positive and negative. 

# Background

Sentiment Analysis is the process of categorising opinions expressed in a piece of text to determine whether the author is expressing a positive, neutral or negative opinion.

# Method

## Identifying Posts Relating to Waste 

1. A list of key words related to waste services is used to identify user messages which may be related to comments about waste services. This list is 'bin', 'waste', 'rubbish', 'refuse', and ‘collection’.
2. Any facebook posts that have been made by Stirling Council are not included in the analysis. 
3. Posts of less than ten words are not included in the analysis. (They are potentially too short to analyse accurately).
4. If the word ‘rubbish’ is used in a post as anything other than a noun, the post is not included. e.g. in ‘she was rubbish’ rubbish is used as an adjective. 

## Generating Sentiment Analysis Scores

1. All of the posts which have not be discarded should now relate to waste.
2. Each post is analysed using the nltk (Natural Language Toolkit, www.nltk.org) and give a positive, neutral and negative score. The neutral scores are not used.

## Aggregating Scores

1. Scores are grouped by month, and averaged by the number of posts this month with either a positive or negative score. For example, if there 20 posts in February 2016 with a combined positive score of 120, the average will be 120/20 i.e. 6.

# Output

1. For each year from 2011 to 2017, an image file containing a bar chart is generated. 
2. A file sentiment_data.csv is generated which contains the dates of posts (grouped by month) and, for each month, the aggregated average sentiment score for this month, for positive and negative scores.

# Limitations

1. Some posts which contain non-ascii characters and which are unable to be converted into usable text are currently discarded.
2. There are some posts where nltk (used for tagging words depending on the part of speech they represent) does not identify the word ‘rubbish’ as a noun correctly.  
3. There may be other key words relating to waste services that could be added.
4. We described earlier how the part of speech for the key word ‘rubbish’ was used to determine the particular meaning of this word in the context in which it would used. The same could be done for the other key words.