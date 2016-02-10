import ConfigParser
import os

homeDir = os.path.expanduser("~")
credentialsConfig = ConfigParser.ConfigParser()
credentialsConfig.read(homeDir + '/.aws/credentials')

config = ConfigParser.ConfigParser()
config.read(homeDir + '/.aws/config')

# Configuration class
class Configuration:
	def regionName(self, profileName):
		profile = self.profileNameForConfig(profileName)
		return config.get(profile, 'region')

	def accessKey(self, profileName):
		return credentialsConfig.get(profileName, 'aws_access_key_id')

	def secretAccessKey(self, profileName):
		return credentialsConfig.get(profileName, 'aws_secret_access_key')

	def profileNameForConfig(self, profileName):
		if profileName == 'default':
			return profileName

		return 'profile ' + profileName

	