class Tweet:
	def __init__(self, text, time, lat, lon):
		self.text = text
		self.time = TimeObj(time)
		self.loc = Location(lat, lon)

		numTweets += 1

	welcomeMsg = "Hello"
	numTweets = 0

	def getText(self):
		return self.text

	def getLoc(self):
		return self.loc