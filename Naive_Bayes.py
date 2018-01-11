
import string

def extract_words(tweet_words):
	words = []
	alpha_lower = string.ascii_lowercase
	alpha_upper = string.ascii_uppercase
	numbers = [str(n) for n in range(10)]
	for word in tweet_words:
		cur_word = ''
		for c in word:
			if (c not in alpha_lower) and (c not in alpha_upper) and (c not in numbers):
				if len(cur_word) >= 2:
					words.append(cur_word.lower())
				cur_word = ''
				continue
			cur_word += c
		if len(cur_word) >= 2:
			words.append(cur_word.lower())
	return words

def get_training_data():
	f = open('training.txt', 'r')
	training_data = []
	for l in f.readlines():
		l = l.strip()
		tweet_details = l.split()
		tweet_id = tweet_details[0]
		tweet_label = tweet_details[1]
		tweet_words = extract_words(tweet_details[2:])
		training_data.append([tweet_id, tweet_label, tweet_words])
	
	f.close()
	
	return training_data

def get_test_data():
	f = open('detik.txt', 'r')
	validation_data = []
	for l in f.readlines():
		l = l.strip()
		tweet_details = l.split(' ')
		tweet_id = tweet_details[0]
		tweet_words = extract_words(tweet_details[1:])
		validation_data.append([tweet_id, '', tweet_words])

	f.close()

	return validation_data


def get_words(training_data):
	words = []
	for data in training_data:
		words.extend(data[2])
	return list(set(words))

def get_word_prob(training_data, label = None):
	words = get_words(training_data)
	freq = {}

	for word in words:
		freq[word] = 1

	total_count = 0
	for data in training_data:
		if data[1] == label or label == None:
			total_count += len(data[2])
			for word in data[2]:
				freq[word] += 1

	prob = {}
	for word in freq.keys():
		prob[word] = freq[word]*1.0/total_count

	return prob

def get_label_count(training_data, label):
	count = 0
	total_count = 0
	for data in training_data:
		total_count += 1
		if data[1] == label:
			count += 1
	return count*1.0/total_count

def label_data(test_data, sports_word_prob, politics_word_prob, entertainment_word_prob, sports_prob, politics_prob, entertainment_prob):
	labels = []
	for data in test_data:
		data_prob_sports = sports_prob
		data_prob_politics = politics_prob
		data_prob_entertainment = entertainment_prob
		
		for word in data[2]:
			if word in sports_word_prob:
				data_prob_sports *= sports_word_prob[word]
				data_prob_politics *= politics_word_prob[word]
				data_prob_entertainment *= entertainment_word_prob[word]
			else:
				continue

		if data_prob_sports >= data_prob_politics:
			labels.append([' '.join(data[2]), '>>>Sports', data_prob_sports, data_prob_politics, data_prob_entertainment])
		elif data_prob_politics >= data_prob_entertainment:
			labels.append([' '.join(data[2]), '>>>Politics', data_prob_sports, data_prob_politics, data_prob_entertainment])
		else:
			labels.append([' '.join(data[2]), '>>>Entertainment', data_prob_sports, data_prob_politics, data_prob_entertainment])
	return labels

def print_labelled_data(labels):
	f_out = open('test_labeling2.txt', 'w')
	for [tweet_id, label, prob_sports, prob_politics, prob_entertainment] in labels:
		f_out.write('%s %s\n' % (tweet_id, label))
	f_out.close()


training_data = get_training_data()
test_data = get_test_data()

word_prob = get_word_prob(training_data)
sports_word_prob = get_word_prob(training_data, 'Sports')
politics_word_prob = get_word_prob(training_data, 'Politics')
entertainment_word_prob = get_word_prob(training_data, 'Entertainment')

sports_prob = get_label_count(training_data, 'Sports')
politics_prob = get_label_count(training_data, 'Politics')
entertainment_prob = get_label_count(training_data, 'Entertainment')

for (word, prob) in word_prob.iteritems():
	sports_word_prob[word] /= prob
	politics_word_prob[word] /= prob
	entertainment_word_prob[word] /= prob

test_labels = label_data(test_data, sports_word_prob, politics_word_prob, entertainment_word_prob, sports_prob, politics_prob, entertainment_prob)
print_labelled_data(test_labels)
