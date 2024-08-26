import numpy as np


def compute_all_w_m(sizes, alphas):
    """
    Compute w_m(α) for each dataset.

    Parameters:
    sizes (list or numpy array): The sizes of the datasets [|s_1|, |s_2|, ..., |s_M|].
    alphas (list or numpy array): The weights corresponding to each dataset [α_1, α_2, ..., α_M].

    Returns:
    list: A list of computed values of w_m(α) for each m.
    """
    if len(sizes) != len(alphas):
        raise ValueError("Sizes and alphas must have the same length.")

    # Compute the denominator once
    denominator = np.sum(np.multiply(alphas, sizes))

    # Compute w_m(α) for each m
    w_m_alpha_values = [(alphas[m] * sizes[m]) /
                        denominator for m in range(len(sizes))]

    return w_m_alpha_values


# Example usage
sizes = [100, 200, 300]  # Sizes of the datasets |s_1|, |s_2|, |s_3|
alphas = [0.5, 1.5, 1.0]  # Weights α_1, α_2, α_3

w_m_alpha_values = compute_all_w_m(sizes, alphas)
for m, w_m_alpha in enumerate(w_m_alpha_values, start=1):
    print(f"w_{m}(α) =", w_m_alpha)


