"""Script untuk generate command dan memanggil `snscrape` yang digunakan untuk scraping suatu topik
   di twitter"""

import csv
import json
import logging
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Any, Dict, List, Optional, Sequence, Tuple

from rich.live import Live
from rich.logging import RichHandler
from rich.table import Table
from src.utils import datetime_validator, get_name, kill_proc_tree

# Setup logging
logging.basicConfig(format="%(message)s", level=logging.INFO, handlers=[RichHandler()])
log = logging.getLogger("rich")

# main directory
main_dir = Path(__file__).parents[1]


class TwitterScraper:
    """Scrapping twitter berdasarkan query yang diberikan.

    Args:
        query (str): Search query.
        lang (str): Language. Defaults to "id".
        geocode (Optional[str]): Geocode [lat,long,r]. Defaults to None.
        since (Optional[str]): Since [string isoformated datetime]. Defaults to None.
        until (Optional[str]): Until [string isoformated datetime]. Defaults to None.

    Examples:
        Scraping spesifik topik
        >>> scraper = TwitterScraper(query="minyak")
        >>> scraper.scrape()
        [ INFO ] Scraping...
        1 - 2022-08-01T16:39:41+00:00 - @gerundghast im broke. harga minyak no joke rn
        2 - 2022-08-01T16:39:17+00:00 - @beaulitude Minyak mahal jadi gimana kalo direbus? https://t.co/MnmgY4iNPs
        3 - 2022-08-01T16:39:13+00:00 - @Damsllette ak blm nemu enakny dmna 😭😭 biasa pke minyak angin doang
        ...
    """

    scraper = "snscrape"
    scraper_type = "twitter-search"

    def __init__(
        self,
        query: str,
        lang: str = "id",
        geocode: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> None:
        self.query = query
        self.lang = lang
        self.geocode = geocode
        if since:
            datetime_validator(since)
        self.since = since
        if until:
            datetime_validator(until)
        self.until = until

    def _get_command(self) -> str:
        """Mengenerate command yang akan diberikan pada `snscrape`

        Returns:
            str: command
        """
        global_options = ["--jsonl"]
        if self.since:
            global_options.append(f"--since {self.since}")
        new_global_options = " ".join(global_options)

        scrapper_options = [
            self.query,
            f"lang:{self.lang}",
            "exclude:nativeretweets",
            "exclude:retweets",
        ]
        if self.geocode:
            scrapper_options.append(f"geocode:{self.geocode}")
        if self.until:
            scrapper_options.append(f"until:{self.until}")
        new_scrapper_options = " ".join(scrapper_options)

        return f'{self.scraper} {new_global_options} {self.scraper_type} "{new_scrapper_options}"'

    def _flatten(
        self, nested_d: Dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> Dict[str, Any]:
        """Flatten nested dictionary

        Args:
            nested_d (Dict[str, Any]): Nested dictionary to flatten.
            parent_key (str, optional): Parrent key. Defaults to "".
            sep (str, optional): Nestted dictionary sepparator. Defaults to ".".

        Returns:
            Dict[str, Any]: Flatten dictionary.
        """
        items = []  # type: List[Tuple[str, Any]]
        for k, v in nested_d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, Dict):
                items.extend(self._flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _denied_users_handler(self, denied_users: str) -> Sequence[str]:
        """Handle denied users."""
        assert Path(denied_users).exists(), "File not exist!!"
        with open(denied_users) as reader:
            users = json.load(reader)  # type: Sequence[str]
        return users

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
            "tweets": "rawContent",
            "username": "user.username",
            "retweet": "retweetCount",
            "source": "sourceLabel",
            "hashtags": "hashtags",
            "url": "url",
            **add_features,
        }
        if denied_users is not None:
            denied_users = self._denied_users_handler(denied_users)  # type: ignore

        if export is not None:
            log.info(f"Exporting to 'output' directory")
            path = main_dir / "output"
            path.mkdir(exist_ok=True)
            filename = get_name((path / f"scrape-{export}.csv").as_posix())
            f = open(filename, "w", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(list(filters.keys()))

        log.info("Scraping...")
        snscrape = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        assert snscrape.stdout is not None, "None stdout"

        try:
            table = Table()
            table.add_column("No")
            table.add_column("Date")
            table.add_column("Username")
            table.add_column("Content")

            with Live(None, refresh_per_second=1, vertical_overflow="visible") as live:
                index = 1
                for out in snscrape.stdout:
                    temp = self._flatten(json.loads(out))

                    if denied_users is not None:  # filter username
                        if temp["user.username"] in denied_users:  # pragma: no cover
                            continue

                    if verbose:  # logging output
                        table.add_row(
                            f"{index}", temp["date"], temp["user.username"], temp["rawContent"]
                        )
                        live.update(table)

                    if export:  # write row
                        row = [temp[x] for x in filters.values()]
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
            log.info("Received exit from user, exiting...")
            kill_proc_tree(snscrape.pid)

        if export:
            log.info(f"Successfully Exported to {filename}")
            f.close()

        log.info("Done!")
