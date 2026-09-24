import os
import subprocess

def main():
    print("=== 開始執行 FCNV2 氣象預測流程 ===")
    
    # 執行 ai-models 進行預測（此步驟會自動下載模型權重與氣象資料）
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
    except Exception as e:
        print(f"執行失敗，錯誤訊息：{e}")

if __name__ == "__main__":
    main()
