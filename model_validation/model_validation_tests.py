import jax.numpy as jnp

from model_validation.utils import generate_vae_samples
from priorCVAE.diagnostics import mean_bootstrap_interval


def mean_bootstrap_interval_contains_zero(key, decoder_params, decoder, latent_dim, num_samples=10000):
    samples = generate_vae_samples(key, decoder_params, decoder, num_samples, latent_dim)
    ci_lower, ci_upper = mean_bootstrap_interval(samples)
    zero_in_interval = (ci_lower <= 0) & (0 <= ci_upper)
    num_valid = jnp.where(zero_in_interval)[0].shape[0]

    return num_valid == samples.shape[1]


