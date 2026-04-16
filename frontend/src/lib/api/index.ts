export { ApiError } from "./base-client"
export type { SnapshotRow } from "./bias-client"
export type { Instrument } from "./instruments-client"

import { ForexApiClient } from "./forex-client"
import { BiasApiClient } from "./bias-client"
import { ForexFactoryApiClient } from "./forex-factory-client"
import { InstrumentsApiClient } from "./instruments-client"

export const forexApi = new ForexApiClient()
export const biasApi = new BiasApiClient()
export const forexFactoryApi = new ForexFactoryApiClient()
export const instrumentsApi = new InstrumentsApiClient()
