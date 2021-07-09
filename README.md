<h3 align="center">
  <img src="assets/twitter_data_parser_icon_web.png" width="300">
</h3>

# Twitter Data Parser

## About
Python (Tweepy based) scripts that allow downloading metadata and tweets for given users.

## How to use it

1. Configure API Keys in `config.py`
2. Prepare a list of usernames in `users.txt`
3. Adjust additional params in `config.py`

### Account Data
1. `python twitter_account_data_parser.py`
2. For each user there will be created a folder named `{user}` with with `{user}_account_data.csv` file inside it.
3. Additionally there will be created a single `account_data.csv` file combining all entries in output folder. Its very useful for further data analysis.

### Tweets
1. `python twitter_tweets_parser.py`
2. For each user there will be created a folder named `{user}` with with `{user}_tweets.csv` file inside it.
3. Script skips already downloaded tweets

## Author

**Greg (Grzegorz) Surma**

[**PORTFOLIO**](https://gsurma.github.io)

[**GITHUB**](https://github.com/gsurma)

[**BLOG**](https://medium.com/@gsurma)

