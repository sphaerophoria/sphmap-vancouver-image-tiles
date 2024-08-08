import json
import math
import subprocess
from pathlib import Path

def main():
    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    output = []
    i = 0
    for item in dataset:
        print(item)
        zip_path = "{}.zip".format(item["name"])
        url = item["mrsid_url"]
        if not Path(zip_path).exists():
            subprocess.run(["curl", "-k", "-o", zip_path, url], check=True)

        if not Path(item["name"]).exists():
            subprocess.run(["unzip", "-d", item["name"], zip_path], check=True)

        mrsid_path = "{}/{}.sid".format(item["name"], item["name"])
        png_path = "{}/{}.png".format(item["name"], item["name"])
        if not Path(png_path).exists():
            subprocess.run(["mrsiddecode", "-i", mrsid_path, "-o", png_path], check=True)

        jpg_small_path = "{}/{}_10p.jpg".format(item["name"], item["name"])
        if not Path(jpg_small_path).exists():
            subprocess.run(["convert", png_path, "-resize", "10%", jpg_small_path], check=True)

        min_lon = math.inf
        min_lat = math.inf
        max_lon = -math.inf
        max_lat = -math.inf
        for coord in item["geom"]["geometry"]["coordinates"][0][0:4]:
            min_lon = min(min_lon, coord[0])
            min_lat = min(min_lat, coord[1])
            max_lon = max(max_lon, coord[0])
            max_lat = max(max_lat, coord[1])

        width = max_lon - min_lon
        height = max_lat - min_lat

        output.append({
            "center": [min_lon + width / 2, min_lat + height / 2],
            "size": [width, height],
            "path": str(Path(jpg_small_path))
        })

    with open("output.json", "w") as f:
        json.dump(output, f)


if __name__ == "__main__":
    main()
