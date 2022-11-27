import argparse
import logging
import os
import pickle

from onnx.checker import check_model
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
from utils import CONFIG

logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


def converter(split: bool, output: str, config: dict):
    os.makedirs(output, exist_ok=True)

    logging.info("Loading model...")
    tfidf = pickle.load(open(config["VECTORIZER"]["path"], "rb"))
    main_model = pickle.load(open(config["MODEL"]["path"], "rb"))

    if not split:
        logging.info("Pipelining tf-idf and main model...")
        from sklearn.pipeline import Pipeline

        model = Pipeline([("tf-idf", tfidf), ("model", main_model)])

        logging.info("Converting model...")
        initial_type = [("words", StringTensorType([None, 1]))]
        options = {"model": {"zipmap": False}}
        onnx_model = convert_sklearn(model, initial_types=initial_type, options=options)
        with open(os.path.join(output, "model.onnx"), "wb") as writer:
            writer.write(onnx_model.SerializeToString())
        check_model(onnx_model)
    else:
        from skl2onnx.common.data_types import FloatTensorType

        logging.info("Converting TF-IDF...")
        initial_type = [("words", StringTensorType([None, 1]))]
        tfidf_onnx = convert_sklearn(tfidf, initial_types=initial_type)
        with open(os.path.join(output, "tf-idf.onnx"), "wb") as writer:
            writer.write(tfidf_onnx.SerializeToString())
        check_model(tfidf_onnx)

        logging.info("Converting Main Model...")
        initial_type = [("words_mat", FloatTensorType([None, 1000]))]
        options = {"zipmap": False}
        onnx_model = convert_sklearn(main_model, initial_types=initial_type, options=options)
        with open(os.path.join(output, "main-model.onnx"), "wb") as writer:
            writer.write(onnx_model.SerializeToString())
        check_model(onnx_model)

    logging.info(
        f"Exported to {output} \n\nPlease use Neutron to view the model \nhttps://netron.app/"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export scikit-learn model to onnx",
        epilog="Please change model path in './config.json' to your custom model",
    )
    parser.add_argument(
        "-s",
        "--split",
        help="Convert tf-idf and main model by itself (without Pipeline)",
        action="store_true",
    )
    parser.add_argument("-o", "--output", help="Output directory", type=str, default="./output")

    args = parser.parse_args()
    logging.info("Starting script with params:")
    for arg, value in vars(args).items():
        print(f"   * {arg}  : {value}")

    logging.info("Loadding configurations from './config.json'")
    config = CONFIG("./config.json")

    converter(split=args.split, output=args.output, config=config.data)
