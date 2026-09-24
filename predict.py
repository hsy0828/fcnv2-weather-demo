import subprocess
import os

def main():
    print("=== 開始執行 FCNV2 氣象預測流程 ===")
    
    # 1. 執行預測
    cmd = [
        "ai-models",
        "--input", "gfs",
        "--date", "20240101",
        "--time", "0000",
        "--lead-time", "24",
        "fourcastnetv2-small"
    ]
    
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
