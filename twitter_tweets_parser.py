import tweepy
import csv
import os.path

import config
from helpers import Helpers


class Main:

	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_key, config.access_secret)
	api = tweepy.API(auth)

	tweets_requests = 0

	def main_loop(self):
		list_of_users = list_of_users = Helpers.get_list_of_users(file_path=config.users_file)
		for user in list_of_users:
			self.tweets_requests = Helpers.get_data_for_user_and_sleep_if_necessary(request_counter=self.tweets_requests, 
														  						    request_limit=config.tweets_request_quota, 
														  						    method=self.get_all_tweets_for_user(self.api, user))

	@staticmethod
	def get_all_tweets_for_user(api, user):

		print("Selected user: " + user.rstrip())
		all_tweets = []
		latest_tweets = []
		oldest_tweet_id = ""
		requests = 0

		latest_stored_tweet_id = Main.get_latest_stored_tweet_id_for_user(user)
	
		while len(latest_tweets) > 0 or requests == 0:
			requests += 1

			try:
				if oldest_tweet_id == "":
					latest_tweets = api.user_timeline(screen_name=user,
													  count=config.max_tweets_count)
				else:
					latest_tweets = api.user_timeline(screen_name=user,
													  count=config.max_tweets_count,
													  max_id=oldest_tweet_id)
			except Exception, e:
				print e
				pass

			if len(latest_tweets) > 1:
				oldest_tweet_id = latest_tweets[-1].id - 1

			if len(latest_tweets) > 0:
				if isinstance(latest_stored_tweet_id, basestring):
					latest_tweet_id = latest_tweets[0].id
					if int(latest_stored_tweet_id) >= int(latest_tweet_id):
						print "Tweets for " + user.rstrip() + " are up to date - returning \n"
						return requests

				filtered_tweets = Main.filter_tweets_older_than_tweet_with_id(latest_stored_tweet_id, latest_tweets)
				if len(filtered_tweets) != len(latest_tweets):
					print "Reached already stored data - saving remaining " + str(len(filtered_tweets)) + " and returning"
					all_tweets.extend(filtered_tweets)
					break

				all_tweets.extend(latest_tweets)
				print "Appending " + str(len(latest_tweets)) + ", now have " + str(len(all_tweets)) + " tweets"
		Main.prepare_and_save_tweets(all_tweets, user)
		return requests

	@staticmethod
	def get_latest_stored_tweet_id_for_user(user):
		try:
			with open(Helpers.get_file_path_for_user(user=user, 
													 sufix=config.tweets_name), config.read_mode) as file:
				for index, item in enumerate(csv.reader(file, delimiter=",")):
					if index == 1:
						return item[0]
		except Exception, e:
			print e
		return 0

	@staticmethod
	def prepare_and_save_tweets(tweets, user):
		print("Adding: " + str(len(tweets)) + " tweets for " + user.rstrip())
		flat_tweets_array = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]
		Main.save_tweets_for_user(flat_tweets_array, user)

	@staticmethod
	def filter_tweets_older_than_tweet_with_id(id, tweets):
		filtered_tweets = []
		for tweet in tweets:
			if int(tweet.id) > int(id):
				filtered_tweets.append(tweet)
		return filtered_tweets

	@staticmethod
	def save_tweets_for_user(tweets, user):
		Helpers.save_data_to_file(data=tweets, 
								  file_path=Helpers.get_file_path_for_user(user=user,
								  										   sufix=config.tweets_name), 
								  headers=config.tweets_headers, 
								  mode=config.append_mode,
								  single=False)

if __name__ == '__main__':
	Main().main_loop()