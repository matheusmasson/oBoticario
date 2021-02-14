import tweepy
import mysql.connector

chave_consumidor = 'ezuZQsNgAdAcQdVTt6zgtiruR'
segredo_consumidor = 'EX5qtCjrtRdMRH0UidNqaq9f2JN8i1izH4IRq0A6STeemgk4tj'
token_acesso = 'AAAAAAAAAAAAAAAAAAAAAD0cMwEAAAAAWmg0cRF1TcG%2Fr9pBjJq6hI5%2Fx%2FM%3D2z3u5NJ6HWIlulwwH4GD9pkPS3MKwRnoei5TBFXtcK2ZhNJBeQ'

autenticacao = tweepy.OAuthHandler(chave_consumidor, segredo_consumidor)
redirect_url = autenticacao.get_authorization_url()
api = tweepy.API(autenticacao)


language = 'pt-BR'
result_type = 'recent'
since_date = "2019-01-01"
until_date = "2019-12-31"
max_tweets = 50
location = 'Brazil'
top_tweets = True

api = tweepy.API(autenticacao)
resultados = api.search(q='Boticário')

#for tweet in resultados:
#     print(f'Usuário: {tweet.user} - Tweet: {tweet.text}')

database = mysql.connector.connect(host="localhost", user = "root", passwd = "senhamysql@M", db = "boticario")




def scraptweets(search_words, date_since, last_date, numTweets, numRuns):

    tweets = tweepy.Cursor(api.search, q=search_words,since=date_since, lang="pt").items(numTweets)

    tweet_list = [tweet for tweet in tweets]

    for tweet in tweet_list:
        text = tweet.text
        user = tweet.user.screen_name
        print(user + "- "+text)

        values = (user, text)

        cursor = database.cursor()

        query = """INSERT INTO boticario.tweeter (user, text) VALUES (%s, %s)"""

        # Execute sql Query
        cursor.execute(query, values)

        cursor.close()

    # Commit the transaction
    database.commit()

search_words = "Boticario OR SOLAR"

scraptweets(search_words,date_since=since_date, last_date=until_date, numTweets=50,numRuns=6)

