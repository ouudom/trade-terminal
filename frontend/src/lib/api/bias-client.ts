import { BaseApiClient } from "./base-client"

export interface SnapshotRow {
  snapshot_id: string
  instrument_id: number
  symbol: string
  name: string
  timeframe: string
  bias: string
  confidence: number
  summary: string
  key_drivers: string | null
  invalidation_notes: string | null
  valid_from: string
  valid_until: string | null
  macro: unknown
}

export class BiasApiClient extends BaseApiClient {
  getSnapshots(): Promise<SnapshotRow[]> {
    return this.get<SnapshotRow[]>("/bias/snapshots", { cache: "no-store" })
  }
}
