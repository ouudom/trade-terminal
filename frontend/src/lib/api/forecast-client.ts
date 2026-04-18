import { BaseApiClient } from "./base-client"
import type { WeeklyForecastRow, DailyValidationRow } from "@/lib/types/forecast"

export interface WeeklyForecastPayload {
  instrument_id: number
  instrument: string
  week_of: string
  technical?: Record<string, any>
  fundamental?: Record<string, any>
  sentimental?: Record<string, any>
  confluence?: Record<string, any>
  overall_bias?: string
  overall_ai_analysis?: string
  overall_key_drivers?: string[]
  overall_bias_invalidation_reasons?: string[]
  overall_setup_scenarios?: Record<string, any>
  confidence?: string
  correlation_warning?: string
  high_impact_events?: Array<Record<string, any>>
}

export interface DailyValidationPayload {
  instrument_id: number
  date: string
  session?: string
  price_at_zone?: boolean
  weekly_bias_intact?: boolean
  overnight_news_invalidation?: boolean
  entry_trigger?: Record<string, any>
  tp_path_clear?: boolean
  tp_path_blockers?: string[]
  output?: string
  output_reason?: string
}

export interface UpsertForecastResponse {
  upserted: number
  week_of: string
}

export interface UpsertValidationResponse {
  upserted: number
  date: string
}

export class ForecastApiClient extends BaseApiClient {
  getLatestWeek(): Promise<{ week_of: string | null }> {
    return this.get<{ week_of: string | null }>("/api/forecast/latest-week", { cache: "no-store" })
  }

  getWeeklyForecasts(week: string): Promise<WeeklyForecastRow[]> {
    return this.get<WeeklyForecastRow[]>(`/api/forecast/weekly?week=${week}`, { cache: "no-store" })
  }

  postWeeklyForecast(payload: WeeklyForecastPayload): Promise<UpsertForecastResponse> {
    return this.post<UpsertForecastResponse>("/api/forecast/weekly", payload)
  }

  postDailyValidation(payload: DailyValidationPayload): Promise<UpsertValidationResponse> {
    return this.post<UpsertValidationResponse>("/api/forecast/daily-validation", payload)
  }
}
