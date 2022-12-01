from pathlib import Path

import pandas as pd
from src.model_tester import ModelScraper

main_dir = Path(__file__).parents[1]


def test_ModelScraper():
    output_dir = main_dir / "output"
    model_path = main_dir / "models" / "[TRAINED] Pipelined TF-IDF - SVM.onnx"

    # test max_result
    ModelScraper(model_path.relative_to(main_dir).as_posix()).scrape(export="covid", max_result=10)
    filename = output_dir / "scrape-covid.csv"
    dataset = pd.read_csv(filename.as_posix())
    assert len(dataset) == 10
    filename.unlink(missing_ok=True)
