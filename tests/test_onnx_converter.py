import shutil
from pathlib import Path

from src.model import Model
from src.onnx_converter import onnx_model_converter

main_dir = Path(__file__).parents[1]


def test_converter():
    output_dir = main_dir / "output"
    output_dir.mkdir(exist_ok=True)

    model_path = main_dir / "models" / "[TRAINED] Pipelined TF-IDF - SVM.pickle"

    # test onnx model without zipmap
    converted_model_path = Path(
        onnx_model_converter(model_path.as_posix(), output_dir.as_posix(), ort=True)
    )
    converted_model = Model(converted_model_path.as_posix())
    label, probabilites = converted_model.session.run(None, {"words": [["test"]]})
    assert label.shape == (1,) and probabilites.shape == (1, 3)  # check model without zipmap output
    ort_model_dir = converted_model_path.parent / f"{converted_model_path.stem}-ort"
    assert ort_model_dir.exists()
    converted_model_path.unlink(missing_ok=True)
    shutil.rmtree(ort_model_dir)

    # test onnx model with zipmap
    converted_model_path = Path(
        onnx_model_converter(model_path.as_posix(), output_dir.as_posix(), zipmap=True)
    )
    converted_model = Model(converted_model_path.as_posix())
    label, probabilites = converted_model.session.run(None, {"words": [["test"]]})
    assert (
        label.shape == (1,) and len(probabilites) == 1 and len(probabilites[0].items()) == 3
    )  # check zipmap output
    converted_model_path.unlink(missing_ok=True)
