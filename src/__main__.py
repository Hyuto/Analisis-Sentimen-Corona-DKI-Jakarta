import logging
import re
import shutil
from pathlib import Path
from typing import List, Optional
from xml.dom import NotFoundErr

import typer

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)

# Setup typer
main = typer.Typer(add_completion=False)

# main directory
main_dir = Path(__file__).parents[1]


@main.command("scrape", help="Scrapping twitter berdasarkan query yang diberikan")
def scrape(
    query: str = typer.Argument(..., help="Query pencarian tweet"),
    lang: str = typer.Option("id", help="Bahasa"),
    max_results: Optional[int] = typer.Option(None, help="Banyak tweet maksimal yang discrape"),
    since: Optional[str] = typer.Option(
        None, help="Since (batasan awal tanggal tweet) [isoformated date string]"
    ),
    until: Optional[str] = typer.Option(
        None, help="Until (batasan akhir tanggal tweet) [isoformated date string]"
    ),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    add_features: Optional[str] = typer.Option(
        None, help='Menambahkan feature yang akan diexport dalam file csv [string separated by ","]'
    ),
    denied_users: Optional[str] = typer.Option(
        None,
        help=(
            "List user yang tweetnya diabaikan [pathlike string ke file list user (json formated)]"
        ),
    ),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    add_features = add_features.split(",") if add_features else []  # type: ignore
    if denied_users:
        if not Path(denied_users).exists():
            raise NotFoundErr("Denied users file is not found!")

    logging.info("Starting scrape commands with args:")
    args = locals()
    for k, v in args.items():
        print(f"  * {k} : {v}")

    from src.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, since, until)
    scraper.scrape(
        export=export,
        add_features=add_features,  # type: ignore
        denied_users=denied_users,
        max_result=max_results,
        verbose=verbose,
    )


@main.command("model-test", help="Testing model dengan tweet baru")
def model_test(
    query: str = typer.Argument("vaksin (corona OR covid)", help="Query pencarian tweet"),
    model: str = typer.Argument(
        (main_dir / "models" / "model.onnx").relative_to(main_dir).as_posix(),
        help="Path model yang digunakan",
    ),
    lang: str = typer.Option("id", help="Bahasa"),
    max_results: Optional[int] = typer.Option(None, help="Banyak tweet maksimal yang discrape"),
    since: Optional[str] = typer.Option(
        None, help="Since (batasan awal tanggal tweet) [isoformated date string]"
    ),
    until: Optional[str] = typer.Option(
        None, help="Until (batasan akhir tanggal tweet) [isoformated date string]"
    ),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    add_features: Optional[str] = typer.Option(
        None, help='Menambahkan feature yang akan diexport dalam file csv [string separated by ","]'
    ),
    denied_users: Optional[str] = typer.Option(
        (main_dir / "data" / "denied-users.json").relative_to(main_dir).as_posix(),
        help=(
            "List user yang tweetnya diabaikan [pathlike string ke file list user (json formated)]"
        ),
    ),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    add_features = add_features.split(",") if add_features else []  # type: ignore
    if denied_users:
        if not Path(denied_users).exists():
            raise NotFoundErr("Denied users file is not found!")

    logging.info("Starting scrape commands with args:")
    args = locals()
    for k, v in args.items():
        print(f"  * {k} : {v}")

    from src.model_tester import ModelScraper

    scraper = ModelScraper(model, query, lang, since, until)
    scraper.scrape(
        export=export,
        add_features=add_features,  # type: ignore
        denied_users=denied_users,
        max_result=max_results,
        verbose=verbose,
    )


@main.command("clean", help="Membersihkan project main directory")
def clean_up(
    clear: bool = typer.Option(False, help="Menghapus semua folder cache"),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    cache_dir = [".mypy_cache", ".pytest_cache", "./**/__pycache__"]
    additional_dir = ["output", "./**/output", "notebook/.ipynb_checkpoints"]
    cache_file = [".coverage"]
    additional_file: List[str] = []
    exclude_dir = ["\.venv", "app"]

    def delete(iterator: List[str], exclude: str = rf"({'|'.join(exclude_dir)})\/") -> None:
        # loop through
        for x in iterator:
            for path in main_dir.glob(x):
                to_delete = path.relative_to(main_dir).as_posix()
                if re.search(exclude, to_delete):
                    continue
                try:
                    if verbose:
                        logging.info(f"Deleting : {to_delete}")
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                except:
                    logging.error(f"Error on deleting : {path}")

    directory = cache_dir + additional_dir if clear else cache_dir
    delete(iterator=directory)
    files = cache_file + additional_file if clear else cache_file
    delete(iterator=files)

    logging.info("Done!")


main()
