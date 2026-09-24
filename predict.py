import sys
from ai_models.inputs import available_inputs
from ai_models.outputs import available_outputs
# 1. 手動匯入並註冊 FourCastNetV2 模型
import ai_models_fourcastnetv2_gfs
from ai_models_fourcastnetv2_gfs.model import FourCastNetv2SmallModel

# 2. 定義預測參數
args = [
    "--input",
    "ecmwf-open-data",
    "--date",
    "20240101",
    "--time",
    "0000",
    "--lead-time",
    "6",
    "--lead-time",
    "12",
    "--lead-time",
    "18",
    "--lead-time",
    "24",
    "--lead-time",
    "30",
    "--lead-time",
    "36",
    "--lead-time",
    "42",
    "--lead-time",
    "48",
    "--lead-time",
    "54",
    "--lead-time",
    "60",
    "--lead-time",
    "66",
    "--lead-time",
    "72",
]

print("=== 開始執行 FourCastNetV2 氣象預測 ===")

# 3. 直接實例化並執行模型 (繞過 CLI 註冊問題)
try:
    model = FourCastNetv2SmallModel(
        input=available_inputs()["ecmwf-open-data"](
            date=20240101, time=0, lead_time=72
        ),
        output=available_outputs()["file"](
            path="fourcastnetv2-small.grib",
        ),
        date=20240101,
        time=0,
        lead_time=[6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72],
    )
    model.run()
    print("預測成功完成！已輸出 fourcastnetv2-small.grib")
except Exception as e:
    # 若上述 API 封裝較為複雜，可用極簡的 CLI 內部物件呼叫方式：
    from ai_models.model import load_model

    print("嘗試使用 ai_models.model 直載模式...")
    # 強制將模型注入 ai-models 的清單中
    from ai_models.model import MODELS

    MODELS["fourcastnetv2-small"] = FourCastNetv2SmallModel

    # 執行 CLI 主入口
    from ai_models.__main__ import main

    sys.argv = ["ai-models"] + args + ["fourcastnetv2-small"]
    main()
