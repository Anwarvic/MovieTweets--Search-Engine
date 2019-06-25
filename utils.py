import time
import yaml



def get_todays_date():
	"""
	This is a simple function to return the date of the day
	when this function runs. For example 29/5/2019 will be 20190529
	It's used when POSTing to wit API
	"""
	obj = time.gmtime(time.time())
	year = str(obj.tm_year).zfill(4)
	month = str(obj.tm_mon).zfill(2)
	day = str(obj.tm_mday).zfill(2)
	return "{}-{}-{}".format(year, month, day)



def parse_yaml(filepath="conf.yaml"):
	"""
	This method parses the YAML configuration file and returns the parsed info
	as python dictionary.
	Args:
		filepath (string): relative path of the YAML configuration file
	Returns:
		the parsed YAML object as a dictionary
	"""
	with open(filepath, 'r') as fin:
		try:
			conf_dictionary = yaml.safe_load(fin)
			return conf_dictionary
		except Exception as exc:
			print("ERROR while parsing YAML conf.")
			print(exc)
