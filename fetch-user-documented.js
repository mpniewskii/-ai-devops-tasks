/**
 * Obiekt reprezentujący przetworzone dane użytkownika.
 * @typedef {Object} UserData
 * @property {string} name - Imię i nazwisko użytkownika.
 * @property {string} email - Adres e-mail użytkownika.
 * @property {Date} lastLogin - Data ostatniego logowania jako obiekt Date.
 */

/**
 * Pobiera dane użytkownika z zewnętrznego API na podstawie jego identyfikatora.
 *
 * @param {string|number} userId - Unikalny identyfikator użytkownika.
 * @returns {Promise<UserData|null>} Obietnica zwracająca obiekt z danymi użytkownika lub `null` w przypadku błędu.
 * @throws {Error} Wyrzuca błąd, gdy odpowiedź HTTP jest nieprawidłowa (obsługiwany wewnętrznie przez blok catch).
 */
function fetchUserData(userId) {
  return fetch(`https://api.example.com/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return {
        name: data.name,
        email: data.email,
        lastLogin: new Date(data.lastLoginTimestamp)
      };
    })
    .catch(error => {
      console.error('Fetch error:', error);
      return null;
    });
}