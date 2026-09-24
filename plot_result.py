import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_temperature_and_wind():
    grib_file = "fourcastnetv2-small.grib"
    
    if not os.path.exists(grib_file):
        print(f"錯誤：找不到 {grib_file}，請先執行預測腳本！")
        return

    print("正在讀取預測結果並繪製 氣溫 + 風場 地圖...")
    
    # 1. 讀取氣溫 (2t) 與 10m 風速分量 (10u, 10v)
    # 使用 cfgrib 分別讀取需要的變數
    ds_temp = xr.open_dataset(grib_file, engine='cfgrib', backend_kwargs={'filter_by_keys': {'shortName': '2t'}})
    ds_wind = xr.open_dataset(grib_file, engine='cfgrib', backend_kwargs={'filter_by_keys': {'typeOfLevel': 'surface'}})

    # 2. 數據轉換與計算
    t2m_celsius = ds_temp['t2m'] - 273.15  # 轉為攝氏 (°C)
    
    u10 = ds_wind['u10']  # 東西向風速 (m/s)
    v10 = ds_wind['v10']  # 南北向風速 (m/s)
    wind_speed = np.sqrt(u10**2 + v10**2)  # 計算總風速

    # 3. 建立地圖
    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # 4. 繪製氣溫底圖 (Contourf / Plot)
    temp_plot = t2m_celsius.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap='coolwarm',
        cbar_kwargs={'label': '2m 氣溫 (°C)', 'shrink': 0.7, 'pad': 0.02}
    )

    # 5. 繪製風場箭頭 (Quiver) - 進行適當抽樣，避免地圖箭頭過於密集
    skip = 10  # 每隔 10 個格點畫一個箭頭
    
    lons = ds_wind.longitude.values[::skip]
    lats = ds_wind.latitude.values[::skip]
    u_sampled = u10.values[::skip, ::skip]
    v_sampled = v10.values[::skip, ::skip]

    # 畫出風向箭頭
    ax.quiver(
        lons, lats, u_sampled, v_sampled,
        transform=ccrs.PlateCarree(),
        scale=400,          # 控制箭頭長度比例
        color='black',      # 箭頭顏色
        alpha=0.6,          # 透明度
        width=0.0015        # 箭頭粗細
    )

    # 6. 加入地理特徵
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5, edgecolor='gray')
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, alpha=0.3)

    plt.title("FCNV2 全球預測：2公尺氣溫 (°C) 與 10公尺風場向量", fontsize=15, pad=12)

    ax.set_extent([115, 126, 20, 27], crs=ccrs.PlateCarree())  # [西經, 東經, 南緯, 北緯]
    
    # 7. 儲存圖片
    output_png = "forecast_temp_wind.png"
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"繪圖完成！結果已儲存為：{output_png}")

if __name__ == "__main__":
    plot_temperature_and_wind()
