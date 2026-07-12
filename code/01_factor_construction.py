import argparse
from pathlib import Path

import numpy as np
import pandas as pd

def make_mock_stock_data(
    n_stocks: int = 200,
    n_days: int = 300,
    seed: int = 42,
) -> pd.DataFrame:
      """
    生成模拟股票面板数据。

    输出字段：
    - date
    - instrument
    - close
    - volume

    这里加入一点“短期反转”特征：
    前一天跌得多的股票，下一天有轻微反弹倾向。
    这样后面评价 reverse_5d 时更容易看到效果。
    """
  rng = np.random.default_rng(seed)
  dates = pd.bdate_range("2023-01-02", periods=n_days)
  instruments = [f"{i:06d}.SZ" for i in range(1, n_stocks + 1)]

  rows = []

  for instrument in instruments:
    price = 10 + rng.normal(0, 1)
    prev_return = 0.0

    for date in dates:
      market_return = rng.normal(0.0002, 0.01)
      stock_noise = rng.normal(0, 0.02)

      # 模拟短期反转：昨天跌，今天更容易涨一点；昨天涨，今天更容易回落一点
      reversal_effect = -0.15 * prev_return

      daily_return = market_return + stock_noise + reversal_effect
      price = price * (1 + daily_return)
      price = max(price, 1)

      volume = int(rng.lognormal(mean=14, sigma=0.6))

      rows.append(
        {
          "date": date,
          "instrument": instrument,
          "close": price,
          "volume": volume,
        }
      )
      
      prev_return = daily_return
      
      df = pd.DataFrame(rows)
      return df











