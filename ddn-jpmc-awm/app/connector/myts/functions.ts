/**
 * @readonly Exposes the function as an NDC function (the function should only query data without making modifications)
 */
export function hello(name?: string) {
  return `hello ${name ?? "world"}`;
}


/**
 * @readonly Formats a number as a percentage
 */
export function formatPercentage(num?: number): string {
  // let pct = `${num}% lol`
  if (typeof num !== 'number' || isNaN(num)) {
    return `${num} is not valid input.  Only numbers can be formatted to a percentage`;  // Returns '0.00%' if input is undefined, null, or not a number
  }
  
  const pct = num.toLocaleString(undefined, {
    style: 'percent',
    minimumFractionDigits: 2
  });
  
  return pct;
}



/**
 * @readonly Calculates the total of all transactions' baseGrossAmount
 */
export function processTransactionsTotal(transactions: Transaction[]): number {
  const initialValue = 0;
  const sumWithInitial = transactions.reduce(
    (accumulator, currentValue) => accumulator + currentValue.baseGrossAmount,
    initialValue,
  );
  return sumWithInitial;
}




/**
 * @readonly Formats a number as a percentage
 */
export function processPositions(positions: Position[]): number {
  return 42
}

export interface Transaction {
  baseGrossAmount: number;
  accountNumber:   string;
  instrumentCode:  string;
}
export interface Position {
  accountBaseCurrency:          string;
  accountNumber:                string;
  baseAdjustedCostAmount:       number;
  baseExpectedIncomeAmount:     number;
  baseMarketPrice:              number;
  baseSettledMarketValueAmount: number;
  baseTradedMarketValueAmount:  number;
  companyName:                  {
    raw: string;
  }[];
  instrumentCode:               string;
}
