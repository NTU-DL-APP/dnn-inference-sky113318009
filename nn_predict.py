import numpy as np
import json

# === Activation functions ===

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    if x.ndim == 1:
        # 適用於單一樣本輸入，例如 [2.0, 1.0, 0.1]
        e_x = np.exp(x - np.max(x))
        return e_x / np.sum(e_x)
    elif x.ndim == 2:
        # 適用於批次輸入，例如 [[2.0, 1.0, 0.1], [...], ...]
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / np.sum(e_x, axis=1, keepdims=True)
    else:
        raise ValueError("Input to softmax must be 1D or 2D")



# === Flatten ===
def flatten(x):
    return x.reshape(x.shape[0], -1)

# === Dense layer ===
def dense(x, W, b):
    return x @ W + b

# Infer TensorFlow h5 model using numpy
# Support only Dense, Flatten, relu, softmax now
def nn_forward_h5(model_arch, weights, data):
    x = data
    for layer in model_arch:
        lname = layer['name']
        ltype = layer['type']
        cfg = layer['config']
        wnames = layer['weights']

        if ltype == "Flatten":
            x = flatten(x)
        elif ltype == "Dense":
            W = weights[wnames[0]]
            b = weights[wnames[1]]
            x = dense(x, W, b)
            if cfg.get("activation") == "relu":
                x = relu(x)
            elif cfg.get("activation") == "softmax":
                x = softmax(x)

    return x


# You are free to replace nn_forward_h5() with your own implementation 
def nn_inference(model_arch, weights, data):
    return nn_forward_h5(model_arch, weights, data)
    
