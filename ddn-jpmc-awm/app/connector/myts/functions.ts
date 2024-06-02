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
  
  const pct = (num / 100).toLocaleString(undefined, {
    style: 'percent',
    minimumFractionDigits: 2
  });
  
  return pct;
}
