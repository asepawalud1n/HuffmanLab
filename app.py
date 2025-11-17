import os
import cv2
import json
import numpy as np
from flask import Flask, render_template, request, send_file, jsonify, Response
from heapq import heapify, heappush, heappop

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
DATASET_FOLDER = "dataset"
DATASET_OUTPUT = "dataset_results"

for f in [UPLOAD_FOLDER, RESULT_FOLDER, DATASET_FOLDER, DATASET_OUTPUT]:
    os.makedirs(f, exist_ok=True)


# ============================
# HUFFMAN NODE
# ============================
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


# ============================
# BUILD HUFFMAN CODES
# ============================
def build_codes(node, code, mapping):
    if node is None:
        return
    if node.symbol is not None:
        mapping[str(node.symbol)] = code
        return
    build_codes(node.left, code + "0", mapping)
    build_codes(node.right, code + "1", mapping)


# ============================
# HOME PAGE
# ============================
@app.route("/")
def index():
    return render_template("index.html")


# ============================
# ENCODE 1 GAMBAR
# ============================
@app.route("/encode", methods=["POST"])
def encode():
    file = request.files["image"]
    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    flat = img.flatten()

    h, w = img.shape

    with open(f"{RESULT_FOLDER}/size.txt", "w") as f:
        f.write(f"{h},{w}")

    # Frekuensi pixel
    freq = {}
    for p in flat:
        freq[p] = freq.get(p, 0) + 1

    heap = [Node(freq[p], p) for p in freq]
    heapify(heap)

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        merged = Node(left.freq + right.freq, None, left, right)
        heappush(heap, merged)

    root = heap[0]

    codes = {}
    build_codes(root, "", codes)

    with open(f"{RESULT_FOLDER}/codes.json", "w") as f:
        json.dump(codes, f)

    encoded = "".join(codes[str(p)] for p in flat)

    with open(f"{RESULT_FOLDER}/compressed.bin", "wb") as f:
        f.write(int(encoded, 2).to_bytes((len(encoded) + 7) // 8, "big"))

    original_size = len(flat) * 8
    compressed_size = len(encoded)
    ratio = round(original_size / compressed_size, 2)

    return render_template(
        "result.html",
        filename=filename,
        original=original_size,
        compressed=compressed_size,
        ratio=ratio,
    )


# ============================
# DECODE 1 GAMBAR
# ============================
@app.route("/decode")
def decode():
    with open(f"{RESULT_FOLDER}/size.txt", "r") as f:
        h, w = map(int, f.read().split(","))

    with open(f"{RESULT_FOLDER}/codes.json", "r") as f:
        codes = json.load(f)

    reverse = {v: int(k) for k, v in codes.items()}

    with open(f"{RESULT_FOLDER}/compressed.bin", "rb") as f:
        bitstring = bin(int.from_bytes(f.read(), "big"))[2:]

    decoded = []
    current = ""

    for bit in bitstring:
        current += bit
        if current in reverse:
            decoded.append(reverse[current])
            current = ""

    arr = np.array(decoded, dtype=np.uint8).reshape((h, w))
    out_path = f"{RESULT_FOLDER}/hasil_decode.png"
    cv2.imwrite(out_path, arr)

    return send_file(out_path, mimetype="image/png")


# ============================
# ENCODE DATASET
# ============================
@app.route("/dataset-encode", methods=["POST"])
def dataset_encode():
    uploaded = request.files.getlist("dataset[]")

    results = []
    total_original = 0
    total_compressed = 0

    for file in uploaded:
        filename = file.filename
        path = os.path.join(DATASET_FOLDER, filename)
        file.save(path)

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        flat = img.flatten()

        freq = {}
        for p in flat:
            freq[p] = freq.get(p, 0) + 1

        heap = [Node(freq[p], p) for p in freq]
        heapify(heap)

        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            merged = Node(left.freq + right.freq, None, left, right)
            heappush(heap, merged)

        root = heap[0]

        codes = {}
        build_codes(root, "", codes)

        encoded = "".join(codes[str(p)] for p in flat)

        with open(os.path.join(DATASET_OUTPUT, filename + ".bin"), "wb") as f:
            f.write(int(encoded, 2).to_bytes((len(encoded) + 7) // 8, "big"))

        original_bits = len(flat) * 8
        compressed_bits = len(encoded)
        ratio = round(original_bits / compressed_bits, 2)

        total_original += original_bits
        total_compressed += compressed_bits

        results.append({
            "name": filename,
            "original": original_bits,
            "compressed": compressed_bits,
            "ratio": ratio
        })

    return render_template(
        "dataset_result.html",
        results=results,
        total_original=total_original,
        total_compressed=total_compressed,
    )


# ============================
# DOWNLOAD CSV
# ============================
@app.route("/download-csv")
def download_csv():
    csv_lines = ["filename,original_bits,compressed_bits,ratio"]

    for file in os.listdir(DATASET_OUTPUT):
        if file.endswith(".bin"):
            name = file.replace(".bin", "")
            csv_lines.append(f"{name},0,0,0")  # placeholder

    csv_data = "\n".join(csv_lines)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=dataset_results.csv"},
    )


if __name__ == "__main__":
    app.run(debug=True)
