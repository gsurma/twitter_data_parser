import config
import csv
import os.path
import time

class Helpers:	

	@staticmethod
	def save_data_to_file(data, file_path, headers, mode, single):
		with open(file_path, mode) as file:
			writer = csv.writer(file)
			if os.path.getsize(file_path) == 0 or mode == config.write_mode:
				writer.writerow(headers)
			if single:
				writer.writerow(data)
			else:
				writer.writerows(data)

	@staticmethod
	def get_file_path_for_user(user, sufix):
		directory = config.output_folder + "/" + user.rstrip() + "/"
		if not os.path.exists(directory):
			os.makedirs(directory)
		return directory + user.rstrip() + "_" + sufix + ".csv"

	@staticmethod
	def get_list_of_users(file_path):
		with open(file_path, config.read_mode) as file:
			list_of_users = []
			for user in file:
				list_of_users.append(user)
		return list_of_users

	@staticmethod
	def get_data_for_user_and_sleep_if_necessary(request_counter, request_limit, method):
		if request_counter < request_limit:
			request_counter += method
			return request_counter
		else:
			print "Request quota reached - sleeping for " + str(required_sleep_time/60) + " minutes"
			time.sleep(required_sleep_time)
			return 0