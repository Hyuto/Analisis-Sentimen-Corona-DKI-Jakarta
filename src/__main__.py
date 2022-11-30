import ast
import logging
import re
import shutil
from pathlib import Path
from typing import List, Optional

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
    geocode: Optional[str] = typer.Option(
        "-6.213621,106.832673,20km", help="Geocode daerah yang akan di scrape."
    ),
    since: Optional[str] = typer.Option(
        None, help="Since (batasan awal tanggal tweet) [isoformated date string]"
    ),
    until: Optional[str] = typer.Option(
        None, help="Until (batasan akhir tanggal tweet) [isoformated date string]"
    ),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    add_features: Optional[str] = typer.Option(
        None, help="Menambahkan feature yang akan diexport dalam file csv [json formated string]"
    ),
    denied_users: Optional[str] = typer.Option(
        None,
        help=(
            "List user yang tweetnya diabaikan [pathlike string ke file list user (json formated)]"
        ),
    ),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    add_features = ast.literal_eval(add_features) if add_features else {}
    if denied_users:
        if not Path(denied_users).exists():
            raise FileNotFoundError("Denied users file is not found!")

    logging.info("Starting scrape commands with args:")
    args = locals()
    for k, v in args.items():
        print(f"  * {k} : {v}")

    from src.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, geocode, since, until)
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
            raise FileNotFoundError("Denied users file is not found!")

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


@main.command(
    "convert-onnx", help="Mengconvert model yang telah dilatih dalam bentuk pickle ke onnx model"
)
def convert_onnx(
    path: str = typer.Argument(..., help="Path ke model yang akan di convert (pickle formated)"),
    ort: bool = typer.Option(False, help="Convert ke tipe ort"),
) -> None:
    model_path = Path(path)
    if not model_path.exists():
        raise FileNotFoundError("Model file is not found!")

    output_dir = main_dir / "output"
    output_dir.mkdir(exist_ok=True)

    import pickle
    import subprocess
    import sys

    from onnx.checker import check_model
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import StringTensorType
    from src.utils import get_name

    model = pickle.load(open(model_path, "rb"))

    logging.info(f"Converting model : {model_path.as_posix()}")
    onnx_model = convert_sklearn(
        model,
        initial_types=[("words", StringTensorType([None, 1]))],
        options={"svm": {"zipmap": False}},
    )
    logging.info(f"Checking onnx model...")
    check_model(onnx_model)

    filename = get_name((output_dir / "Exported model.onnx").relative_to(main_dir).as_posix())
    logging.info(f"Exporting onnx model to : {filename}")
    with open(filename, "wb") as writer:
        writer.write(onnx_model.SerializeToString())

    if ort:
        logging.info("Optimizing onnx model to ort...")
        subprocess.run(
            f'{sys.executable} -m onnxruntime.tools.convert_onnx_models_to_ort "{(main_dir / filename).absolute()}"',
            shell=True,
        )

    logging.info("Done!")


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
