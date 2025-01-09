from termcolor import colored

from bin_piece_utils import *

def evaluate_bins(bins):
    '''Wertet das Ergebnis aus'''
    '''Time Complexity: O(b*m) für b Boxen und m Typen, Auxiliary Space: O(1)'''
    correct_bins = 0
    used_pieces = 0
    wasted_pieces = 0
    for bin in bins:
        if [] not in bin:
            correct_bins += 1
            used_pieces += sum(map(len, bin))
        else:
            wasted_pieces += sum(map(len, bin))
    
    incorrect_bins = len(bins)-correct_bins
    return (correct_bins, incorrect_bins, used_pieces, wasted_pieces, wasted_pieces/(used_pieces+wasted_pieces))


def display_result(result, bins, runtime):
    '''Gibt das Ergebnis aus'''
    correct_bins, incorrect_bins, used_pieces, wasted_pieces, waste_ratio = result
    print("------------------")
    print("Korrekte Boxen:", correct_bins)
    print("Inkorrekte Boxen:", incorrect_bins)
    print("Verpackte Kleidungsstücke:", used_pieces)
    print(colored("Übrige Kleidungsstücke:", "red"), wasted_pieces)
    print(colored("Übrige / alle Kleidungsstücke:", "red"), "%.4f" % waste_ratio)
    print("Laufzeit: ", "{:.2f}".format(runtime), "s")
    print("------------------")
    print("Boxen:")
    print("Eine Zeile entspricht einer Box, die wie folgt aufgebaut ist, S entspricht einem beliebigen Stil: [Typ 1:[S, S, S], Typ 2:[S, S, S], ..., Typ n:[S, S, S]]")
    print("\nMuster: Box N: Typ X: [Stil 1, Stil 2, Stil 3]\n")
    for i, bin in enumerate(bins):
        print(f"Box {i+1}: ", end="\t")
        for j, type_list in enumerate(bin):
            print(f"Typ {j+1}:", type_list, end="   ")
        print()


def bins_are_correct(bins, clothes, style_combinations_matrix):
    '''Überprüft, ob das Ergebnis korrekt ist'''
    '''Time Complexity: O(b*s^2) für b Boxen und s Stile einer Box, Auxiliary Space: O(s) für s Stile einer Box'''
    # Überprüft die Menge der Kleidungsstücke
    for data in clothes:
        type, style, amount = data
        type, style, amount = int(type), int(style), int(amount)
        
        cnt = 0
        for bin in bins:
            for c_style in bin[type-1]:
                if c_style == style:
                    cnt+=1
        if cnt != amount:
            print('amount of clothes incorrect')
            return False
    # Überprüft die Kompatibilität der Stile der Boxen
    for bin in bins:
        bin_styles = styles_in_bin(bin)
        i = 0
        while i < len(bin_styles):
            style = bin_styles[i]
            j = i + 1
            while j < len(bin_styles):
                if not style_combinations_matrix[bin_styles[j]][style]:
                    print('style incompatibility error')
                    print(bins)
                    print('----')
                    print(bin)
                    return False
                j += 1
            i += 1
    return True