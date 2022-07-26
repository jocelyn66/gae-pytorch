import torch
import torch.nn.modules.loss
import torch.nn.functional as F


def loss_function_gvae(preds, labels, mu, logvar, n_nodes, norm, pos_weight):
    """
    cost:
    - norm: 当标签特别稀疏时，起到平衡作用，这有利于优化稳定/收敛
    - pos_weight: 当标签不平衡时
    KLD: 符合先验分布
    """
    cost = norm * F.binary_cross_entropy_with_logits(preds, labels, pos_weight=pos_weight)

    # see Appendix B from VAE paper:
    # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
    # https://arxiv.org/abs/1312.6114
    # 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD = -0.5 / n_nodes * torch.mean(torch.sum(
        1 + 2 * logvar - mu.pow(2) - logvar.exp().pow(2), 1))
    return cost + KLD


def loss_function_gae(preds, labels, mu, logvar, n_nodes, norm, pos_weight):
    cost = norm * F.binary_cross_entropy_with_logits(preds, labels, pos_weight=pos_weight)
    return cost
