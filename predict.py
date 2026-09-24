import subprocess
import os

def main():
    print("=== 開始執行 FCNV2 氣象預測流程 ===")
    
    # 1. 執行預測
   # 設定你想預測的總小時數與間隔
max_hours = 72  # 未來想改 24、72、120 直接改這個數字
step_hours = 6

cmd = [
    "ai-models",
    "--input",
    "ecmwf-open-data",
    "--date",
    "20240101",
    "--time",
    "0000",
]

# 自動產生: --lead-time 6 --lead-time 12 ... 直到 --lead-time 72
for lead_time in range(step_hours, max_hours + 1, step_hours):
    cmd.extend(["--lead-time", str(lead_time)])

cmd.append("fourcastnetv2-small")
    
    try:
        print("正在下載資料與權重，並執行預測中...")
        subprocess.run(cmd, check=True)
        print("預測完成！結果已儲存至 fourcastnetv2-small.grib")
        
        # 2. 自動執行繪圖腳本
        print("開始執行自動繪圖...")
        subprocess.run(["python", "plot_result.py"], check=True)
        
    except Exception as e:
        print(f"執行失敗，錯誤訊息：{e}")

if __name__ == "__main__":
    main()
