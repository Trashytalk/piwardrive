from __future__ import annotations

"""Model explainability helpers."""

from typing import Any, Iterable

import numpy as np
from sklearn.inspection import permutation_importance


def compute_feature_importance(model: Any, X: Iterable[Any], y: Iterable[Any]) -> dict[str, float]:
    """Return feature importance mapping for ``model``."""
    X_arr = np.array(list(X))
    y_arr = np.array(list(y))
    if hasattr(model, "feature_importances_"):
        names = getattr(model, "feature_names_in_", [str(i) for i in range(X_arr.shape[1])])
        return {str(n): float(v) for n, v in zip(names, model.feature_importances_)}
    result = permutation_importance(model, X_arr, y_arr, n_repeats=5, random_state=0)
    names = getattr(model, "feature_names_in_", [str(i) for i in range(X_arr.shape[1])])
    return {str(n): float(v) for n, v in zip(names, result.importances_mean)}


def explain_prediction(model: Any, x: Iterable[Any]) -> dict[str, Any]:
    """Return explanation values for a single prediction."""
    arr = np.array([list(x)])
    try:
        import shap  # type: ignore
    except Exception:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(arr)[0]
            return {"proba": [float(p) for p in proba]}
        return {"prediction": float(model.predict(arr)[0])}
    explainer = shap.Explainer(model)
    vals = explainer(arr)
    return {"values": [float(v) for v in vals.values[0]]}


__all__ = ["compute_feature_importance", "explain_prediction"]
