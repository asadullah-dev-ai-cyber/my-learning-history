from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def get_top_colors(image_path, num_colors=10):
    # 1. Open image and convert to RGB
    img = Image.open(image_path).convert('RGB')

    # 2. Resize to speed up clustering execution
    img.thumbnail((150, 150))

    # 3. Convert to 2D array of pixels (Total Pixels x 3)
    img_arr = np.array(img)
    pixels = img_arr.reshape(-1, 3)

    # 4. Use KMeans to cluster similar colors together into 10 groups
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)

    # 5. Extract cluster center RGB values and counts
    cluster_centers = kmeans.cluster_centers_  # RGB float arrays
    labels = kmeans.labels_  # Assigns each pixel to a cluster

    # Count frequency of pixels in each cluster
    counts = np.bincount(labels)

    # 6. Sort clusters by population size (most dominant first)
    sorted_indices = np.argsort(counts)[::-1]
    dominant_rgb = cluster_centers[sorted_indices]

    # 7. Convert dominant RGB floats to integer Hex codes
    hex_colors = []
    for r, g, b in dominant_rgb:
        hex_code = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
        hex_colors.append(hex_code)

    return hex_colors