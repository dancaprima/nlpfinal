import sys

sentimentData = 'sentiwords_id.txt'
twitterData = 'test_labeling.txt'

def tweet_dict(twitterData):
    twitter_list_dict = []
    with open(twitterData) as infile:
        for line in infile:
            twitter_list_dict.append(line)
    return twitter_list_dict
   
    
def sentiment_dict(sentimentData):
    afinnfile = open(sentimentData)
    scores = {}
    for line in afinnfile:
        term, score = line.split(":")
        scores[term] = float(score) 

    return scores 
    
def main():
    
    
    tweets = tweet_dict(twitterData)
    sentiment = sentiment_dict(sentimentData)
    for index in range(len(tweets)):
        tweet_word = tweets[index].split()
        sent_score = 0
        for word in tweet_word:
            word = word.rstrip('?:!.,;"!@')
            word = word.replace("\n", "")
            
            if word in sentiment.keys():
                sent_score = sent_score + float(sentiment[word])
                    
            else:
                sent_score = sent_score
        if float(sent_score) > 0:
            if float(sent_score) > 0.7:
                 print tweets[index].replace("\n", ""), 'Sentimen sangat positif', sent_score, "\n"
            else:
                 print tweets[index].replace("\n", ""), 'Sentimen positif', sent_score, "\n"
             
             
        if float(sent_score) < 0:
            if float(sent_score) < -0.7:
                 print tweets[index].replace("\n", ""), 'Sentimen sangat negatif', sent_score, "\n"
            else:
                 print tweets[index].replace("\n", ""), 'Sentimen negatif', sent_score, "\n"


        if float(sent_score) == 0:
            print tweets[index].replace("\n", ""), 'sentiment netral', sent_score, "\n"
   
if __name__ == '__main__':
    main()
