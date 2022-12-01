import json
from pathlib import Path

import pandas as pd
from src.scraper import TwitterScraper

main_dir = Path(__file__).parents[1]


def test_TwitterScraper():
    output_dir = main_dir / "output"

    denied_users_test = output_dir / "test-denied-users.json"
    with (open(denied_users_test, "w")) as w:
        w.write(json.dumps(["kompascom", "detikHealth", "detikcom", "kumparan"]))

    # test max_result
    TwitterScraper("minyak").scrape(
        export="minyak",
        max_result=10,
        denied_users=denied_users_test.as_posix(),
    )
    filename = output_dir / "scrape-minyak.csv"
    dataset = pd.read_csv(filename.as_posix())
    assert len(dataset) == 10
    filename.unlink(missing_ok=True)
    denied_users_test.unlink(missing_ok=True)

    # test since and until
    since, until = "2022-07-18", "2022-07-19"
    TwitterScraper("ayam bakar", since=since, until=until).scrape(export="ayam", verbose=False)
    filename = output_dir / "scrape-ayam.csv"
    dataset = pd.read_csv(filename.as_posix())
    dataset["tanggal"] = pd.to_datetime(dataset["tanggal"])
    assert (dataset["tanggal"] >= since).all() and (dataset["tanggal"] < until).all()
    filename.unlink(missing_ok=True)
