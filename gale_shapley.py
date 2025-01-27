import heapq
from collections import deque
from itertools import product


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

    return [[stud for _, stud in affect] for affect in parc_affect]


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

    return [[numEt for numEt in range(len(etud_affect)) if etud_affect[numEt][0] == numParc] for numParc in range(len(pref_parc))]


def get_instable(pref_etud: list[list[int]], pref_parc: list[list[int]], affect_parc: list[list[int]]) -> list[list[int]]:
    """
    Trouver les paires instables.
    """
    pref_des_etud = [set() for _ in range(len(pref_etud))]
    pref_des_parc = [set() for _ in range(len(pref_parc))]

    instables = set()
    for parc, affect in enumerate(affect_parc):
        for etud in affect:
            pref_du_parc = set(pref_parc[parc][:pref_parc[parc].index(etud)]) - set(affect_parc[parc])
            pref_du_etud = set(pref_etud[etud][:pref_etud[etud].index(parc)])
            pref_des_etud[etud] = pref_du_etud
            pref_des_parc[parc] = pref_du_parc

    print(pref_des_etud)
    for parc, pref_parc in enumerate(pref_des_parc):
        pe = [pref_des_etud[etud] if etud in pref_parc else set() for etud in range(len(pref_etud))]
        check = next((i for i, s in enumerate(pe) if parc in s), -1)
        if check != -1:
            print(check, parc)
