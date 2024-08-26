import torch

def compute_all_w_m(sizes, alphas):
    """
    Compute w_m(α) for each dataset using PyTorch.

    Parameters:
    sizes (list or tensor): The sizes of the datasets [|s_1|, |s_2|, ..., |s_M|].
    alphas (list or tensor): The weights corresponding to each dataset [α_1, α_2, ..., α_M].

    Returns:
    list: A list of computed values of w_m(α) for each m.
    """
    # Convert inputs to PyTorch tensors if they are not already
    if not isinstance(sizes, torch.Tensor):
        sizes = torch.tensor(sizes, dtype=torch.float32)
    if not isinstance(alphas, torch.Tensor):
        alphas = torch.tensor(alphas, dtype=torch.float32)

    if sizes.size(0) != alphas.size(0):
        raise ValueError("Sizes and alphas must have the same length.")

    # Compute the denominator once
    denominator = torch.sum(alphas * sizes)

    # Compute w_m(α) for each m
    w_m_alpha_values = [(alphas[m] * sizes[m]) / denominator for m in range(len(sizes))]

    return w_m_alpha_values


# Example usage
sizes = [100, 200, 300]  # Sizes of the datasets |s_1|, |s_2|, |s_3|
alphas = [0.1, 0.2, 0.7]  # Weights α_1, α_2, α_3

w_m_alpha_values = compute_all_w_m(sizes, alphas)
for m, w_m_alpha in enumerate(w_m_alpha_values, start=1):
    print(f"w_{m}(α) =", w_m_alpha)