from copy import copy

def styles_in_bin(bin):
    '''Ermittelt alle Stile innerhalb einer Box'''
    '''Time Complexity: O(k) für k Kleidungsstücke der Box, Auxiliary Space: O(s) für s Stile der Box'''
    # Nur einzigartige Einträge werden zugelassen
    styles = set()
    # Iterieren und Speichern aller Stile
    for style_list in bin:
        for style in style_list:
            styles.add(style)
    # Zurückgeben als Liste anstatt eines Sets
    return list(styles)


def compatible_styles_with_bin(bin, style_combinations_matrix, styles_amount, extra_styles = []):
    '''Ermittelt alle Stile kombinierbar mit einer Box in O(n*m*k) für n Stile der Box, m Stile die momentan noch zur Auswahl stehen und k kompatible Stile mit der Box'''
    '''Time Complexity: O(n*s) für n Stile der Box und s als Menge aller Stile, Auxiliary Space: O(s) für s als Menge aller Stile'''
    # Alle möglichen Stile
    all_compatible_styles = [x for x in range(1,styles_amount+1)]
    # Alle momentanen Stile
    bin_styles = styles_in_bin(bin) + extra_styles
    
    # Iterieren aller Stile der Box
    for style in bin_styles:
        i = 0
        while i < len(all_compatible_styles):
            # Jeder Stil der nicht mit dem momentan betrachteten kombinierbar ist, wird entfernt
            if not style_combinations_matrix[all_compatible_styles[i]][style]:
                all_compatible_styles.pop(i)
            else:
                i += 1
    # Übrig gebliebene Stile sind kompatibel und werden zurückgegeben
    return all_compatible_styles


def missing_elements(bin, style_combinations_matrix, styles_amount, extra_styles = []):
    '''Ermittelt alle fehlenden Typen einer Box, eingeschlossen der kompatiblen Stile in O(n*m*k) für die Funktion compatible_styles_with_bin'''
    '''Time Complexity: O(n*s) für n Stile der Box und s als Menge aller Stile, Auxiliary Space: O(s+t) für s Stile und t Typen'''
    # Kompatible Stile werden ermittelt
    compatible_styles = compatible_styles_with_bin(bin, style_combinations_matrix, styles_amount, extra_styles=extra_styles)
    # Fehlende Typen werden ermittelt
    types = []
    for i, style_list in enumerate(bin):
        if len(style_list) == 0:
            types.append(i+1)
    return types, compatible_styles


def is_insertable(bin, piece, style_combinations_matrix):
    '''Überprüft, ob ein Kleidungsstück in eine Box passt in O(n*m) für n Stile der Box und m für das Suchen des Stils in einer Kombinationsliste'''
    '''Time Complexity: O(k) für k Kleidungsstücke der Box, Auxiliary Space: O(s) für s Stile der Box'''
    piece_type, piece_style = piece
    # Überprüft, ob die Box noch Platz für den Typen bietet
    if len(bin[piece_type-1]) >= 3:
        return False
    # Untersucht, ob der Stil mit allen anderen der Box kombinierbar ist
    styles_bin = styles_in_bin(bin)
    for style in styles_bin:
        if not style_combinations_matrix[style][piece_style]:
            return False
    return True


def insert_piece(bin, piece):
    '''Fügt ein Kleidungsstück in-place in eine Box ein'''
    '''Time Complexity: O(1), Auxiliary Space: O(1)'''
    piece_type, piece_style = piece
    bin[piece_type-1] = bin[piece_type-1] + [piece_style]