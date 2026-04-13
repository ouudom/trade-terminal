import { BaseApiClient } from "./base-client"
import type { RawCandle } from "@/lib/types"

export class ForexApiClient extends BaseApiClient {
  getChartCandles(symbol: string, timeframe: string): Promise<RawCandle[]> {
    return this.get<RawCandle[]>(`/forex/chart/${symbol}?timeframe=${timeframe}`, {
      cache: "no-store",
    })
  }
}
