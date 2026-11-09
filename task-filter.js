/**
 * Filtruje zadania zakończone, sortuje je według ID i zwraca samą listę tytułów.
 *
 * @param {Array<{id: number, title: string, status: string}>} tasks - Tablica obiektów zadań.
 * @returns {Array<string>} Tablica tytułów zakończonych zadań posortowanych rosnąco po ID.
 */
function getCompletedTaskTitles(tasks) {
  if (!Array.isArray(tasks)) {
    return [];
  }

  return tasks
    .filter(task => task.status === 'completed')
    .sort((a, b) => a.id - b.id)
    .map(task => task.title);
}

module.exports = getCompletedTaskTitles;