"""
Huffman Coding Implementation for Image Compression
====================================================
Module ini berisi implementasi lengkap algoritma Huffman Coding
untuk kompresi citra grayscale secara lossless.

Author: Pengolahan Citra Digital Lab
"""

import heapq
import json
import os
from collections import Counter
import numpy as np
import cv2


class HuffmanNode:
    """
    Node untuk pohon Huffman

    Attributes:
        freq (int): Frekuensi kemunculan pixel/node
        pixel (int): Nilai pixel (0-255), None jika node internal
        left (HuffmanNode): Child kiri
        right (HuffmanNode): Child kanan
    """

    def __init__(self, freq, pixel=None, left=None, right=None):
        self.freq = freq
        self.pixel = pixel
        self.left = left
        self.right = right

    def __lt__(self, other):
        """Perbandingan untuk priority queue (heap)"""
        return self.freq < other.freq


class HuffmanCoding:
    """
    Kelas utama untuk kompresi dan dekompresi citra menggunakan Huffman Coding

    Huffman Coding adalah algoritma kompresi lossless yang menggantikan
    setiap pixel dengan kode biner dengan panjang variabel. Pixel yang
    sering muncul mendapat kode pendek, pixel jarang mendapat kode panjang.
    """

    def __init__(self):
        self.codes = {}  # Mapping pixel -> kode biner
        self.reverse_codes = {}  # Mapping kode biner -> pixel
        self.tree = None

    def _build_frequency_table(self, pixels):
        """
        Menghitung frekuensi kemunculan setiap nilai pixel

        Args:
            pixels (np.array): Array 1D dari nilai pixel

        Returns:
            dict: {pixel_value: frequency}
        """
        return dict(Counter(pixels))

    def _build_huffman_tree(self, freq_table):
        """
        Membangun pohon Huffman dari tabel frekuensi

        Algoritma:
        1. Buat leaf node untuk setiap pixel
        2. Masukkan semua node ke priority queue (min-heap)
        3. Loop hingga tersisa 1 node (root):
           - Ambil 2 node dengan frekuensi terkecil
           - Gabungkan menjadi node baru dengan freq = sum
           - Masukkan kembali ke heap

        Args:
            freq_table (dict): Tabel frekuensi pixel

        Returns:
            HuffmanNode: Root dari pohon Huffman
        """
        heap = []

        # Buat leaf node untuk setiap pixel
        for pixel, freq in freq_table.items():
            node = HuffmanNode(freq=freq, pixel=pixel)
            heapq.heappush(heap, node)

        # Bangun pohon bottom-up
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = HuffmanNode(
                freq=left.freq + right.freq,
                left=left,
                right=right
            )
            heapq.heappush(heap, merged)

        return heap[0] if heap else None

    def _generate_codes(self, node, code=""):
        """
        Generate kode Huffman dengan traversal pohon (DFS)

        Traversal:
        - Ke kiri -> tambah '0'
        - Ke kanan -> tambah '1'
        - Leaf node -> simpan kode

        Args:
            node (HuffmanNode): Node saat ini
            code (str): Kode biner saat ini
        """
        if node is None:
            return

        # Jika leaf node (pixel value ada)
        if node.pixel is not None:
            self.codes[node.pixel] = code if code else "0"
            self.reverse_codes[code if code else "0"] = node.pixel
            return

        # Rekursif ke left (0) dan right (1)
        self._generate_codes(node.left, code + "0")
        self._generate_codes(node.right, code + "1")

    def compress_image(self, image_path, output_dir):
        """
        Kompresi gambar lengkap dengan semua file output

        Proses:
        1. Baca dan konversi ke grayscale
        2. Flatten menjadi 1D array
        3. Hitung frekuensi
        4. Bangun pohon Huffman
        5. Generate kode
        6. Encode pixel menjadi bitstream
        7. Simpan ke file binary
        8. Simpan metadata (codes.json, size.txt)

        Args:
            image_path (str): Path gambar input
            output_dir (str): Directory output

        Returns:
            dict: Statistik kompresi {
                'original_size': int (bits),
                'compressed_size': int (bits),
                'compression_ratio': float,
                'filename': str,
                'image_shape': tuple,
                'unique_pixels': int
            }
        """
        # Baca gambar dan konversi ke grayscale
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Tidak dapat membaca gambar: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape

        # Flatten menjadi 1D array
        pixels = gray.flatten()

        # Hitung frekuensi
        freq_table = self._build_frequency_table(pixels)

        # Bangun pohon Huffman
        self.tree = self._build_huffman_tree(freq_table)

        # Generate kode Huffman
        self.codes = {}
        self.reverse_codes = {}
        self._generate_codes(self.tree)

        # Encode: konversi setiap pixel ke kode biner
        encoded_bits = ''.join([self.codes[pixel] for pixel in pixels])

        # Hitung ukuran
        original_size = len(pixels) * 8  # 8 bit per pixel (grayscale)
        compressed_size = len(encoded_bits)

        # Simpan hasil kompresi
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Simpan compressed binary
        bin_path = os.path.join(output_dir, f"{base_name}_compressed.bin")
        self._save_binary(encoded_bits, bin_path)

        # Simpan codes (untuk dekompresi)
        codes_path = os.path.join(output_dir, f"{base_name}_codes.json")
        with open(codes_path, 'w') as f:
            # Konversi key dari int ke str untuk JSON
            json_codes = {str(k): v for k, v in self.codes.items()}
            json.dump(json_codes, f, indent=2)

        # Simpan ukuran gambar
        size_path = os.path.join(output_dir, f"{base_name}_size.txt")
        with open(size_path, 'w') as f:
            f.write(f"{height},{width}")

        # Simpan gambar grayscale asli untuk preview
        gray_path = os.path.join(output_dir, f"{base_name}_gray.png")
        cv2.imwrite(gray_path, gray)

        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': original_size / compressed_size if compressed_size > 0 else 0,
            'filename': os.path.basename(image_path),
            'image_shape': (height, width),
            'unique_pixels': len(freq_table),
            'base_name': base_name
        }

    def _save_binary(self, bit_string, output_path):
        """
        Simpan bitstream ke file binary

        Konversi string '01010101' menjadi bytes.
        Padding dengan '0' jika tidak habis dibagi 8.

        Args:
            bit_string (str): String berisi '0' dan '1'
            output_path (str): Path output file
        """
        # Padding agar habis dibagi 8
        padding = 8 - len(bit_string) % 8
        if padding != 8:
            bit_string += '0' * padding

        # Simpan info padding di awal (1 byte)
        # Byte pertama menyimpan jumlah padding bit
        with open(output_path, 'wb') as f:
            f.write(bytes([padding]))

            # Konversi setiap 8 bit menjadi 1 byte
            for i in range(0, len(bit_string), 8):
                byte = bit_string[i:i+8]
                f.write(bytes([int(byte, 2)]))

    def decompress_image(self, bin_path, codes_path, size_path, output_path):
        """
        Dekompresi gambar dari file binary

        Proses:
        1. Baca kode Huffman dari codes.json
        2. Baca ukuran gambar dari size.txt
        3. Baca bitstream dari .bin
        4. Decode bitstream menjadi pixel array
        5. Reshape ke ukuran asli
        6. Simpan gambar

        Args:
            bin_path (str): Path file binary terkompresi
            codes_path (str): Path file codes.json
            size_path (str): Path file size.txt
            output_path (str): Path output gambar hasil dekode

        Returns:
            dict: Info dekompresi
        """
        # Baca codes
        with open(codes_path, 'r') as f:
            codes = json.load(f)
            # Reverse mapping: code -> pixel
            self.reverse_codes = {v: int(k) for k, v in codes.items()}

        # Baca ukuran gambar
        with open(size_path, 'r') as f:
            height, width = map(int, f.read().strip().split(','))

        # Baca binary file
        with open(bin_path, 'rb') as f:
            padding = f.read(1)[0]  # Byte pertama = padding info
            binary_data = f.read()

        # Konversi bytes ke bitstring
        bit_string = ''.join([bin(byte)[2:].zfill(8) for byte in binary_data])

        # Hapus padding
        if padding != 8:
            bit_string = bit_string[:-padding]

        # Decode bitstream
        pixels = []
        current_code = ""

        for bit in bit_string:
            current_code += bit
            if current_code in self.reverse_codes:
                pixels.append(self.reverse_codes[current_code])
                current_code = ""

        # Reshape ke ukuran asli
        pixel_array = np.array(pixels, dtype=np.uint8)

        # Potong jika ada excess (karena encoding)
        expected_pixels = height * width
        pixel_array = pixel_array[:expected_pixels]

        # Reshape
        img = pixel_array.reshape((height, width))

        # Simpan gambar
        cv2.imwrite(output_path, img)

        return {
            'success': True,
            'output_path': output_path,
            'shape': (height, width),
            'total_pixels': len(pixels)
        }


def calculate_dataset_statistics(results):
    """
    Hitung statistik dari hasil kompresi dataset

    Args:
        results (list): List of compression results

    Returns:
        dict: Statistik lengkap
    """
    if not results:
        return {}

    ratios = [r['compression_ratio'] for r in results]
    original_sizes = [r['original_size'] for r in results]
    compressed_sizes = [r['compressed_size'] for r in results]

    total_original = sum(original_sizes)
    total_compressed = sum(compressed_sizes)

    stats = {
        'mean_ratio': np.mean(ratios),
        'median_ratio': np.median(ratios),
        'max_ratio': max(ratios),
        'min_ratio': min(ratios),
        'total_original_bits': total_original,
        'total_compressed_bits': total_compressed,
        'total_compression_ratio': total_original / total_compressed if total_compressed > 0 else 0,
        'savings_percentage': ((total_original - total_compressed) / total_original * 100) if total_original > 0 else 0,
        'total_files': len(results)
    }

    return stats


# Testing
if __name__ == "__main__":
    print("Huffman Coding Module")
    print("=" * 50)
    print("Module ini berisi implementasi algoritma Huffman")
    print("untuk kompresi citra grayscale secara lossless.")
    print("=" * 50)
