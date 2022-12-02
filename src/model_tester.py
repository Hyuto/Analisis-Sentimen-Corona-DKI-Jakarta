import csv
import json
import logging
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Dict, Optional

from src.model import Model
from src.preprocessing import preprocessing
from src.scraper import TwitterScraper
from src.utils import get_name, kill_proc_tree

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)

# main directory
main_dir = Path(__file__).parents[1]


class ModelScraper(TwitterScraper):
    """Model scrapper.

    Args:
        model (str): Model path.
        query (str): Search query. Defaults to "#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine".
        lang (str): Language. Defaults to "id".
        geocode (Optional[str]): Geocode [lat,long,r]. Defaults to "-6.213621,106.832673,20km" which is Jakarta geocode.
        since (Optional[str]): Since [string isoformated datetime]. Defaults to None.
        until (Optional[str]): Until [string isoformated datetime]. Defaults to None.
    """

    def __init__(
        self,
        model: str,
        query: str = "#corona OR covid OR Covid19 OR #DiRumahAja OR #quarantine OR Corona OR DiRumahAja OR wabah OR pandemi OR quarantine",
        lang: str = "id",
        geocode: Optional[str] = "-6.213621,106.832673,20km",  # jakarta geocode
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> None:
        super().__init__(query, lang, geocode, since, until)
        self.model = Model(model)
        self.labels = ["negative", "neutral", "positive"]

    def scrape(
        self,
        add_features: Dict[str, str] = {},
        denied_users: Optional[str] = None,
        max_result: Optional[int] = None,
        export: Optional[str] = None,
        verbose: bool = True,
    ) -> None:
        """Running scraping dengan `snscrape`

        Args:
            add_features (Dict[str, str]): Menambahkan filter kolom yang akan diexport.
                Defaults to {}.
            denied_users (Optional[str]): List user yang tweetnya dapat dihiraukan, berupa
                pathlike string ke file tempat list user disimpan (json format). Defaults to None.
            max_result (Optional[int]): Jumlah maksimal tweet yang di scrape. Defaults to None.
            export (Optional[str]): Nama file tempat table diexport pada direktori `output`.
                Jika `None` maka table hasil scraping tidak akan diexport. Defaults to None.
            verbose (bool): Tampilkan tweet yang di scrape di terminal. Defaults to True.
        """
        command = self._get_command()
        filters = {
            "tanggal": "date",
            "tweets": "content",
            "username": "user.username",
            "retweet": "retweetCount",
            "source": "sourceLabel",
            "hashtags": "hashtags",
            "url": "url",
            **add_features,
        }
        if denied_users is not None:  # pragma: no cover
            denied_users = self._denied_users_handler(denied_users)  # type: ignore

        if export is not None:
            logging.info(f"Exporting to 'output' directory")
            path = main_dir / "output"
            path.mkdir(exist_ok=True)
            filename = get_name((path / f"scrape-{export}.csv").as_posix())
            f = open(filename, "w", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(list(filters.keys()) + ["sentiment"])

        logging.info("Scraping...")
        snscrape = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        assert snscrape.stdout is not None, "None stdout"

        try:
            index = 1
            for out in snscrape.stdout:
                temp = self._flatten(json.loads(out))

                if denied_users is not None:  # filter username
                    if temp["user.username"] in denied_users:  # pragma: no cover
                        continue

                class_pred, _ = self.model.predict(preprocessing(temp["content"]))

                if verbose:  # logging output
                    content = repr(
                        f"{temp['content'][:67]}..."
                        if len(temp["content"]) > 69
                        else temp["content"]
                    )
                    print(
                        f"{index} - {temp['date']} - {temp['user.username']} - "
                        + f"{content} - {self.labels[class_pred[0]]}"
                    )

                if export:  # write row
                    row = [temp[x] for x in filters.values()] + [self.labels[class_pred[0]]]
                    writer.writerow(row)

                if max_result:  # brake and kill subprocess
                    if index >= max_result:
                        kill_proc_tree(snscrape.pid)
                        break
                index += 1
        except KeyError as e:  # pragma: no cover
            kill_proc_tree(snscrape.pid)
            raise e
        except KeyboardInterrupt:  # pragma: no cover
            logging.info("Received exit from user, exiting...")
            kill_proc_tree(snscrape.pid)

        if export:
            logging.info(f"Successfully Exported to {filename}")
            f.close()

        logging.info("Done!")
