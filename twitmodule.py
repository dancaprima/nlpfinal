import tweepy
from tweepy import OAuthHandler
import csv
 
consumer_key = '5irYZYrIuf8NtexFzIi0XeGl2'
consumer_secret = 'qq714ccKL3kBxWnUOqSAfIjkKfDmKKnVfWvZZMsiFfHtKBMV7d'
access_key = '110041356-4ykNsiovCezy5SA9iPGidjnSbL0LYq3pXoWYDSSe'
access_secret = 'i0Cx381tF1DbE335XfZDaydTP6ljh8sv6HyryuVxpSroh'
 
def get_all_tweets(screen_name):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	alltweets = []	
	
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	alltweets.extend(new_tweets)
	
	oldest = alltweets[-1].id - 1
	

	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	

		outtweets = [(tweet.id_str, tweet.text.encode("utf-8")) for tweet in alltweets]

		with open('%s_tweets.csv' % screen_name, 'wb') as f:
						writer = csv.writer(f)
						writer.writerow(["id","tweet"])
						writer.writerows(outtweets)
	
		pass
	# with open('entertainment_file.txt','w') as file:
	# 		for item in outtweets:
	# 				print>>file, item
		# with open("olahraga_training.txt", "w") as text_file:
		# 		for tweet in alltweets:
		# 				text_file.write(tweet.id_str.encode("utf-8")+ ' detik '+ "'{}'".format(tweet.text.encode("utf-8")) + "\n")

		# with open("entertainment_training.txt", "w") as text_file:
		# 		for tweet in alltweets:
		# 				text_file.write(tweet.id_str.encode("utf-8")+ ' Entertainment ' + "'{}'".format(tweet.text.encode("utf-8")) + "\n")


if __name__ == '__main__':
	get_all_tweets("detikcom")