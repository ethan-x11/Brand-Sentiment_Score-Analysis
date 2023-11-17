from transformers import pipeline

def sentiment_analysis(textlist):
    sanalysis = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    return sanalysis(textlist)


if __name__ == '__main__':
    l = ['I love sentiment analysis!', 'I hate sentiment analysis!','Really Good']
    print(sentiment_analysis(l))