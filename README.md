# arxiv-twitter-thread-bot

[Inspired By](https://x.com/BasedBeffJezos/status/1773185683982528893?s=20)

## Instructions to run

Clone the repository and install dependencies:
```
pip install -r requirements.txt
```

Add your `openai` and `typefully` keys to .env:
```
OPENAI_API_KEY=
TYPEFULLY_API_KEY=
```

Open python terminal
```
python

> from pdf_to_tweet_thread import *
> response, img_path = twitter_thread_summary("https://arxiv.org/pdf/2403.18802.pdf")

... 

Saved first page to imgs/2305.09656.png
Link: https://typefully.com/t/{link}

```
