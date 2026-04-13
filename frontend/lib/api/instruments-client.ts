import { BaseApiClient } from "./base-client"

export interface Instrument {
  id: number
  symbol: string
  name: string
  asset_class: string
  is_active: boolean
}

export class InstrumentsApiClient extends BaseApiClient {
  list(): Promise<Instrument[]> {
    return this.get<Instrument[]>("/instruments")
  }

  update(id: number, payload: Partial<Instrument>): Promise<Instrument> {
    return this.put<Instrument>(`/instruments/${id}`, payload)
  }
}
