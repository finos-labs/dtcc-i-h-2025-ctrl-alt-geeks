export enum ApiMethods {
    PROFILE = 'getProfile',
    HOLDINGS = 'getHoldings',
    POSITIONS = 'getPositions',
    ORDER_HISTORY = 'getOrderHistory',
    PLACE_ORDER = 'placeOrder',
    CANCEL_ORDER = 'cancelOrder',
}

export type TransactionType = 'BUY' | 'SELL';