def metadata_retrieval_score(
    match_conditions,   # list of str, e.g., ['=', '>', '<=']
    join_conditions,    # list of str, e.g., ['and', 'or']
    no_of_results,      # int
    max_possible_docs   # int
):
    MATCH_CONDITIONS = {'=': 1, '>': 0.7, '<': 0.7, '>=': 0.7, '<=': 0.7, '!=': 0.7}
    JOIN_CONDITIONS = {"between": 0.1, "in": 0, "and": 0, "or": 0.05}

    # Compute condition score
    condition_count = len(match_conditions)
    if condition_count == 0:
        return 0.0
    
    condition_score = sum(MATCH_CONDITIONS.get(cond, 0) for cond in match_conditions)
    avg_condition_score = condition_score / condition_count

    # Compute join penalty
    join_penalty = sum(JOIN_CONDITIONS.get(j, 0) for j in join_conditions)

    # Base score
    base_score = avg_condition_score - join_penalty

    # Results penalty
    if no_of_results == 1:
        results_penalty = 0.0
    elif 2 <= no_of_results <= max_possible_docs:
        results_penalty = 0.05
    elif no_of_results > max_possible_docs:
        overage = no_of_results - max_possible_docs
        proportional_penalty = 0.05 + min(0.95, (overage / max_possible_docs) * 0.45)
        results_penalty = proportional_penalty
    else:
        results_penalty = 0.0  # shouldn't happen

    # Final score, clamped to [0, 1]
    final_score = max(0.0, min(1.0, base_score - results_penalty))
    return final_score
