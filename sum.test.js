const sum = require('./sum');

test('dodaje 1 + 2 i zwraca wynik 3', () => {
  expect(sum(1, 2)).toBe(3);
});

test('poprawnie dodaje liczby ujemne', () => {
  expect(sum(-1, -5)).toBe(-6);
});