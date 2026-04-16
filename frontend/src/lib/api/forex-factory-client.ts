import { BaseApiClient } from "./base-client"
import type { ForexEvent } from "@/lib/types"

export class ForexFactoryApiClient extends BaseApiClient {
  getEvents(): Promise<ForexEvent[]> {
    return this.get<ForexEvent[]>("/forexfactory/events")
  }

  fetchCalendar(week: string): Promise<void> {
    return this.get<void>(`/forexfactory/calendar?week=${encodeURIComponent(week)}`)
  }
}
