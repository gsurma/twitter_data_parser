import tweepy
import csv
import os.path

import config
from helpers import Helpers


class Main:

	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_key, config.access_secret)
	api = tweepy.API(auth)

	account_data_requests = 0

	def main_loop(self):
		list_of_users = Helpers.get_list_of_users(file_path=config.users_file)
		for user in list_of_users:
			print "Getting data for " + user
			self.account_data_requests = Helpers.get_data_for_user_and_sleep_if_necessary(request_counter=self.account_data_requests,
			 													   						  request_limit=config.account_data_request_quota,
			 													   						  method=Main.get_account_data_for_user(self.api, user))
		self.save_account_data_for_all_users()

	@staticmethod
	def get_account_data_for_user(api, user):
		try:
			account_data =  api.get_user(screen_name=user)
			Main.prepare_and_save_account_data_for_user(account_data, user)
		except Exception, e:
			print e
			pass
		return 1

	@staticmethod
	def prepare_and_save_account_data_for_user(data, user):
		prepared_data = [data.friends_count,
						 data.followers_count,
						 data.favourites_count, 
						 data.geo_enabled, data.listed_count, 
						 data.verified, data.created_at, 
						 data.location, data.id, 
						 data.name]
		Helpers.save_data_to_file(data=prepared_data, 
								  file_path=Helpers.get_file_path_for_user(user=user, 
								  										   sufix=config.account_data_name), 
								  headers=config.account_data_headers, 
								  mode=config.write_mode,
								  single=True)

	def save_account_data_for_all_users(self):
		account_data = []
		for root, dirs, files in os.walk(config.output_folder):
			for file in files:
				if not (file.startswith('.')):
					folder_name = file.split(config.account_data_name, 1)[0][:-1]
					file_name = config.output_folder + "/" + folder_name + "/" + file
					if os.path.isfile(file_name):
						with open(file_name, config.read_or_write_mode) as f:
							reader = csv.reader(f)
							for index, item in enumerate(reader):
								if index == 1:
									account_data.append(item)
		self.save_account_data_to_file(file_path=config.account_data_file,
									   data=account_data)

	def save_account_data_to_file(self, file_path, data):
		print "Saving " + str(len(data)) + " entries to " + file_path
		Helpers.save_data_to_file(data=data,
								  file_path=file_path,
								  headers=config.account_data_headers,
								  mode=config.write_mode,
								  single=False)

if __name__ == '__main__':
	Main().main_loop()