import { WeeklyForecastDashboard } from "@/components/features/weekly-forecast/weekly-forecast-dashboard"
import { forecastApi } from "@/lib/api"
import type { WeeklyForecastRow } from "@/lib/types/forecast"

export default async function WeeklyForecastPage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string }>
}) {
  const params = await searchParams

  let weekOf = params.week ?? null
  let rows: WeeklyForecastRow[] = []

  try {
    if (!weekOf) {
      const { week_of } = await forecastApi.getLatestWeek()
      weekOf = week_of
    }

    if (weekOf) {
      rows = await forecastApi.getWeeklyForecasts(weekOf)
    }
  } catch {
    // Backend unavailable — render with empty state
  }

  return <WeeklyForecastDashboard rows={rows} weekOf={weekOf ?? ""} />
}
