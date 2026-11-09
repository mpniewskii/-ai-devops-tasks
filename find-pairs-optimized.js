function findPairs(arr, targetSum) {
  const pairs = [];
  const seenValues = new Map();

  for (const value of arr) {
    const complement = targetSum - value;
    const matchingValues = seenValues.get(complement) || 0;

    for (let i = 0; i < matchingValues; i++) {
      pairs.push([complement, value]);
    }

    seenValues.set(value, (seenValues.get(value) || 0) + 1);
  }

  return pairs;
}

module.exports = findPairs;
