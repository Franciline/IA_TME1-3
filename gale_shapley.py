import heapq
from collections import deque


def gale_shapley_etud(pref_etud, pref_uni, capacites):
    """
    Algorithme de Gale-Shapley (étudiants-optimal).

    Parameters
    ----------
        pref_etud : Matrice des préférences des étudiants.
        pref_uni : Matrice des préférences de l'université.
        capacites : Liste des capacites des parcours
    Returns
    -------
        list[list[int]] : Liste des affectations. Une sous-liste de l'indice i représente l'affectation des étudiants au parcours i.
    """

    # Les étudiants libres. Les éléments sont des tuples (indice du parcours suivant disponible pour le choix, id_étudiant)
    # Utilisation comme le stack
    etud_libre = deque(range(len(pref_etud)), maxlen=len(pref_etud))

    # Index : etud_id, value : parcours à partir duquel l'étudiant peut commencer de choisir
    etud_parc = [0] * len(pref_etud)
    # La liste des tas pour chaque parcours. Chaque tas stockent des tuples (-rang d'étudiant selon le parcours, id_étudiant)
    parc_affect = [[] for _ in range(len(pref_uni))]

    for i in range(len(parc_affect)):
        heapq.heapify(parc_affect[i])  # create heaps

    while (etud_libre):  # continuer tant qu'il existe des étudiants libres
        etud = etud_libre.pop()  # dernier etudiant
        parc = etud_parc[etud]   # parcours choisi par lui
        etud_parc[etud] += 1

        if parc == len(pref_uni):  # étudiant a proposé a toutes les unis
            continue

        rang_etud = pref_uni[parc].index(etud)  # rang d'étudiant O(n)

        if len(parc_affect[parc]) < capacites[parc]:  # parcours n'est pas plein
            heapq.heappush(parc_affect[parc], (-rang_etud, etud))
            continue

        # Sinon, parcours est plein, remplacer l'étudiant avec le pire classement (rang max) par l'étudiant libre (s'il est mieux)
        (rang_libere, etud_libere) = heapq.nsmallest(1, parc_affect[parc])[0]  # etud avec le pire classement

        if rang_etud < -rang_libere:  # remplacer uniquement si l'étudiant 'etud' est mieux
            heapq.heapreplace(parc_affect[parc], (-rang_etud, etud))  # O(log(n))
            etud_libre.append(etud_libere)  # étudiant remplacé
        else:
            etud_libre.append(etud)

    return [[stud for _, stud in affect] for affect in parc_affect]
