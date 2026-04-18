import { BaseApiClient } from "./base-client"
import type { WeeklyForecastRow } from "@/lib/types/forecast"

export class ForecastApiClient extends BaseApiClient {
  getLatestWeek(): Promise<{ week_of: string | null }> {
    return this.get<{ week_of: string | null }>("/forecast/latest-week", { cache: "no-store" })
  }

  getWeeklyForecasts(week: string): Promise<WeeklyForecastRow[]> {
    return this.get<WeeklyForecastRow[]>(`/forecast/weekly?week=${week}`, { cache: "no-store" })
  }
}
