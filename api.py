import re
from datetime import datetime
from collections import OrderedDict
class api():
	def get_top_words(self,tweet):
		collection_of_word = []
		for s in tweet:
			words = s['text'].split(' ')
			# words = re.split(r'\w',s['text'])
			length = len(words)
			for x in range(0,length):
				if words[x][0] == '@' or re.match(r'\W+',words[x]) == True:
					continue
				collection_of_word.append(words[x])
		collection_of_word = sorted(collection_of_word)

		sorted_result_length = len(collection_of_word)
		offset = 0;
		result = []
		for i in range(1,sorted_result_length):
				if collection_of_word[i-1] != collection_of_word[i]:
					result.append({"words":collection_of_word[i-1],"total_words":((i)-offset) })
					offset = i
		result = sorted(result, key=lambda k: k['total_words'],reverse=True)
		return result

	def get_popular_users(self,tweet):
		tweet = sorted(tweet, key=lambda k: k['total_tweet'],reverse=True)
		result_length = len(tweet)
		popular_users = []
		for x in range(0,(result_length)):
			popular_users.append({"fromuser":tweet[x]["fromuser"],"total_tweet":tweet[x]["total_tweet"]})
		# result_length = len(tweet)
		# popular_users = OrderedDict()
		# for x in range(0,(result_length)):
		# 	popular_users.move_to_end({result[x]["fromuser"]:result[x]["total_tweet"]},last=True)
		return popular_users

	def get_popular_mentions(self,tweet):
		result = []
		data = []
		for s in tweet:
			for x in s['mentions']:
				data.append(x)
		data = sorted(data)
		length = len(data)
		offset = 0
		for i in range(1,length):
			if data[i-1] != data[i] and (i-1) != length - 1:
				result.append({"mentioned_user" : data[i-1],"total_mention" : (i-offset) })
				offset = i
		result = sorted(result, key=lambda k: k['total_mention'],reverse=True)
		# result_length = len(result)
		# popular_mentions = ()
		# for x in range(0,(result_length)):
		# 	data_result = result[x]["name"] + ":" + str(result[x]["total_mention"])
		# 	popular_mentions += (data_result,)
		return result

	def get_hourly_tweet(self,tweet):
		data = []
		for x in tweet:
			ordinal_date = datetime.fromtimestamp(x['createdat'])
			real_date = ordinal_date.strftime('%H')
			data.append({"date": real_date})
		# data = sorted(data)
		data_length = len(data)
		offset = 0
		result = []
		for i in range(1,data_length):
				if data[i-1] != data[i]:
					result.append({	"hour":data[i-1]["date"],"total_tweet":((i)-offset)})
					offset = i
				elif (i+1) == data_length:
					result.append({	"hour":data[i]["date"],"total_tweet":i-(offset-1)})
		hourly_data = []
		result_length = len(result)
		for j in range(0,24):
			isFound = False
			for r in range(0,result_length):
				if int(result[r]["hour"]) == j:
					hourly_data.append({"hour" : result[r]["hour"],"total_tweet" : result[r]["total_tweet"]})
					isFound = True
			if isFound == False:
				hourly_data.append({"hour" : '0'+str(j),"total_tweet" : 0})	
		
		return hourly_data
