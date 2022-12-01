from pathlib import Path

import numpy as np
from src.model import Model

main_dir = Path(__file__).parents[1]


def test_predict():
    model = Model((main_dir / "models" / "[TRAINED] Pipelined TF-IDF - SVM.onnx").as_posix())

    assert model.predict("test")
    assert model.predict(["test"])
    assert model.predict(np.asarray(["test"]))
    assert model.predict(np.asarray([["test"]]))
    label, probs = model.predict(np.asarray(["test", "test 2"]))
    assert label.shape == (2,) and probs.shape == (2, 3)
