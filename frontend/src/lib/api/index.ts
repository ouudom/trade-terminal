export { ApiError } from "./base-client"
export type { SnapshotRow } from "./bias-client"
export type { Instrument } from "./instruments-client"

import { BiasApiClient } from "./bias-client"
import { InstrumentsApiClient } from "./instruments-client"

export const biasApi = new BiasApiClient()
export const instrumentsApi = new InstrumentsApiClient()
