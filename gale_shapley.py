import heapq
from typing import Tuple
from collections import deque


def gale_shapley_etud(pref_etud: list[list[int]], pref_parc: list[list[int]], capacites: list[int]) -> Tuple[list[list[int]], int]:
    """
    Algorithme de Gale-Shapley (étudiants-optimal).

    Parameters
    ----------
        pref_etud : Matrice des préférences des étudiants.
        pref_parc : Matrice des préférences des parcours.
        capacites : Liste des capacites des parcours
        
    Returns
    -------
        list[list[int]] : Liste des affectations. Une sous-liste d'indice i représente l'affectation des étudiants au parcours i
        ite: int, nombre d'itérations de l'appel
    """

    ite = 0
    # Pile des étudiants libres représentés par leur numéros
    etud_libre = deque(range(len(pref_etud)), maxlen=len(pref_etud))  # 1er élément de la pile est l'étudiant n

    # Liste des propositions: etud_parc[i] = indice du parcours dans les préférences à partir duquel l'étudiant i commence à proposer
    etud_parc = [0] * len(pref_etud)

    # Liste des tas pour chaque parcours. Chaque tas stocke des tuples (-rang d'étudiant dans le parcours, id_étudiant)
    parc_affect = [[] for _ in range(len(pref_parc))] # parc_affect[i] contient le tas du parcours i

    for i in range(len(parc_affect)):
        heapq.heapify(parc_affect[i])  # création des tas-min

    while (etud_libre): # tant qu'il existe des étudiants libres
        
        etudiant = etud_libre.pop()                             # dernier etudiant
        parcours = pref_etud[etudiant][etud_parc[etudiant]]     # parcours choisi par lui
        etud_parc[etudiant] += 1                                # prochain parcours à proposer

        if parcours == len(pref_parc):  # étudiant a proposé a tous les parcours
            continue

        rang_etud = pref_parc[parcours].index(etudiant)  # rang d'étudiant dans les préf du parcours O(n)

        # Si parcours n'est pas plein
        if len(parc_affect[parcours]) < capacites[parcours]:
            heapq.heappush(parc_affect[parcours], (-rang_etud, etudiant))
            continue

        # Sinon, parcours est plein, remplacer l'étudiant affecté avec le pire classement (rang max) par l'étudiant libre (s'il est mieux)
        (rang_libere, etud_libere) = min(parc_affect[parcours])                 # etudiant le moins préféré

        if rang_etud < -rang_libere:                                            # remplacer uniquement si l'étudiant 'etudiant' est mieux
            heapq.heapreplace(parc_affect[parcours], (-rang_etud, etudiant))    # O(log(n))
            etud_libre.append(etud_libere)                                      # l'étudiant remplacé est placé en tête de pile
        else:
            etud_libre.append(etudiant)                                         # retourne en tête de pile

        ite += 1

    return [[stud for _, stud in affect] for affect in parc_affect], ite


def gale_shapley_parc(pref_etud: list[list[int]], pref_parc: list[list[int]], capacites: list[int]) -> Tuple[list[list[int]], int]:
    """
    Algorithme de Gale-Shapley (parcours-optimal).

    Parameters
    ----------
        pref_etud : Matrice des préférences des étudiants.
        pref_parc : Matrice des préférences des parcours.
        capacites : Liste des capacites des parcours
    Returns
    -------
        list[list[int]] : Liste des affectations. Une sous-liste de l'indice i représente l'affectation des étudiants au parcours i.
        ite: int, nombre d'itérations de l'appel
    """

    ite = 0
    # Pile des parcours libres, parcours avec capacité > 1 apparaissent autant de fois à la suite que nb capacité
    parc_libre = deque([y for y in range(len(capacites)) for _ in range(capacites[y])], maxlen=sum(capacites))

    # La liste des propositions: parc_etu[i] = indice de l'étudiant dans les préférences à partir duquel le parcours i commence à proposer
    parc_etu = [0] * len(pref_parc)

    # L'iste d'affectation de chaque étudiant: [numparcours, rangparcours]
    etud_affect = [[] for _ in range(len(pref_etud))]

    while (parc_libre):  # tant qu'il existe des parcours libres
        parcours = parc_libre.pop()                         # dernier parcours dans pile
        etudiant = pref_parc[parcours][parc_etu[parcours]]  # etudiant que propose le parcours
        parc_etu[parcours] += 1                             # prochain étudiant à proposer

        # parcours a proposé a toutes les étudiant
        if parcours == len(pref_etud):
            continue

        rang_parc = pref_etud[etudiant].index(parcours)     # rang parcours dans les préf de étudiants O(n)

        # Si étudiant libre
        if etud_affect[etudiant] == []:
            etud_affect[etudiant] = [parcours, rang_parc]   # O(1)
            continue

        # sinon si étudiant est pris, comparer les deux rangs
        if rang_parc < etud_affect[etudiant][1]:            # [numParcours, rangParcours]
            parc_libre.append(etud_affect[etudiant][0])     # on ajoute le parcours remplacé dans la pile
            etud_affect[etudiant] = [parcours, rang_parc]
        else:
            parc_libre.append(parcours)                     # retourne en tête de pile
        ite += 1

    return [[numEt for numEt in range(len(etud_affect)) if etud_affect[numEt][0] == numParc] for numParc in range(len(pref_parc))], ite


def _get_avant(lst: list[int], val: int, exclus: set[int] = None) -> set[int]:
    """
    Trouve tous les éléments dans la liste 'lst' qui se trouvent avant l'élément val et 
    qui ne se trouve pas dans l'ensemble exclus.
    Utilisé pour récupérer des étudiants/parcours préférés par rapport à val, celui affecté.

    Hypothèse : tous les éléments de 'lst' sont différents

    Parameters
    ----------
        lst : list[int] liste d'éléments à parcourir
        val: int valeur où arrêter le parcours
        exclus: set[int] ensemble de valeurs à ne pas prendre en compte

    Returns
    -------
        res: ensemble d'éléments recherchés
    """
    res = set()
    for elem in lst:
        if val == elem:
            break
        if (exclus is None) or (elem not in exclus):
            res.add(elem)
    return res


def get_instable(pref_etud: list[list[int]], pref_parc: list[list[int]], affect_parc: list[list[int]]) -> list[list[int]]:
    """
    Trouver les paires instables.

    Parameters
    ----------
        pref_etud : list[list[int]]
            Matrice des préférences des étudiants.
        pref_parc : list[list[int]]
            Matrice des préférences des parcours de l'université.
        affect_parc : list[list[int]] 
            Une liste des affectations des étudiants aux parcours. La liste à l'indice i représente l'affectation au parcours i.

    Returns
    -------
        instables: la liste des paires instables
    """

    pref_des_etud = [set() for _ in range(len(pref_etud))]
    pref_des_parc = [set() for _ in range(len(pref_parc))]

    instables = set()  # Un ensemble des paires (parcours, etudiant) unstable
    for parc, affect in enumerate(affect_parc):
        for etud in affect:
            # Les etudiants plus préférés par des parcours que ceux ont été affectés
            pref_des_parc[parc] = _get_avant(pref_parc[parc], etud, set(affect_parc[parc]))
            # Les parcours plus préférés par des étudiant que celui à qui il a été affecté
            pref_des_etud[etud] = _get_avant(pref_etud[etud], parc)

    for parc, pref_parc in enumerate(pref_des_parc):
        # pref_parc : les étudiants préférés par le parcours parc
        for etud in pref_parc:
            if (parc in pref_des_etud[etud]):  # si l'étudiant aussi préfére le parcours parc -> instable
                instables.add((parc, etud))

    return instables
