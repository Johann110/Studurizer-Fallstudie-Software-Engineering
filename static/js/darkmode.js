// Dark Mode Toggle Funktionalität
document.addEventListener('DOMContentLoaded', function() {
    // Local Storage Key
    const DARK_MODE_KEY = 'studurizer_darkmode';

    // Dark Mode Toggle Button Referenz
    const toggleSwitch = document.getElementById('darkModeToggle');

    // Dark Mode Status prüfen
    const currentTheme = localStorage.getItem(DARK_MODE_KEY);

    // Dark Mode Präferenzen des Systems prüfen
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Initialisieren des Themes
    if (currentTheme) {
        // Gespeichertes Theme verwenden
        document.documentElement.setAttribute('data-theme', currentTheme);

        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
    } else if (prefersDarkScheme.matches) {
        // System-Präferenz für Dark Mode verwenden
        document.documentElement.setAttribute('data-theme', 'dark');
        toggleSwitch.checked = true;
        localStorage.setItem(DARK_MODE_KEY, 'dark');
    }

    // Event Listener für Toggle-Button
    toggleSwitch.addEventListener('change', switchTheme);

    // Dark Mode System-Präferenz Änderung
    prefersDarkScheme.addEventListener('change', (e) => {
        if (!localStorage.getItem(DARK_MODE_KEY)) {
            if (e.matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
                toggleSwitch.checked = true;
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                toggleSwitch.checked = false;
            }
        }
    });

    // Theme-Umschaltfunktion
    function switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem(DARK_MODE_KEY, 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem(DARK_MODE_KEY, 'light');
        }
    }
});