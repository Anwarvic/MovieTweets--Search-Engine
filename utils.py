
import yaml



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
