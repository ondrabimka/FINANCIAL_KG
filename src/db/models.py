from typing import Optional

from gqlalchemy import Field, Memgraph, Node, Relationship

memgraph = Memgraph()


class Ticker(Node):
    __label__ = "Ticker"
    ticker: str = Field(index=True, exists=True, unique=True, db=memgraph)
    address1: str = Field()
    city: str = Field()
    state: str = Field()
    zip: str = Field()
    country: str = Field()
    phone: str = Field()
    website: str = Field()
    industry: str = Field()
    industryKey: str = Field()
    industryDisp: str = Field()
    sector: str = Field()
    sectorKey: str = Field()
    sectorDisp: str = Field()
    longBusinessSummary: str = Field()
    fullTimeEmployees: Optional[int] = Field()
    auditRisk: Optional[int] = Field()
    boardRisk: Optional[int] = Field()
    compensationRisk: Optional[int] = Field()
    shareHolderRightsRisk: Optional[int] = Field()
    overallRisk: Optional[int] = Field()
    governanceEpochDate: Optional[int] = Field()
    compensationAsOfEpochDate: Optional[int] = Field()
    irWebsite: Optional[str] = Field()
    maxAge: Optional[int] = Field()
    priceHint: Optional[int] = Field()
    previousClose: Optional[float] = Field()
    open: Optional[float] = Field()
    dayLow: Optional[float] = Field()
    dayHigh: Optional[float] = Field()
    regularMarketPreviousClose: Optional[float] = Field()
    regularMarketOpen: Optional[float] = Field()
    regularMarketDayLow: Optional[float] = Field()
    regularMarketDayHigh: Optional[float] = Field()
    dividendRate: Optional[float] = Field()
    dividendYield: Optional[float] = Field()
    exDividendDate: Optional[int] = Field()
    payoutRatio: Optional[float] = Field()
    fiveYearAvgDividendYield: Optional[float] = Field()
    beta: Optional[float] = Field()
    trailingPE: Optional[float] = Field()
    forwardPE: Optional[float] = Field()
    volume: Optional[int] = Field()
    regularMarketVolume: Optional[int] = Field()
    averageVolume: Optional[int] = Field()
    averageVolume10days: Optional[int] = Field()
    averageDailyVolume10Day: Optional[int] = Field()
    bid: Optional[float] = Field()
    ask: Optional[float] = Field()
    bidSize: Optional[int] = Field()
    askSize: Optional[int] = Field()
    marketCap: Optional[int] = Field()
    fiftyTwoWeekLow: Optional[float] = Field()
    fiftyTwoWeekHigh: Optional[float] = Field()
    priceToSalesTrailing12Months: Optional[float] = Field()
    fiftyDayAverage: Optional[float] = Field()
    twoHundredDayAverage: Optional[float] = Field()
    trailingAnnualDividendRate: Optional[float] = Field()
    trailingAnnualDividendYield: Optional[float] = Field()
    currency: Optional[str] = Field()
    enterpriseValue: Optional[int] = Field()
    profitMargins: Optional[float] = Field()
    floatShares: Optional[int] = Field()
    sharesOutstanding: Optional[int] = Field()
    sharesShort: Optional[int] = Field()
    sharesShortPriorMonth: Optional[int] = Field()
    sharesShortPreviousMonthDate: Optional[int] = Field()
    dateShortInterest: Optional[int] = Field()
    sharesPercentSharesOut: Optional[float] = Field()
    heldPercentInsiders: Optional[float] = Field()
    heldPercentInstitutions: Optional[float] = Field()
    shortRatio: Optional[float] = Field()
    shortPercentOfFloat: Optional[float] = Field()
    impliedSharesOutstanding: Optional[int] = Field()
    bookValue: Optional[float] = Field()
    priceToBook: Optional[float] = Field()
    lastFiscalYearEnd: Optional[int] = Field()
    nextFiscalYearEnd: Optional[int] = Field()
    mostRecentQuarter: Optional[int] = Field()
    earningsQuarterlyGrowth: Optional[float] = Field()
    netIncomeToCommon: Optional[int] = Field()
    trailingEps: Optional[float] = Field()
    forwardEps: Optional[float] = Field()
    pegRatio: Optional[float] = Field()
    lastSplitFactor: str = Field()
    lastSplitDate: Optional[int] = Field()
    enterpriseToRevenue: Optional[float] = Field()
    enterpriseToEbitda: Optional[float] = Field()
    fiftyTwoWeekChange: Optional[float] = Field()
    SandP52WeekChange: Optional[float] = Field()
    lastDividendValue: Optional[float] = Field()
    lastDividendDate: Optional[int] = Field()
    exchange: str = Field()
    quoteType: str = Field()
    underlyingSymbol: str = Field()
    shortName: str = Field()
    longName: str = Field()
    firstTradeDateEpochUtc: Optional[int] = Field()
    timeZoneFullName: str = Field()
    timeZoneShortName: str = Field()
    uuid: str = Field()
    messageBoardId: str = Field()
    gmtOffSetMilliseconds: Optional[int] = Field()
    currentPrice: Optional[float] = Field()
    targetHighPrice: Optional[float] = Field()
    targetLowPrice: Optional[float] = Field()
    targetMeanPrice: Optional[float] = Field()
    targetMedianPrice: Optional[float] = Field()
    recommendationMean: Optional[float] = Field()
    recommendationKey: str = Field()
    numberOfAnalystOpinions: Optional[int] = Field()
    totalCash: Optional[int] = Field()
    totalCashPerShare: Optional[float] = Field()
    ebitda: Optional[int] = Field()
    totalDebt: Optional[int] = Field()
    quickRatio: Optional[float] = Field()
    currentRatio: Optional[float] = Field()
    totalRevenue: Optional[int] = Field()
    debtToEquity: Optional[float] = Field()
    revenuePerShare: Optional[float] = Field()
    returnOnAssets: Optional[float] = Field()
    returnOnEquity: Optional[float] = Field()
    freeCashflow: Optional[int] = Field()
    operatingCashflow: Optional[int] = Field()
    earningsGrowth: Optional[float] = Field()
    revenueGrowth: Optional[float] = Field()
    grossMargins: Optional[float] = Field()
    ebitdaMargins: Optional[float] = Field()
    operatingMargins: Optional[float] = Field()
    financialCurrency: str = Field()
    trailingPegRatio: Optional[float] = Field()
    insiderPurchases: Optional[int] = Field()
    insiderSales: Optional[int] = Field()
    insiderNetSharesPurchased: Optional[int] = Field()
    insiderTotalInsiderSharesHeld: Optional[int] = Field()
    insiderPercentNetSharesPurchased: Optional[float] = Field()
    insiderPercentBuyShares: Optional[float] = Field()
    insiderPercentSellShares: Optional[float] = Field()
    insidersPercentHeld: Optional[float] = Field()
    institutionsPercentHeld: Optional[float] = Field()
    institutionsFloatPercentHeld: Optional[float] = Field()
    institutionsCount: Optional[int] = Field()


class InsiderHolder(Node):
    __label__ = "InsiderHolder"
    name: str = Field(index=True, exists=True, unique=True, db=memgraph)
    position: Optional[str] = Field()
    mostRecentTransaction: Optional[str] = Field()
    latestTransactionDate: Optional[str] = Field()
    sharesOwnedDirectly: Optional[str] = Field()
    positionDirectDate: Optional[str] = Field()
    sharesOwnedIndirectly: Optional[str] = Field()
    positionIndirectDate: Optional[str] = Field()


class InsiderTransaction(Node):
    __label__ = "InsiderTransaction"
    shares: int = Field()
    value: float = Field()
    text: Optional[str] = Field()
    position: Optional[str] = Field()
    transaction: Optional[str] = Field()
    startDate: Optional[str] = Field()
    ownership: Optional[str] = Field()


class Institution(Node):
    __label__ = "Institution"
    name: str = Field(index=True, exists=True, unique=True, db=memgraph)


class MutualFund(Node):
    __label__ = "MutualFund"
    name: str = Field(index=True, exists=True, unique=True, db=memgraph)


class Has_Insider(Relationship):
    __label__ = "Has_Insider"
    __src__ = Ticker
    __dst__ = InsiderHolder


class Created(Relationship):
    __label__ = "Created"
    __src__ = InsiderHolder
    __dst__ = InsiderTransaction


class Purchased(Relationship):
    __label__ = "Purchased"
    __src__ = InsiderTransaction
    __dst__ = Ticker


class Holds_IT(Relationship):
    __label__ = "Holds_IT"
    __src__ = Institution
    __dst__ = Ticker

    shares: int = Field()
    dateReported: str = Field()
    pctHeld: float = Field()
    value: int = Field()


class Holds_MT(Relationship):
    __label__ = "Holds_MT"
    __src__ = MutualFund
    __dst__ = Ticker

    shares: int = Field()
    dateReported: str = Field()
    pctHeld: float = Field()
    value: int = Field()
