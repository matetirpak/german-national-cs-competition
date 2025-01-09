from copy import deepcopy
from heapq import heapify, heappush, heappop
from random import randint
import time

from structure_utils import *
from result_utils import *
from bin_piece_utils import *

def main():
    while True:
        try:
            path = input("Bitte Geben Sie den Pfad zu Ihrem Ordner ein, z.B.: C:\informatik\\bwinf\ \n")
            while True:
                ans = input("\nSollen alle Standard-Beispiele gelöst werden? Sie müssen vollzählig in den ursprünglichen Namen, paeckchen[0-7].txt, im Ordner enthalten sein. y/n\n")
                if ans != 'n' and ans != 'y':
                    print("Die Antwort muss entweder 'y' für ja oder 'n' für nein lauten. Bitte versuchen Sie es erneut")
                    continue
                if ans == 'y':
                    solve_all_examples(path)
                    exit()
                if ans == 'n':
                    file_name = input("Bitte geben Sie einen Dateinamen ein, z.B.: test0.txt\n")
                    file = path+file_name
                    solve_single_file(file)
                    exit()
        except OSError:
            print("Der Pfad existiert nicht. Bitte versuchen Sie es erneut\n")


def solve_single_file(file):
    '''Löst ein bestimmtes Beispiel mit einer detaillierten Ergebnis-Übersicht'''
    style_combinations, clothes, types_amount, styles_amount = read_file(file)
    result, correct_sol, bins, elapsed_time = solve(style_combinations, clothes, types_amount, styles_amount)
    if not correct_sol:
        print("Die Überprüfung des Ergebnisses ergibt einen Fehler")
        exit()
    else:
        display_result(result, bins, elapsed_time)

def solve_all_examples(dir):
    '''Löst alle Standard-Beispiele'''
    solutions = []
    for i in range(0,8):
        file = dir + f'paeckchen{i}.txt'
        style_combinations, clothes, types_amount, styles_amount = read_file(file)
        result, correct_sol, _, elapsed_time = solve(style_combinations, clothes, types_amount, styles_amount)
        if correct_sol:
            solutions.append((result[-1], elapsed_time))
        else:
            solutions.append(("error", elapsed_time))
    
    for sol in solutions:
        print("wasted pieces / all pieces: ", "{:.4f}".format(sol[0]), end="\t\t")
        print("runtime: ", "{:.2f}".format(sol[1]), "s")


def solve(style_combinations, clothes, types_amount, styles_amount):
    '''Lösungsvorgang eines Beispiels'''
    '''Time Complexity: O(e*n*m*b^2*k*s*o) für e Epochen, n gespeicherte Lösungen pro Epoche, m neue Lösungen pro Ursprung, b Boxen, k Kleidungsstücke einer Box, s Stile und o Stile einer Box 
       Auxiliary Space: O(n*m) für n gespeicherte Lösungen pro Epoche und m neue Lösungen pro Ursprung'''
    start_time = time.time()
    
    # Die Daten werden strukturiert 
    # Erstellen eines Verzeichnisses für mögliche Kombinationen
    style_combinations_dict, style_combinations_matrix = create_combinations_dict_and_matrix(style_combinations, styles_amount)
    # Sortieren der Kleidungsstücke
    style_compatibility_ranking = create_compatibility_ranking(style_combinations_dict, styles_amount)
    clothes_desc_compatibility = sort_clothes(clothes, style_compatibility_ranking, types_amount, styles_amount)
    
    # Einfügen der Kleidungsstücke
    bins = []
    first_fit_decreasing(bins, clothes_desc_compatibility, style_compatibility_ranking, style_combinations_matrix, types_amount)
    # Unvollständige Boxen werden mithilfe überflüssiger Kleidungsstücke aus vollständigen Boxen gefüllt
    fill_wrong_bins(bins, style_combinations_matrix, styles_amount)
    # Falls unvollständige Boxen übrig bleiben, sollen derren Kleidungsstücke entnommen und in bereits vollständige gepackt werden
    insert_pieces_from_wrong_bins(bins, style_compatibility_ranking, style_combinations_matrix, types_amount, styles_amount)

    _, bins=simulated_annealing(bins, 3, 2, 10, style_combinations_matrix, style_compatibility_ranking, types_amount, styles_amount)

    # Füllen unvollständiger Boxen
    fill_wrong_bins(bins, style_combinations_matrix, styles_amount)
    # Vollständige Boxen werden auf möglichst viele kleinere, ebenfalls vollständige Boxen aufgeteilt
    split_bins(bins)
    # Einfügen der Stücke in bereits vollständige Boxen
    insert_pieces_from_wrong_bins(bins, style_compatibility_ranking, style_combinations_matrix, types_amount, styles_amount)
    
    # Auswerten der Lösung
    result = evaluate_bins(bins)
    # Überprüfen der Lösung
    correct_sol = bins_are_correct(bins, clothes, style_combinations_matrix)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return result, correct_sol, bins, elapsed_time


def split_bins(bins):
    '''Jede völlständige Box wird auf möglichst viele kleinere, neue und ebenfalls korrekte Boxen aufgeteilt'''
    '''Time Complexity: O(b*t) für b Boxen und t Typen, Auxiliary Space: O(k) für k entnommene Kleidungsstücke'''
    i = len(bins)-1
    # Jede Box wird einzeln betrachtet, dabei wird von hinten iteriert, sodass neue Boxen hinten angehangen werden können, ohne die Iteration zu stören
    while i >= 0:
        bin = bins[i]
        # Eine Schicht, "layer", liegt vor, wenn von jedem Kleidungsstück 1 vorhanden ist, folglich entspricht die Anzahl Schichten der geringsten Anzahl Stücke eines beliebigen Typen
        layers = min(map(len, bin))
        
        # Jede überflüssige Schicht wird als neue Box am Ende angehängt
        while layers > 1:
            new_bin = []
            for type, _ in enumerate(bin):
                new_bin.append([bin[type].pop()])
            bins.append(new_bin)
            layers-=1
        i -= 1
    return


def insert_pieces_from_wrong_bins(bins, style_compatibility_ranking, style_combinations_matrix, types_amount, styles_amount):
    '''Sammelt alle Kleidungsstücke aus unvollständigen Boxen und fügt diese erneut mit first fit decreasing ein'''
    '''Time Complexity: O(s*t*(k+b)) für s Stile, t Typen, k Kleidungsstücke des Typen und b Boxen, Auxiliary Space: O(n) für n einzufügende Kleidungsstücke'''
    # Es werden alle Kleidungsstücke aus unvollständigen Boxen entfernt
    clothes = collect_wrong_pieces(bins)
    # Die Kleidungsstücke werden erneut eingefügt
    sorted_pieces = sort_clothes(clothes, style_compatibility_ranking, types_amount, styles_amount)
    first_fit_decreasing(bins, sorted_pieces, style_compatibility_ranking, style_combinations_matrix, types_amount)
    return

def collect_wrong_pieces(bins):
    '''Sammelt alle Kleidungsstücke aus unvollständigen Boxen'''
    '''Time Complexity: O(b*k) für b Boxen und k Kleidungsstücke einer Box, Auxiliary Space: O(n) für n entnommene Kleidungsstücke'''
    pieces = []
    i = 0
    # Einzelne Betrachtung aller Boxen
    while i < len(bins):
        bin = bins[i]
        # Box ist unvollständig
        if [] in bin:
            # Iterieren und Speichern aller Kleidungsstücke
            for type, style_list in enumerate(bin):
                for style in style_list:
                    pieces.append([type+1, style, 1])
            # Entfernen der Box
            bins.pop(i)
        else:
            i += 1
    return pieces


def random_solution_swapping(old_bins, probability, style_combinations_matrix, style_compatibility_ranking, types_amount, styles_amount):
    '''Es werden zufällige Tausche zwischen je zwei Kleidungsstücken durchgeführt und anschließend Optimierungen durchgeführt'''
    '''Time Complexity: O(b^2*k*s*n) für b Boxen, k Kleidungsstücke einer Box, s Stile und n Stile einer Box, Auxiliary Space: O(b*k) für Boxen und k Kleidungsstücke der Boxen, aufgrund der deepcopy'''
    bins = deepcopy(old_bins)
    # Alle Boxen werden iteriert
    for bin_i, bin in enumerate(bins):
        # Nur vollständige Boxen werden zunächst für Tausche in Erwägung gezogen, um die Festigkeit derer Elemente zu bekämpfen, da volle Boxen in den meisten anderen Algorithmen unberührt bleiben
        if [] in bin:
            continue
        for type_i, style_list in enumerate(bin):
            for style_i, style in enumerate(style_list):
                # Zufallsgenerator
                if 1 != randint(1,int(1/probability)):
                    continue
                # Für das Kleidungsstück wird ein Tausch angestrebt
                success=False
                comp_styles = compatible_styles_with_bin(bin, style_combinations_matrix, styles_amount)
                
                # Es wird nach einem zweiten Tauschobjekt gesucht
                s_bin_i = bin_i
                while s_bin_i < len(bins)-1:
                    s_bin_i += 1
                    s_bin = bins[s_bin_i]

                    comp_styles_two = compatible_styles_with_bin(s_bin, style_combinations_matrix, styles_amount)
                    if style not in comp_styles_two:
                        continue
                    for s_style_i, s_style in enumerate(s_bin[type_i]):
                        # Kleidungsstücke 
                        if s_style==style:
                            continue
                        if s_style in comp_styles:
                            # Zufallsgenerator
                            if 1 != randint(1,int(1/probability)):
                                continue
                            # Tausch wird durchgeführt
                            success=True
                            break
                    if success:
                        break
                if not success:
                    continue
                # Tausch wird realisiert
                bins[bin_i][type_i][style_i], bins[s_bin_i][type_i][s_style_i]=s_style, style
    
    # Optimierung
    fill_wrong_bins(bins, style_combinations_matrix, styles_amount)
    split_bins(bins)
    fill_wrong_bins(bins, style_combinations_matrix, styles_amount)
    insert_pieces_from_wrong_bins(bins, style_compatibility_ranking, style_combinations_matrix, types_amount, styles_amount)
    return bins


def simulated_annealing(bins, epochs, saved_sols, samples, style_combinations_matrix, style_compatibility_ranking, types_amount, styles_amount):
    '''Durch zufällige Tausche zwischen Kleidungsstücken soll in einem strukturierten Prozess die bestmöglichste Aufstellung der Boxen gefunden werden'''
    '''Time Complexity: O(e*n*m*b^2*k*s*o) für e Epochen, n gespeicherte Lösungen pro Epoche, m neue Lösungen pro Ursprung, b Boxen, k Kleidungsstücke einer Box, s Stile und o Stile einer Box 
       Auxiliary Space: O(n*m*k) für n gespeicherte Lösungen pro Epoche und m neue Lösungen pro Ursprung und k Kleidungsstücke in den Boxen'''
    # Zu Beginn wird der momentane Zustand als bester betrachtet
    cur_bests=[bins]
    # Hier sollen die Lösungen sortiert nach ihrer Qualität gespeichert werden
    solutions=[]
    heapify(solutions)
    # Mit einer ID werden Fehlermeldungen des Heaps vermieden, wenn der Wert übereinstimmt und darauffolgend versucht wird, die Liste zu vergleichen 
    id = 0
    for e in range(epochs):
        # Jedes gespeicherte Ergebnis wird einzeln betrachtet
        for i in range(saved_sols):
            # Erster Zyklus der Funktion kann nur ein Ergebnis beinhalten, überspringen
            if e==0 and i>0:
                break
            # Es werden Stichproblem an dem Ergebnis durchgeführt und im Heap gespeichert
            for _ in range(samples):
                sol = random_solution_swapping(cur_bests[i], 0.15, style_combinations_matrix, style_compatibility_ranking, types_amount, styles_amount)
                _,_,_,_, val = evaluate_bins(sol)
                id+=1
                heappush(solutions, (val, id, sol))
        # Letzte epoch wurde erreicht, bestes Ergebnis wird zurückgegeben
        if e==epochs-1:
            val, _, best=heappop(solutions)
            return val, best
        # Die besten Exemplare sollen aktualisiert werden
        cur_bests = []
        # Heap für den nächsten Zyklus
        new_solutions=[]
        heapify(new_solutions)
        # Die besten Exemplare werden für den nächsten Zyklus gespeichert und zudem in den Heap eingefügt
        for _ in range(saved_sols):
            val, tmp_id, best=heappop(solutions)
            cur_bests.append(best)
            heappush(new_solutions, (val, tmp_id, best))
        # Heap wird überschrieben
        solutions=new_solutions
    
    # Input-Werte sind falsch
    return 1, None


def fill_wrong_bins(bins, style_combinations_matrix, styles_amount, enable_swapping=False):
    '''Unvollständige Boxen werden so weit es geht gefüllt'''
    '''Time Complexity: O(b*k*s) für b Boxen, k als Menge Kleidungsstücke aller Boxen und s kompatible Stile, Auxiliary Space: O(m) für m gesammelte Kleidungsstücke'''
    # Einzelnes Betrachten der Boxen
    for i, bin in enumerate(bins):
        # Box ist vollständig und wird übersprungen
        if [] not in bin:
            continue
        # Es werden fehlende Typen und die kompatiblen Stile mit der Box gepeichert
        missing_types, compatible_styles = missing_elements(bin, style_combinations_matrix, styles_amount)
        # Es werden die fehlenden Kleidungsstücke in anderen Boxen gesucht und dort entnommen
        pieces, success = search_pieces(bins, i, missing_types, compatible_styles, style_combinations_matrix, styles_amount)
        # Die Kleidungsstücke werden in die Box eingefügt
        for piece in pieces:
            insert_piece(bins[i], piece)
    return


def search_pieces(bins, to_be_filled_i, missing_types, compatible_styles, style_combinations_matrix, styles_amount):
    '''Es wird ein passendes Kleidungsstück aus einer beliebigen Box gesucht'''
    '''Time Complexity: O(k*s) für k als Menge Kleidungsstücke aller Boxen und s kompatible Stile, Auxiliary Space: O(m) für m gesammelte Kleidungsstücke'''
    new_styles = []
    pieces = []
    # Jede Box wird durchsucht
    for bin_i, bin in enumerate(bins):
        # Die Box entspricht der, für die die Kleidungsstücke gesucht werden, daher überspringen
        if bin_i == to_be_filled_i:
            continue
        # Die Typen der Box werden nacheinander betrachtet
        for type, style_list in enumerate(bin):
            # Es kann kein passendes Kleidungsstück geben, da entweder der Typ nicht gesucht wird oder die Menge nicht zum Entnehmen ausreicht
            if len(style_list) <=1 or type+1 not in missing_types:
                continue
            # Gesuchtes Kleidungsstück existiert potenziell
            for style_i, style in enumerate(style_list):
                # Keine Kompatibilität mit der Box, für die die Kleidungsstücke gesucht werden, daher überspringen
                if style not in compatible_styles:
                    continue
                # Kleidungsstück ist passend, Entnehmen
                piece_style = style_list.pop(style_i)
                # Entnommenes Stück speichern                
                pieces.append([type+1, piece_style])
                # Gesuchte Elemente aktualisieren
                new_styles.append(piece_style)
                missing_types, compatible_styles = missing_elements(bins[to_be_filled_i], style_combinations_matrix, styles_amount, extra_styles=new_styles)
                break
            if len(missing_types) == len(pieces):
                # es konnten alle fehlenden Kleidungsstücke gefunden werden und diese werden zurückgegeben
                return pieces, True
    # Es konnte nur ein Teil der nötigen fehlenden Kleidungsstücke gefunden werden, diese werden zurückgegeben
    return pieces, False


def first_fit_decreasing(bins, clothes_desc_compatibility, style_compatibility_ranking, style_combinations_matrix, types_amount):
    '''Einfügen der Kleidungsstücke in den erstmöglichen Platz in aufsteigender Reihenfolge der Kompatibilität der Stile'''
    '''Time Complexity: O(s*t*(k+b)) für s Stile, t Typen, k Kleidungsstücke des Typen und b Boxen, Auxiliary Space: O(n) für n Kleidungsstücke'''
    for general_style in style_compatibility_ranking:
        # Einfügen der Kleidungsstücke Stil nach Stil, in der Reihenfolge der Kompatibilität der Stile
        for type, style_list in enumerate(clothes_desc_compatibility):
            # Iterieren der Kleidungsstücke eines Types, solange diese den gesuchten Stil besitzten
            index = 0
            j = 0
            while j < len(style_list):
                style = style_list[j]
                
                if style != general_style:
                    # Stil wurde bereits ausgeschöpft
                    break
                
                # Einfügen des Kleidungsstücks in den erstmöglichen Platz
                piece = [type+1, style]
                while index < len(bins):
                    if is_insertable(bins[index], piece, style_combinations_matrix):
                        break
                    index += 1
                if index == len(bins):
                    # Es muss eine neue Box erstellt werden
                    new_bin = [[]] * (types_amount)
                    bins.append(new_bin)
                # Einfügen
                insert_piece(bins[index], piece)
                j+=1
            clothes_desc_compatibility[type] = clothes_desc_compatibility[type][j:]
    return

if __name__ == '__main__':
    main()
