import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_temperature():
    grib_file = "fourcastnetv2-small.grib"
    
    if not os.path.exists(grib_file):
        print(f"錯誤：找不到 {grib_file}，請先執行預測腳本！")
        return

    print("正在讀取預測結果並繪製地圖...")
    
    # 讀取 GRIB 檔案中的 2m 氣溫 (t2m)
    ds = xr.open_dataset(grib_file, engine='cfgrib', backend_kwargs={'filter_by_keys': {'shortName': '2t'}})
    
    # 將開氏溫度 (K) 轉換為攝氏溫度 (°C)
    t2m_celsius = ds['t2m'] - 273.15

    # 建立地圖畫布 (使用 PlateCarree 投影)
    fig = plt.figure(figsize=(14, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # 繪製溫度填色圖
    im = t2m_celsius.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap='coolwarm',
        cbar_kwargs={'label': '溫度 (°C)', 'shrink': 0.7}
    )

    # 加入地圖特徵（海岸線與國界）
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, alpha=0.5)

    plt.title("FCNV2 24小時 全球2公尺氣溫預測圖", fontsize=14, pad=10)
    
    # 儲存圖檔
    output_png = "forecast_t2m.png"
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"繪圖完成！圖檔已儲存為：{output_png}")

if __name__ == "__main__":
    plot_temperature()
