import csv
import nltk
from sys import exit
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


waste_words = set(['bin', 'waste', 'rubbish', 'refuse', 'collection'])

# returns True if any of the words in list are contained in the string, 
# False otherwise
def anyWordInString(list, string):
	return any(subs in string for subs in list)

# return a list of facebook messages that relate to waste
def getFBWasteMessages(waste_words, messages):
	waste_messages =[]
	for message in messages:
		if (anyWordInString(waste_words, message['message']) and 
			wasteWordsUsedInContext(waste_words, message['message'])):
			waste_messages.append(message)
	return waste_messages

# return True if any of the waste_words are used in a message in a way that 
# indicates the message relates to waste
def wasteWordsUsedInContext(waste_words, message):
	
	words = nltk.word_tokenize(message)
	tags = nltk.pos_tag(words)
	rubbish_results = [i for i in tags if i[0].lower() == 'rubbish']
	if rubbish_results:
		# is 'rubbish' used as a noun at least once?
		parts_of_speech = [tag[1] for tag in rubbish_results]
		return ('NN' in parts_of_speech)
	else:
		return True

# get all FB messages that are from council users (not staff) and are more than
# 10 words long
# returns a list of dicts
def getFBMessages(inputfile):
	messages = []

	count = 0

	with open(inputfile, 'rU') as f:
		reader = csv.DictReader(f, delimiter = ',')
		for row in reader:
			message = {}
			
			if (validRow(row)):
				message['date'] = row['Date']
				# get rid of any strange characters in fb messages
				message['message'] = row['Message'].decode('utf-8', 'ignore')
				messages.append(message)
			# for dev only - limit number of messages returned
			# count += 1
			# if count > 4000:
			# 	return messages
	return messages

# Returns True if 1) a row has a non-empty ParentID field (it's a comment 
# from Stirling Council), 2) the message is more than 10 words long (otherwise
# it's too short for sentiment analysis)
def validRow(row):
	StirlingStaffPost = (row['ParentID'].strip() == "")
	moreThan10Words = (len(row['Message'].split()) > 10)
	return (not(StirlingStaffPost) and moreThan10Words)

def validateMessages(messages):

	for row in messages:
		assert(len(row['message'].split()) > 10)
	

def analyzeSentiments(messages):
	sentiments = []
	for message in messages:
		sid = SentimentIntensityAnalyzer()

		ss = sid.polarity_scores(message['message'])

	   	message['positive'] = ss['pos']
	   	message['negative'] = ss['neg']
	   	message['neutral'] = ss['neu']

	   	sentiments.append(message)

	return sentiments

# write sentiment data to a csv file
def writeSentimentDataToFile(sentiment_data, outputfile):

	keys = ['date', 'positive','negative']
	try:
		with open(outputfile, 'wb') as f:
			writer = csv.DictWriter(f, keys)
			writer.writeheader()
			for row in sentiment_data:
				try:
					writer.writerow(row)
				except:
					# skip any message we can't write to the file
					print "Skipping message with strange characters"
					continue
	except:
		print ("Unable to write %s to output file") % row
		sys.exit(0)
	return

# the dates of the fb messages are anonomysed. They are grouped by month.
# e.g. all messages from June 2016 will be 1/06/2016
def sortSentimentData(sentiment_data):
	# print sorted(sentiment_data, key=lambda k: datetime.strptime(k['date'], format="%x")) 
	return sorted(sentiment_data, key=lambda k: datetime.strptime(k['date'], '%x')) 

# bundles up all messages by month, aggregating pos, neutral and neg scores

def groupSentimentData(sentiment_data):
	
	# the data needs to be sorted by date
	sentiment_data = sortSentimentData(sentiment_data)

	grouped_sentiments_by_month = []
	count =0 
	pos=neg=neu = 0
	last_date = ""
	msg = {}
	for message in sentiment_data:
		date = message['date']
		pos += message['positive']
		neg += message['negative']
	
		count += 1
		if date != last_date:
			last_date = date
			msg['date'] = date
			msg['positive'] = round(pos/count,2)
			msg['negative'] = round(neg/count,2)
			count = 0
			grouped_sentiments_by_month.append(msg)
			msg = {}
		else:
			last_date == date
	
	return grouped_sentiments_by_month

# year is 2-digit string e.g. '17'
def filterSentimentDataByYear(sentiment_data, year):
	# only keep data for the specified year
	data = [row for row in sentiment_data if row['date'].endswith(str(year))]
	#  sort before returning
	return sorted(data, key=lambda k: datetime.strptime(k['date'], '%x'))


def generateSentimentGraph(sentiment_data, outputfile_prefix, year):
	
	df = pd.DataFrame(sentiment_data)
	df.set_index('date', inplace=True)
	
	bar = df.plot.bar(figsize=(15,10))

	# save the results as an image
	fig = bar.get_figure()
	fig.suptitle("Sentiment Analysis of Waste-related Facebook Posts ('" + str(year) + ")", fontsize=30)
	plt.xlabel('Date', fontsize=20)
	plt.ylabel('Aggregated Average Sentiment Score', fontsize=20)
	fig.savefig(outputfile_prefix + str(year) + '.png')


###########################################################################

# get all the messages from the file
messages = getFBMessages('facebookData.csv')

# extract only messages that relate to waste
waste_messages = getFBWasteMessages(waste_words, messages)

sentiment_data = analyzeSentiments(waste_messages)

sentiment_data = groupSentimentData(sentiment_data)

for year in range(11,17):

	filtered_data = filterSentimentDataByYear(sentiment_data, year)
	generateSentimentGraph(filtered_data, 'facebook_sentiments', year)

writeSentimentDataToFile(sentiment_data, 'sentiment_data.csv')








