import numpy as np
import os
import pandas as pd

# ======== User-Defined Parameters ========

# Name of the trial (used in filenames and directories)
base = "Multiple"  # Change this to match your trial prefix (e.g., "Single", "Trial1", etc.)

# Path to the input folder containing .npz files
input_dir = os.path.join("path", "to", "your", "npz", "files", base)  # <- Change this

# Path to the output folder for .csv files
output_dir = os.path.join("path", "to", "save", "csv", base + "_csv")  # <- Change this

# Number of tracked organisms (50 as an example here.)
N = 50

# Range of frames to analyze (0 to the max frame # of the video.)
START = 0
STOP = 18000

# ========================================

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

for i in range(N):
    input_file = os.path.join(input_dir, f"Daphniaall50HQ_fish{i}.npz")
    output_file = os.path.join(output_dir, f"{base}_daphnia{i}.csv")

    with np.load(input_file) as npz:
        X = npz["X#wcentroid"]
        Y = -npz["Y#wcentroid"]
        time = npz["time"]
        frame = npz["frame"]
        speed_centroid = npz["SPEED#wcentroid"]
        speed_precomputed = npz["SPEED"]
        missing = npz["missing"].astype(bool)

    clean = ~missing

    if START == 0:
        X_clean = X[clean][START:STOP - sum(missing)]
        Y_clean = Y[clean][START:STOP - sum(missing)]
        time_clean = time[clean][START:STOP - sum(missing)]
        frame_clean = frame[clean][START:STOP - sum(missing)]
    else:
        X_clean = X[clean][START - sum(missing):STOP - sum(missing)]
        Y_clean = Y[clean][START - sum(missing):STOP - sum(missing)]
        time_clean = time[clean][START - sum(missing):STOP - sum(missing)]
        frame_clean = frame[clean][START - sum(missing):STOP - sum(missing)]

    fps = frame_clean[-1] / time_clean[-1]

    df = pd.DataFrame({
        'X': X_clean.T,
        'Y': Y_clean.T,
        'Time': time_clean.T,
        'fps': fps.T
    })

    df.to_csv(output_file, index=False)
