# config.py

# A dictionary mapping specific Moroccan cities to their known CINE prefixes.
prefixes = {
    # Major Economic Hubs
    'Rabat': ['A'],
    'Casablanca': ['B', 'BE', 'BH', 'BJ', 'BK'],
    'Tanger': ['E', 'I'],
    'Fès': ['D', 'G'],
    'Meknès': ['F'],

    # Other Large Cities
    'Agadir': ['J'],
    'Oujda': ['L'],
    'Tétouan': ['M'],
    'Béni Mellal': ['V'],
    'El Jadida': ['P'],
    'Nador': ['N'],

    # Southern and Other Cities
    'Laâyoune': ['X'],
    'Ouarzazate': ['Z'],
    'Berkane': ['L'],
    'Benslimane': ['W'],
    'Fkih Ben Salah': ['V'],

    # A fallback for any city not explicitly listed
    'default': ['XX']
}