from copy import deepcopy

def sort_clothes(clothes, style_compatibility_ranking, types_amount, styles_amount):
    '''Sortiert die Kleidung (im noch unveränderten Format der txt-Datei) nach aufsteigender Kompatibilität der Stile mit Berücksichtigung des Typen'''
    '''Time Complexity: O(k) für k Kleidungsstücke, Auxiliary Space: O(k) für k Kleidungsstücke'''
    # Es wird ein Hilfsarray erstellt, die Indexe entsprechen den Kleidungsstilen
    counting_arr = [[]] * (styles_amount+1)
    # Die Kleidungsstücke werden in das Hilfarray einsortiert
    for piece in clothes:
        counting_arr[int(piece[1])] = counting_arr[int(piece[1])] + [piece]
    # Kleidungsstücke werden in der Reihenfolge der Kompatibilität der Stile in eine 2D Liste zusammengefügt. Der Index+1 entspricht dem Typen und der Wert dem Stil
    types_desc_compatibility = [[]] * (types_amount)
    # Folgende Schleife entspricht weiterhin einer Iteration der Kleidungsstücke, O(n), nur mit besonderer Betrachtung ihrer Stile 
    for style in style_compatibility_ranking:
        # Alle Kleidungsstücke des Stiles werden betrachtet
        for piece in counting_arr[style]:
            # In den Index, repräsentativ für den Typen, wird der Stil so oft eingefügt, wie es das Kleidungsstück gibt
            types_desc_compatibility[int(piece[0])-1] = types_desc_compatibility[int(piece[0])-1] + [int(piece[1])] * int(piece[2])

    return types_desc_compatibility


def create_compatibility_ranking(comb_dict, styles_amount):
    '''Erstellt eine Liste mit aufsteigender Kompatibilität der Stile, bzw. Anzahl möglicher Kombinationen mit anderen'''
    '''Time Complexity: O(s^2) für s Stile, Auxiliary Space: O(s) für s Stile'''
    # Es sollen hier die Stile in aufsteigender Kompatibilität eingetragen werden, je mehr Kombinationsmöglichkeiten ein Stil hat, desto kompatibler ist er
    style_compatibility_ranking = []
    # Es wird ein Hilfsarray zum Zählen erstellt
    style_compatibility_counter = [0] * (styles_amount+1)

    # Es wird die Anzahl Kombinationsmöglichkeiten jedes Stils im dem eigenen Index gespeichert
    for key, value in comb_dict.items():
        style_compatibility_counter[key] = len(value)
    # Der Stil mit dem größten Wert wird an den Anfang der leeren Liste gehangen, dann aus dem Hilfsarray entfernt und der Prozess wiederholt
    for _ in range(styles_amount):
        # Index des Maximums ermitteln
        maximum = max(style_compatibility_counter)
        index = style_compatibility_counter.index(maximum)
        # Anfügen des Stils an den Beginn der Lösungsliste und Entfernen im Hilfsarray
        style_compatibility_ranking.insert(0, index)
        style_compatibility_counter[index] = 0
    # Die Kompatibilität liegt in aufsteigender Reihenfolge vor
    return style_compatibility_ranking


def create_combinations_dict_and_matrix(combinations, styles_amount):
    '''Erstellt eine Dictionary, in welcher für jeden Stil alle anderen kombinierbaren gespeichert sind und eine Matrix, die die Kompatibilität zweier Stile als bool beinhaltet'''
    '''Time Complexity: O(s+n) für s Stile und n Kombinationen, Auxiliary Space: O(s^2) für s Stile'''
    comb_dict = dict()
    comb_matrix = [[False] * (styles_amount + 1) for _ in range(styles_amount + 1)]

    # Für jeden Stil wird die Kompatibilität mit sich selbst eingetragen
    for style in range(1, styles_amount+1):
        comb_dict[style] = [style]
        comb_matrix[style][style] = True
    # Jede Kombination wird in die Verzeichnisse beider beteiligter Stile eingetragen
    for comb in combinations:
        # Die beiden kombinierbaren Stile
        style_one = int(comb[0])
        style_two = int(comb[1])
        
        # Eintragen in die Dictionary und Matrix, Berücksichtigung beider Richtungen
        comb_dict[style_one] += [style_two]
        comb_dict[style_two] += [style_one]
        
        comb_matrix[style_one][style_two] = True
        comb_matrix[style_two][style_one] = True

    return comb_dict, comb_matrix


def read_file(file):
    '''Liest eine Datei ein'''
    '''Time Complexity: O(n) für n Zeilen des Dokuments, Auxiliary Space: O(n) für n Zeilen des Dokuments'''
    data = [line.split() for line in open(file, 'r')]
    # Es wird der Absatz zwischen den Kombinationen und den Kleidungsstücken gesucht
    for i, v in enumerate(data):
        if len(v) == 0:
            break
    # Trennen dieser, Weiterverarbeitung folgt in weiteren Funktionen
    combinations = data[1:i]
    clothes = data[i+1:]
    # Leere Kleidungsstück-Listen entstehen bei Leerzeichen am Ende der txt-Datei, diese werden entfernt
    i = len(clothes)-1
    while len(clothes[i]) == 0:
        i -= 1
    clothes = clothes[:i+1]
    # Auslesen der Anzahl Typen und Stile
    types_amount = int(data[0][0])
    styles_amount = int(data[0][1])
    return combinations, clothes, types_amount, styles_amount