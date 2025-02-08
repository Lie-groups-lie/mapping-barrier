import numpy as np
import geopandas as gpd
from shapely.geometry import shape
from rasterio.features import shapes
from affine import Affine
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def polygonize_image(input_png, output_geojson):
    # 1. 读取图像并二值化
    img = Image.open(input_png).convert('L')
    arr = np.array(img)
    # 若图像中有非 0/255 值，进行阈值化处理
    arr = (arr > 127).astype(np.uint8) * 255  # 结果仅为 0 或 255

    # 2. 定义仿射变换：
    transform = Affine.translation(0, 0) * Affine.scale(1, -1)

    # 3. 使用 rasterio.features.shapes 提取多边形
    results = list(shapes(arr, mask=None, transform=transform, connectivity=8))
    features = []
    for geom, value in results:
        # 将 geom 转换为 shapely 几何对象
        poly = shape(geom)
        features.append({
            "geometry": poly,
            "value": int(value),
            "name": "" 
        })

    # 4. 分离黑色区域，过滤掉白色区域（像素值为 255），并对黑色区域按面积降序排序
    black_features = [feat for feat in features if feat["value"] == 0]
    black_features = sorted(black_features, key=lambda feat: feat["geometry"].area, reverse=True)
    for idx, feat in enumerate(black_features, start=1):
        feat["order"] = idx
        feat["base"] = "black" 
    all_features = black_features

    # 5. 构造 GeoDataFrame 并输出 GeoJSON 文件
    gdf = gpd.GeoDataFrame(all_features)
    gdf.set_crs(epsg=4326, inplace=True)
    gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"GeoJSON 文件已保存为：{output_geojson}")
