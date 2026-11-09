const ipv4Pattern = /^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$/;

/**
 * Sprawdza, czy podany tekst ma poprawny format adresu IPv4.
 *
 * @param {string} address - Adres IP do sprawdzenia.
 * @returns {boolean} `true`, jeśli adres jest poprawnym adresem IPv4.
 */
function isValidIPv4(address) {
  return typeof address === 'string' && ipv4Pattern.test(address);
}

module.exports = isValidIPv4;
