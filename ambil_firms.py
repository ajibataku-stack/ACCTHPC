#!/usr/bin/env python3
"""Ambil hotspot terbaru Indonesia dari NASA FIRMS dan gabungkan jadi satu CSV.

Hasilnya (hotspot_idn.csv) bisa dimuat ke halaman Pantau Hotspot lewat tombol
"Muat CSV FIRMS".

Cara pakai:
  1. Minta MAP_KEY gratis di https://firms.modaps.eosdis.nasa.gov/api/map_key/
  2. Simpan sebagai variabel lingkungan (jangan ditulis di berkas ini):
       Linux/macOS:  export FIRMS_MAP_KEY="kunci_anda"
       Windows:      setx FIRMS_MAP_KEY "kunci_anda"
  3. Jalankan:
       python3 ambil_firms.py                # 2 hari terakhir, tiga satelit VIIRS
       python3 ambil_firms.py --hari 5       # rentang hari lain
       python3 ambil_firms.py --modis        # tambahkan MODIS

Untuk pembaruan otomatis, jadwalkan di komputer Anda, misalnya cron tiap 3 jam:
  0 */3 * * *  FIRMS_MAP_KEY=kunci_anda /usr/bin/python3 /jalur/ambil_firms.py

Hanya memakai pustaka standar Python 3.8+.
"""
import argparse
import os
import sys
import urllib.error
import urllib.request

BASE = "https://firms.modaps.eosdis.nasa.gov/api/country/csv"
VIIRS = ["VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT"]
MODIS = ["MODIS_NRT"]


def ambil(key, sumber, negara, hari):
    url = f"{BASE}/{key}/{sumber}/{negara}/{hari}"
    req = urllib.request.Request(url, headers={"User-Agent": "pantau-hotspot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser(description="Ambil hotspot FIRMS untuk Indonesia.")
    ap.add_argument("--hari", type=int, default=2, help="jumlah hari ke belakang (default 2)")
    ap.add_argument("--negara", default="IDN", help="kode negara 3 huruf (default IDN)")
    ap.add_argument("--modis", action="store_true", help="sertakan MODIS_NRT")
    ap.add_argument("--keluar", default="hotspot_idn.csv", help="nama berkas hasil")
    a = ap.parse_args()

    key = os.environ.get("FIRMS_MAP_KEY", "").strip()
    if not key:
        sys.exit("FIRMS_MAP_KEY belum diatur. Lihat petunjuk di bagian atas berkas ini.")

    header, baris = None, []
    for s in VIIRS + (MODIS if a.modis else []):
        try:
            teks = ambil(key, s, a.negara, a.hari)
        except urllib.error.HTTPError as e:
            print(f"[{s}] gagal: HTTP {e.code}", file=sys.stderr)
            continue
        except urllib.error.URLError as e:
            print(f"[{s}] gagal: {e.reason}", file=sys.stderr)
            continue
        baris_s = [l for l in teks.splitlines() if l.strip()]
        if not baris_s or not baris_s[0].lower().startswith("latitude"):
            print(f"[{s}] respons bukan CSV: {baris_s[0][:120] if baris_s else 'kosong'}", file=sys.stderr)
            continue
        if header is None:
            header = baris_s[0]
        elif baris_s[0] != header:
            # kolom MODIS berbeda dari VIIRS; simpan terpisah agar tidak merusak kolom
            nama = a.keluar.replace(".csv", f"_{s.lower()}.csv")
            with open(nama, "w", encoding="utf-8") as f:
                f.write("\n".join(baris_s) + "\n")
            print(f"[{s}] kolom berbeda, disimpan terpisah: {nama} ({len(baris_s) - 1} baris)")
            continue
        baris.extend(baris_s[1:])
        print(f"[{s}] {len(baris_s) - 1} baris")

    if header is None:
        sys.exit("Tidak ada data yang berhasil diambil. Periksa MAP_KEY dan koneksi.")
    with open(a.keluar, "w", encoding="utf-8") as f:
        f.write(header + "\n" + "\n".join(baris) + "\n")
    print(f"Selesai: {len(baris)} hotspot disimpan di {a.keluar}")


if __name__ == "__main__":
    main()
