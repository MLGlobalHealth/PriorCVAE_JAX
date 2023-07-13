"""
Test the loss functions.
"""
import random
import jax
import numpy as np
import jax.numpy as jnp

from priorCVAE.losses import kl_divergence, scaled_sum_squared_loss, mean_squared_loss


def test_kl_divergence(dimension):
    """Test KL divergence between a Gaussian N(m, S) and a unit Gaussian N(0, I)"""
    key = jax.random.PRNGKey(random.randint(a=0, b=999))
    m = jax.random.uniform(key=key, shape=(dimension, ), minval=0.1, maxval=4.)
    log_S = jax.random.uniform(key=key, shape=(dimension,), minval=0.1, maxval=.9)

    kl_value = kl_divergence(m, log_S)

    expected_kl_value = -0.5 * (1 + log_S - jnp.exp(log_S) - jnp.square(m))
    expected_kl_value = jnp.sum(expected_kl_value)

    np.testing.assert_array_almost_equal(kl_value, expected_kl_value, decimal=6)


def test_scaled_sum_squared_loss(num_data, dimension):
    """Test scaled sum squared loss."""
    key = jax.random.PRNGKey(random.randint(a=0, b=999))
    y = jax.random.uniform(key=key, shape=(num_data, dimension), minval=0.1, maxval=4.)
    key, _ = jax.random.split(key)
    y_reconstruction = jax.random.uniform(key=key, shape=(num_data, dimension), minval=0.1, maxval=4.)
    vae_variance = jax.random.normal(key=key).item()

    vae_loss_val = scaled_sum_squared_loss(y, y_reconstruction, vae_variance)
    expected_val = jnp.sum(0.5 * (y - y_reconstruction)**2/vae_variance)

    np.testing.assert_array_almost_equal(vae_loss_val, expected_val, decimal=6)


def test_mean_squared_loss(num_data, dimension):
    """Test mean squared loss."""
    key = jax.random.PRNGKey(random.randint(a=0, b=999))
    y = jax.random.uniform(key=key, shape=(num_data, dimension), minval=0.1, maxval=4.)
    key, _ = jax.random.split(key)
    y_reconstruction = jax.random.uniform(key=key, shape=(num_data, dimension), minval=0.1, maxval=4.)
    vae_variance = jax.random.normal(key=key).item()

    vae_loss_val = mean_squared_loss(y, y_reconstruction, vae_variance)
    expected_val = jnp.mean((y_reconstruction - y)**2/vae_variance)

    np.testing.assert_array_almost_equal(vae_loss_val, expected_val, decimal=6)