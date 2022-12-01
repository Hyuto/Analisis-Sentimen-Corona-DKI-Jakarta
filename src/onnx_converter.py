import logging
import os
import pickle
import subprocess
import sys

from onnx.checker import check_model
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
from src.utils import get_name

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


def onnx_model_converter(
    model_path: str, output_dir: str, zipmap: bool = False, ort: bool = False
) -> str:
    model = pickle.load(open(model_path, "rb"))

    logging.info(f"Converting model : {model_path}")
    onnx_model = convert_sklearn(
        model,
        initial_types=[("words", StringTensorType([None, 1]))],
        options=dict(
            [
                (name, {"zipmap": zipmap})
                for name, est in model.named_steps.items()
                if est == model._final_estimator
            ]
        ),
    )
    logging.info(f"Checking onnx model...")
    check_model(onnx_model)

    filename = get_name(os.path.join(output_dir, "Exported model.onnx"))
    logging.info(f"Exporting onnx model to : {filename}")
    with open(filename, "wb") as writer:
        writer.write(onnx_model.SerializeToString())

    if ort:
        logging.info("Optimizing onnx model to ort...")
        subprocess.run(
            f'{sys.executable} -m onnxruntime.tools.convert_onnx_models_to_ort "{os.path.abspath(filename)}" --output_dir "{os.path.splitext(filename)[0]}-ort"',
            shell=True,
        )

    return filename
