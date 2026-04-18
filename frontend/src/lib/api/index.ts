export { ApiError } from "./base-client"
export type { Instrument } from "./instruments-client"

import { InstrumentsApiClient } from "./instruments-client"
import { ForecastApiClient } from "./forecast-client"

export const instrumentsApi = new InstrumentsApiClient()
export const forecastApi = new ForecastApiClient()
