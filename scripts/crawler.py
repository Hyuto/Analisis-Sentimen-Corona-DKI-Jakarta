import argparse
import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

import pandas as pd
import tweepy
from utils import CONFIG, get_name

main_dir = os.path.dirname(os.path.dirname(__file__))


class TweetCrawler:
    def __init__(self, name: str, output_dir: str = os.path.join(main_dir, "output")):
        self.name = name
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.authenticated = False

    @staticmethod
    def _logger(count: int, tweet: tweepy.models.SearchResults, **kwargs) -> None:
        text = tweet.full_text
        if len(text) > 65:
            text = text[:65] + "..."
        template = f"{count}. {tweet.created_at} - {repr(text)}"
        print(template)
        if kwargs:
            for k, v in kwargs.items():
                template_kwargs = " " * (len(str(count)) + 2) + f"{k} : {v}"
                print(template_kwargs[: len(template)])

    def _export(
        self,
        tweetan: List[Dict[str, Any]],
        data: Dict[str, List[Any]],
        export_json: bool,
    ) -> None:
        filename_csv = f"crawl-{self.name}.csv"
        path_csv = get_name(os.path.join(self.output_dir, filename_csv))
        dataset = pd.DataFrame(data)
        dataset.to_csv(path_csv, index=False)

        if export_json:
            filename_json = f"crawl-{self.name}.json"
            path_csv = get_name(os.path.join(self.output_dir, filename_json))
            with open(path_csv, "w") as writer:
                writer.write(json.dumps(tweetan))

    def setup_auth_api(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> None:
        if not self.authenticated:
            self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self._auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self._auth, wait_on_rate_limit=True)
            self.authenticated = True
            print("Authenticated !")

    def run(
        self,
        query: str,
        geocode: Optional[str] = None,
        max_tweets: Optional[int] = None,
        export_json: bool = False,
        spliter: int = 20000,
        callbacks: List[Tuple[str, Callable[[Any], Any]]] = [],
    ) -> None:
        assert self.authenticated, "Tolong setup auth terlebih dahulu! Cek setup_auth_api method."

        tweetan = []
        data: Dict[str, List[Any]] = {
            "Tanggal": [],
            "Tweets": [],
            "ID": [],
            "Screen Name": [],
            "Banyak Retweet": [],
            "Source": [],
            "Retweet Status": [],
            "Hashtags": [],
            **{x[0]: [] for x in callbacks},
        }

        # Crawl using tweepy
        for tweet in tweepy.Cursor(
            self.api.search_tweets,
            q=query,  # query crawling
            geocode=geocode,  # geocode
            tweet_mode="extended",  # full_text support
            count=200,
            lang="id",
        ).items(max_tweets):
            tweetan.append(tweet._json)
            data["Tanggal"].append(tweet.created_at)
            data["Tweets"].append(tweet.full_text)
            data["ID"].append(tweet.id)
            data["Screen Name"].append(tweet.user.screen_name)
            data["Source"].append(tweet.source)
            data["Banyak Retweet"].append(tweet.retweet_count)
            data["Hashtags"].append(
                "\t".join(sorted([x["text"] for x in tweet.entities["hashtags"]]))
            )
            if "RT" in tweet.full_text:
                data["Retweet Status"].append(1)
            else:
                data["Retweet Status"].append(0)

            if callbacks:
                for callback in callbacks:
                    data[callback[0]].append(callback[1](tweet))

            self._logger(len(tweetan), tweet, **{x[0]: data[x[0]][-1] for x in callbacks})
            if len(tweetan) >= spliter:
                self._export(tweetan[:spliter], {x: data[x][:spliter] for x in data}, export_json)
                tweetan, data = tweetan[spliter:], {x: data[x][spliter:] for x in data}

        if len(tweetan) >= 0:
            self._export(tweetan, data, export_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script untuk melakukan crawling tweet terbaru mengenai corona"
    )
    parser.add_argument("-n", "--name", help="Dataset name", type=str, required=True)
    parser.add_argument(
        "-m", "--max-tweets", help="Jumlah maximal tweet yang akan di crawl", type=int
    )
    parser.add_argument(
        "-ejs", "--export-json", help="Export twitter json yang telah di crawl", action="store_true"
    )
    parser.add_argument(
        "-s",
        "--splitter",
        help="Splitting data dengan menspesifikan jumlah maximal tweet per-file",
        type=int,
        default=20000,
    )
    args = parser.parse_args()

    crawler = TweetCrawler(args.name)
    crawler.setup_auth_api(**CONFIG["TWITTER-API"])
    crawler.run(
        **CONFIG["SEARCH-PLAN"],
        max_tweets=args.max_tweets,
        export_json=args.export_json,
        spliter=args.splitter,
    )
