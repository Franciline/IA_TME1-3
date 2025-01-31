import heapq
from collections import deque


def gale_shapley_etud(pref_etud: list[list[int]], pref_parc: list[list[int]], capacites: list[int]) -> list[list[int]]:
    """
    Algorithme de Gale-Shapley (étudiants-optimal).

    Parameters
    ----------
        pref_etud : Matrice des préférences des étudiants.
        pref_parc : Matrice des préférences des parcours.
        capacites : Liste des capacites des parcours
    Returns
    -------
        list[list[int]] : Liste des affectations. Une sous-liste de l'indice i représente l'affectation des étudiants au parcours i.
    """
    ite = 0
    # Les étudiants libres. Les éléments sont des tuples (indice du parcours suivant disponible pour le choix, id_étudiant) changed?
    # Utilisation comme le stack
    etud_libre = deque(range(len(pref_etud)), maxlen=len(pref_etud))  # 1er élément de la pile est étudiant n

    # La liste des propositions
    # Index : etud_id, value : parcours à partir duquel l'étudiant commence à proposer
    etud_parc = [0] * len(pref_etud)

    # La liste des tas pour chaque parcours. Chaque tas stockent des tuples (-rang d'étudiant selon le parcours, id_étudiant)
    parc_affect = [[] for _ in range(len(pref_parc))]

    for i in range(len(parc_affect)):
        heapq.heapify(parc_affect[i])  # création des tas-min

    while (etud_libre):  # continuer tant qu'il existe des étudiants libres
        # print([[stud for _, stud in affect] for affect in parc_affect])
        etudiant = etud_libre.pop()  # dernier etudiant
        parcours = pref_etud[etudiant][etud_parc[etudiant]]   # parcours choisi par lui
        etud_parc[etudiant] += 1     # prochain parcours à proposer

        if parcours == len(pref_parc):  # étudiant a proposé a toutes les parcours
            continue

        rang_etud = pref_parc[parcours].index(etudiant)  # rang d'étudiant dans les préf du parcours O(n)

        # Si parcours n'est pas plein
        if len(parc_affect[parcours]) < capacites[parcours]:
            heapq.heappush(parc_affect[parcours], (-rang_etud, etudiant))
            continue

        # Sinon, parcours est plein, remplacer l'étudiant avec le pire classement (rang max) par l'étudiant libre (s'il est mieux)
        (rang_libere, etud_libere) = min(parc_affect[parcours])  # etudiant le moins préféré

        # (rang_libere, etud_libere) = min(parc_affect[parcours])
        # ? n==1 same as using min(), is it better in complexity?

        if rang_etud < -rang_libere:  # remplacer uniquement si l'étudiant 'etudiant' est mieux
            heapq.heapreplace(parc_affect[parcours], (-rang_etud, etudiant))  # O(log(n))
            etud_libre.append(etud_libere)  # étudiant remplacé placé en tête de pile
        else:
            etud_libre.append(etudiant)  # retourne en tête de pile

        ite += 1

    return [[stud for _, stud in affect] for affect in parc_affect], ite


def gale_shapley_parc(pref_etud: list[list[int]], pref_parc: list[list[int]], capacites: list[int]) -> list[list[int]]:
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
    """

    ite = 0
    # pile des parcours libres, parcours avec capacité > 1 apparaissent plusieurs fois à la suite
    parc_libre = deque([y for y in range(len(capacites)) for _ in range(capacites[y])], maxlen=sum(capacites))

    # La liste des propositions
    # Index : parcours_id, value : étudiant à partir duquel le parcours commence à proposer
    parc_etu = [0] * len(pref_parc)

    # liste de liste pour affectation de chaque étudiant: [numparcours, rangparcours]
    etud_affect = [[] for _ in range(len(pref_etud))]

    while (parc_libre):  # continuer tant qu'il existe des parcours libres
        parcours = parc_libre.pop()  # dernier parcours dans pile
        etudiant = pref_parc[parcours][parc_etu[parcours]]  # etudiant que propose le parcours
        parc_etu[parcours] += 1     # prochain étudiant à proposer

        # parcours a proposé a toutes les étudiant
        if parcours == len(pref_etud):
            continue

        rang_parc = pref_etud[etudiant].index(parcours)  # rang parcours dans les préf de étudiants O(n)

        # Si étudiant libre
        if etud_affect[etudiant] == []:
            etud_affect[etudiant] = [parcours, rang_parc]  # O(1)
            continue

        # sinon si étudiant est pris
        # comparer les deux rangs
        if rang_parc < etud_affect[etudiant][1]:  # [numParcours, rangParcours]
            parc_libre.append(etud_affect[etudiant][0])  # on ajoute le parcours remplacé dans la pile
            etud_affect[etudiant] = [parcours, rang_parc]
        else:
            parc_libre.append(parcours)  # retourne en tête de pile
        ite += 1
    return [[numEt for numEt in range(len(etud_affect)) if etud_affect[numEt][0] == numParc] for numParc in range(len(pref_parc))], ite


def _get_avant(lst: list[int], val: int, exclus: set[int] = None) -> set[int]:
    """
    Trouver tous les éléments dans une list 'lst' qui se trouvent avant l'élément val.
    Ainsi, les éléments qui se trouvent dans l'exclus ne sont pas ajoutés.  
    Hypothèse : tous les éléments de 'lst' sont différents

    Parameters
    ----------
        lst : list[int]
        val: int
        exclus: set[int]

    Returns
    -------
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
