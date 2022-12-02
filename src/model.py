from typing import List, Tuple, Union

import numpy as np
import numpy.typing as npt
import onnx
import onnxruntime as ort


class Model:
    """ONNX Model handler

    Args:
        model_path (str): onnx model path
    """

    def __init__(self, model_path: str) -> None:
        self._path = model_path
        self.onnx_model = onnx.load_model(model_path)
        self.session = ort.InferenceSession(model_path)

    def summary(self) -> None:  # pragma: no cover
        """Print model summary"""
        print(f"Model : {self._path}\n")
        print("Input :")
        for x in self.session.get_inputs():
            print(f"  * {x.name} - {x.type} - {x.shape}")
        print("Output :")
        for i, x in enumerate(self.session.get_outputs()):
            print(f"  {i}. {x.name} - {x.type} - {x.shape}")
        print("Nodes :")
        for i, x in enumerate(self.onnx_model.graph.node):
            print(f"  {i}. {x.name}")

    def predict(
        self, texts: Union[str, List[str], npt.NDArray[np.string_]]
    ) -> Tuple[npt.NDArray[np.int64], npt.NDArray[np.float64]]:
        """Predict using model.

        Args:
            texts (Union[str, List[str], npt.NDArray[np.string_]]): Teks input yang akan di deteksi
            oleh model. Dapat berupa string tunggal atau sequence berupa list ataupun numpy array.

        Returns:
            Hasil deteksi berupa tupple dengan format (label, probabilities).
        """
        if type(texts) == str:
            X = np.asarray([[texts]])
        elif type(texts) == list:
            X = np.asarray(texts).reshape(-1, 1)
        elif type(texts) == np.ndarray:
            if len(texts.shape) == 2 and texts.shape[1] == 1:
                X = texts
            elif len(texts.shape) == 1:
                X = texts.reshape(-1, 1)
            else:  # pragma: no cover
                raise NotImplementedError("Only take 1-Dim or (None, 1) array shape!")
        else:  # pragma: no cover
            raise TypeError("Not supported input type!")

        assert len(X.shape) == 2, "Dimension Error!"
        assert X.shape[1] == 1, "Dimension Error!"
        result: Tuple[npt.NDArray[np.int64], npt.NDArray[np.float64]] = self.session.run(
            None, {"words": X}
        )
        return result
