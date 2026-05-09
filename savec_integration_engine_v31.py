#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAVEC Integration Engine
========================

Statistical Architecture for Validated Ethical Curation (SAVEC)
Layer 1 (Validation Foundation) + Layer 2 (Governance Engine).

This module implements:

  LAYER 1 — Statistical Validation Foundation
  --------------------------------------------
  OPTIMISATION 1 — Log-Bayes Factor (Savage-Dickey on log scale)
    Numerically stable BF computation via scipy.stats.beta.logpdf.
    Prevents floating-point overflow for n > 1 000.

  OPTIMISATION 2 — Vectorised Jackknife Sensitivity Analysis
    Matrix-based CV via NumPy broadcasting.
    Typical speedup: 50-100x over loop-based equivalent.

  OPTIMISATION 3 — Holm-Bonferroni Step-Down Correction
    Uniformly more powerful than classical Bonferroni while maintaining
    strong FWER control (Holm, 1979).

  INTEGRATION — CodeCarbon + Dynamic RVI
    Real-time carbon tracking with graceful TDP fallback.
    Geographic-adaptive water intensity (Li et al., 2023).

  LAYER 2 — Governance Engine
  ----------------------------
  GovernanceResolver
    Conflict resolution across multiple community/institutional
    authorities. Pessimistic default (Axiom 2): max() on AccessLevel,
    all() on can_export, any() on manual_audit.
    SHA-256 immutable audit trail (Req. 2.2).

  ContextualRVI
    Sensitivity-tier-aware RVI threshold modulation.
    Ethical Justification multiplier J tightens the threshold for
    higher-sensitivity items. J can never loosen it (asymmetry
    constraint). Log-scale relaxation for large corpora (n > 10 000).

  EpistemicBridgeResult + resolve_layer1_to_layer2()
    Structured Layer 1 -> Layer 2 hand-off. Combined confidence score
    capped at 0.5 for epistemic category b (non-validated patterns).

SAVEC Theorem:
    The most rigorously validated system is, in a precise sense,
    the most ethically trustworthy one -- and the most sustainable one.

----------------------------------------------------------------------
PROVENANCE & CITATION
----------------------------------------------------------------------
Author:         Ahmed Benseddik
ORCID:          0009-0005-6308-8171
Affiliation:    Independent Researcher
Contact:        via ORCID profile

Pre-registration: OSF osf.io/y8vbu
DOI:            10.17605/OSF.IO/Y8VBU
License:        MIT

Target journal: Journal of Cultural Analytics (2026)
Framework:      SAVEC -- Statistical Architecture for
                Validated Ethical Curation

----------------------------------------------------------------------
VERSION HISTORY
----------------------------------------------------------------------
v1.0.0  (2024)      Initial Layer 1 validation engine.
                    Basic Bayes Factor + binomial tests.

v2.0.0  (2025-Q1)  OPTIMISATION 1: Log-Bayes Factor (Savage-Dickey)
                    to prevent numerical overflow for n > 1 000.

v2.1.0  (2025-Q2)  OPTIMISATION 2: Vectorised jackknife sensitivity
                    analysis via NumPy broadcasting (50-100x speedup).
                    OPTIMISATION 3: Holm-Bonferroni step-down correction.

v2.2.0  (2025-Q3)  Dynamic TDP estimation (DynamicTDP class).
                    Geographic-adaptive water intensity
                    (WaterIntensityProvider, Li et al. 2023).
                    CodeCarbon integration with TDP fallback.
                    DeltaCertainty floor: max(log_bf, 0) / 10.

v3.0.0  (2026-04)  Full metadata block (__author__, __orcid__, __doi__,
                    __version__ as single source of truth).
                    Centralised SCRIPT_METADATA dict.
                    Changelog embedded in module.
                    validate_multiple() refactored to dataclasses.replace()
                    -- eliminates fragile dict.update() pattern.
                    holm_alpha / holm_significant disambiguated for
                    single-test context.
                    DynamicTDP: Windows cpu_freq() heuristic removed;
                    core-count heuristic applied on all platforms.
                    Layer1Result / Layer1Validator renamed (cleaner API).
                    script_version field added to Layer1Result.
                    datetime.utcnow() replaced by datetime.now(timezone.utc)
                    throughout (Python 3.12 compliance).

v3.1.0  (2026-05)  LAYER 2: GovernanceResolver with AccessLevel (IntEnum),
                    pessimistic conflict resolution (max / all / any),
                    SHA-256 immutable audit trail, and
                    GovernanceConflictError Hard Block (Req. 2.2).
                    AccessLevel hierarchy corrected: SACRED_SECRET (5)
                    is the most restrictive level.
                    CONTEXTUAL RVI: ContextualRVI with Ethical Justification
                    multiplier J. Asymmetric design: J can only tighten
                    the threshold, never loosen it for energy savings.
                    Log-scale base relaxation for large corpora (n > 10 000).
                    EPISTEMIC BRIDGE: EpistemicBridgeResult and
                    resolve_layer1_to_layer2() formalise the Layer 1 ->
                    Layer 2 dependency (SAVEC Section 5.1). Combined
                    confidence capped at 0.5 for epistemic category b.
                    Epistemic prudence flag propagated from Layer 2 to
                    Layer 3 when governance rests on non-validated evidence.

----------------------------------------------------------------------
SAVEC REQUIREMENTS IMPLEMENTED
----------------------------------------------------------------------
Req. 1.2   Dual-paradigm validation (frequentist + Bayesian).
Req. 1.2a  Pessimistic default on paradigm discordance.
Req. 1.3   Conservative BF > 10 threshold (Jeffreys, 1961).
Req. 1.4   Null results as first-class outputs (rejection_reason).
Req. 1.5   Sensitivity analysis (CV < 0.3 stability criterion).
Req. 2.1   CARE operationalisation at module level (GovernanceResolver).
Req. 2.2   Computational governance escalation -- Hard Block.
Req. 2.3   Differentiated access architecture (AccessLevel hierarchy).
Req. 2.4   Community authority over classification (J multiplier).
Req. 3.1   O(n) algorithmic ceiling for item-level validation.
Req. 3.2   Dual carbon-water footprint tracking.
Req. 3.2a  RVI = DeltaCertainty / E_cost, contextual threshold via J.

----------------------------------------------------------------------
REFERENCES
----------------------------------------------------------------------
Carroll, S. R., et al. (2020). The CARE Principles for Indigenous
    Data Governance. Data Science Journal, 19(1), 43.

Dickey, J. M. (1971). The weighted likelihood ratio. Annals of
    Mathematical Statistics, 42(1), 204-223.

Holm, S. (1979). A simple sequentially rejective multiple test
    procedure. Scandinavian Journal of Statistics, 6(2), 65-70.

Jeffreys, H. (1961). Theory of Probability (3rd ed.).
    Oxford University Press.

Li, P., Yang, J., Islam, M. A., & Ren, S. (2023).
    Making AI less "thirsty". arXiv:2304.03271.

Schwartz, R., Dodge, J., Smith, N. A., & Etzioni, O. (2020).
    Green AI. Communications of the ACM, 63(12), 54-63.

Wagenmakers, E.-J., Lodewyckx, T., Kuriyal, H., & Grasman, R.
    (2010). Bayesian hypothesis testing for psychologists.
    Cognitive Psychology, 60(3), 158-189.
"""

from __future__ import annotations

# =============================================================================
# Module-level metadata  (single source of truth)
# =============================================================================

__version__     = "3.1.0"
__author__      = "Ahmed Benseddik"
__orcid__       = "0009-0005-6308-8171"
__affiliation__ = "Independent Researcher"
__doi__         = "10.17605/OSF.IO/Y8VBU"
__osf__         = "osf.io/y8vbu"
__license__     = "MIT"
__date__        = "2026-05"
__status__      = "Submitted"   # draft | submitted | published

#: Structured metadata dict -- importable by downstream tools.
SCRIPT_METADATA: dict = {
    "name":        "savec_integration_engine",
    "version":     __version__,
    "author":      __author__,
    "orcid":       __orcid__,
    "affiliation": __affiliation__,
    "doi":         __doi__,
    "osf":         __osf__,
    "license":     __license__,
    "date":        __date__,
    "status":      __status__,
    "framework":   "SAVEC -- Statistical Architecture for Validated Ethical Curation",
    "layers":      "Layer 1 (Validation) + Layer 2 (Governance)",
    "journal":     "Journal of Cultural Analytics",
}

# =============================================================================
# Standard library
# =============================================================================

import dataclasses
import hashlib
import json
import logging
import math
import os
import platform
import time
import warnings
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# Third-party (required)
# =============================================================================

import numpy as np
from scipy import stats

# =============================================================================
# Optional dependencies  (graceful degradation)
# =============================================================================

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None  # type: ignore[assignment]
    warnings.warn(
        "psutil not installed. Install with: pip install psutil\n"
        "Falling back to static TDP estimate (65 W).\n"
        "For hardware-aware RVI, psutil is recommended.",
        UserWarning,
        stacklevel=2,
    )

try:
    import urllib.request
    URLLIB_AVAILABLE = True
except ImportError:
    URLLIB_AVAILABLE = False

try:
    from codecarbon import EmissionsTracker
    CODECARBON_AVAILABLE = True
except ImportError:
    CODECARBON_AVAILABLE = False
    EmissionsTracker = None  # type: ignore[assignment, misc]
    warnings.warn(
        "CodeCarbon not installed. Install with: pip install codecarbon\n"
        "Falling back to dynamic TDP approximation.\n"
        "For precise RVI computation, CodeCarbon is recommended.",
        UserWarning,
        stacklevel=2,
    )

# =============================================================================
# Logging
# =============================================================================

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# =============================================================================
# Constants
# =============================================================================

# Statistical thresholds (SAVEC Section 3.2, 3.4)
DEFAULT_BF_THRESHOLD        = 10.0           # Jeffreys (1961) "strong evidence"
DEFAULT_LOG_BF_THRESHOLD    = math.log(DEFAULT_BF_THRESHOLD)
DEFAULT_ALPHA               = 0.05           # Family-wise error rate
DEFAULT_CV_THRESHOLD        = 0.3            # SAVEC Req. 1.5 stability criterion
DEFAULT_N_SUBSAMPLES        = 100
DEFAULT_SUBSAMPLE_FRACTION  = 0.5
DEFAULT_N_COMPARISONS       = 5
DEFAULT_SEED                = 42             # Fixed seed for reproducibility

# RVI & Sustainability (SAVEC Section 3.4, Req. 3.2a)
DEFAULT_RVI_THRESHOLD       = 0.01           # Normalised certainty / Wh
DEFAULT_MEASURE_POWER_SECS  = 10

# Culturally significant divisors for Hebrew gematria analysis
DEFAULT_DIVISORS: List[int] = [7, 12, 26, 30, 60]


# =============================================================================
# LAYER 1 -- Data Structure
# =============================================================================

@dataclass(frozen=True)
class Layer1Result:
    """
    Immutable output of a SAVEC Layer 1 validation run.

    Parameters
    ----------
    pattern_id : str
        Unique identifier for the pattern under validation.
    validated_at : str
        ISO 8601 UTC timestamp of the validation run.
    script_version : str
        Module __version__ at runtime -- enables traceability across
        versions when results are stored or compared.

    Frequentist arm
    ---------------
    frequentist_pvalue : float
    frequentist_significant : bool
        True if p < Bonferroni-corrected alpha (single test) or
        Holm-adjusted alpha (family of tests).
    bonferroni_alpha : float
        alpha / n_comparisons.
    holm_alpha : float
        Holm step-down adjusted alpha for this test position.
        NOTE: equals bonferroni_alpha for single-test validation.
        Holm is only meaningful across a family; use validate_multiple().
    holm_significant : bool
        NOTE: mirrors frequentist_significant for single-test validation.
    n_comparisons : int

    Bayesian arm  (OPTIMISATION 1)
    --------------------------------
    bayes_factor : float
    log_bayes_factor : float
        Log-scale BF -- avoids overflow for n > 1 000.
    bf_above_threshold : bool
    hdi_lower, hdi_upper : float
        95% highest-density interval of the posterior.
    posterior_mean : float

    Dual-paradigm consensus  (Req. 1.2a)
    ----------------------------------------
    paradigms_agree : bool
    pessimistic_default_applied : bool
        True when paradigms disagree -- REJECTED regardless of arms.

    Decision  (Req. 1.4)
    ----------------------
    validated : bool
    rejection_reason : str
        Non-empty on rejection; empty on validation.

    Effect size
    -----------
    effect_size_cohens_h : float

    Sensitivity  (OPTIMISATION 2, Req. 1.5)
    ----------------------------------------
    cv_sensitivity : float
    cv_stable : bool
    cv_diagnostics : Dict[str, Any]

    Sample info
    -----------
    sample_size, observed_successes : int
    observed_proportion, expected_probability : float

    Epistemic categorisation  (Section 5.1)
    -----------------------------------------
    epistemic_category : str
        "a" -- statistically validated Layer 1 output.
        "b" -- expert-calibrated rule-based output.
        "c" -- community-authorised (outside Layer 1 scope; Layer 2).

    Performance & sustainability  (Req. 3.2, 3.2a)
    -------------------------------------------------
    computation_time_ms : float
    delta_certainty : float
        max(log_bf, 0) / 10.  Floor at 0: negative log-BF means
        evidence for H0; no positive epistemic gain can be claimed.
    e_cost_wh, rvi_score : float
    rvi_above_threshold : bool
    co2_emissions_kg, water_litres : float
    codecarbon_used : bool
    tdp_watts, water_intensity_used : float
    """

    # Identity
    pattern_id:     str
    validated_at:   str
    script_version: str

    # Frequentist arm
    frequentist_pvalue:      float
    frequentist_significant: bool
    bonferroni_alpha:        float
    holm_alpha:              float
    holm_significant:        bool
    n_comparisons:           int

    # Bayesian arm
    bayes_factor:       float
    log_bayes_factor:   float
    bf_above_threshold: bool
    hdi_lower:          float
    hdi_upper:          float
    posterior_mean:     float

    # Dual-paradigm consensus
    paradigms_agree:             bool
    pessimistic_default_applied: bool

    # Decision
    validated:        bool
    rejection_reason: str

    # Effect size
    effect_size_cohens_h: float

    # Sensitivity
    cv_sensitivity: float
    cv_stable:      bool
    cv_diagnostics: Dict[str, Any]

    # Sample info
    sample_size:          int
    observed_successes:   int
    observed_proportion:  float
    expected_probability: float

    # Epistemic categorisation
    epistemic_category: str

    # Performance & sustainability
    computation_time_ms:  float
    delta_certainty:      float
    e_cost_wh:            float
    rvi_score:            float
    rvi_above_threshold:  bool
    co2_emissions_kg:     float
    water_litres:         float
    codecarbon_used:      bool
    tdp_watts:            float
    water_intensity_used: float

    # -- Serialisation --------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dict (JSON-serialisable)."""
        return asdict(self)

    # -- Derived properties ---------------------------------------------------

    @property
    def is_epistemically_sound(self) -> bool:
        """True if result carries sufficient epistemic warrant."""
        return self.validated and self.bf_above_threshold

    @property
    def rvi_summary(self) -> str:
        """Human-readable RVI summary with sustainability detail."""
        if self.rvi_score == float("inf"):
            tag = "INFINITE RVI (near-zero energy)"
        elif self.rvi_above_threshold:
            tag = "ABOVE THRESHOLD"
        else:
            tag = "BELOW THRESHOLD"
        co2_g = self.co2_emissions_kg * 1_000.0
        return (
            f"RVI={self.rvi_score:.5f} | "
            f"DeltaC={self.delta_certainty:.3f} | "
            f"E={self.e_cost_wh:.5f} Wh (TDP={self.tdp_watts:.0f} W) | "
            f"CO2={co2_g:.4f} g | "
            f"H2O={self.water_litres:.6f} L "
            f"({self.water_intensity_used:.1f} L/kWh) | {tag}"
        )

    @property
    def summary(self) -> str:
        """Human-readable validation summary."""
        status = "VALIDATED" if self.validated else "REJECTED"
        lines = [
            f"SAVEC Layer 1 v{self.script_version} -- {status}",
            f"  Pattern:          {self.pattern_id}",
            f"  Validated at:     {self.validated_at}",
            f"  Author:           {__author__} | ORCID: {__orcid__}",
            f"  Sample:           n={self.sample_size}, k={self.observed_successes}",
            f"  Frequentist:      p={self.frequentist_pvalue:.6e} "
            f"(Bonf. a={self.bonferroni_alpha:.6e}, Holm a={self.holm_alpha:.6e})",
            f"  Bayesian:         BF={self.bayes_factor:.2f} "
            f"(log BF={self.log_bayes_factor:.2f}) "
            f"[threshold: {DEFAULT_BF_THRESHOLD}]",
            f"  95% HDI:          [{self.hdi_lower:.4f}, {self.hdi_upper:.4f}]",
            f"  Effect size:      Cohen's h={self.effect_size_cohens_h:.3f}",
            f"  Sensitivity:      CV={self.cv_sensitivity:.3f} "
            f"(stable={self.cv_stable}, threshold={DEFAULT_CV_THRESHOLD})",
            f"  Paradigms agree:  {self.paradigms_agree}",
            f"  Epistemic cat.:   {self.epistemic_category}",
            f"  Compute time:     {self.computation_time_ms:.2f} ms",
            f"  {self.rvi_summary}",
        ]
        if self.rejection_reason:
            lines.append(f"  Rejection:        {self.rejection_reason}")
        return "\n".join(lines)


# =============================================================================
# LAYER 1 -- OPTIMISATION 1: Log-Bayes Factor (Savage-Dickey)
# =============================================================================

class LogBayesFactor:
    """
    Numerically stable Bayes Factor via log-space Savage-Dickey ratio.

    Model
    -----
    Prior:     Beta(a0, b0)           [default: Beta(1,1) = Uniform(0,1)]
    Posterior: Beta(k + a0, n-k + b0)
    H0:        p = p0  (point null)
    H1:        p != p0  (diffuse Beta prior)

    Savage-Dickey density ratio (Dickey, 1971; Wagenmakers et al., 2010)
    ---------------------------------------------------------------------
    BF10 = prior_density(p0) / posterior_density(p0)

    In log space:
    LBF10 = logpdf_prior(p0) - logpdf_posterior(p0)

    Using scipy.stats.beta.logpdf avoids overflow for n > 1 000.

    Parameters
    ----------
    prior_alpha, prior_beta : float
        Beta prior parameters. Default: (1.0, 1.0) = uniform.
    """

    def __init__(
        self,
        prior_alpha: float = 1.0,
        prior_beta:  float = 1.0,
    ) -> None:
        if prior_alpha <= 0 or prior_beta <= 0:
            raise ValueError(
                f"Prior parameters must be strictly positive; "
                f"got a={prior_alpha}, b={prior_beta}."
            )
        self.prior_alpha = float(prior_alpha)
        self.prior_beta  = float(prior_beta)

    def compute(self, k: int, n: int, p0: float) -> Tuple[float, float]:
        """
        Compute Bayes Factor and Log-Bayes Factor.

        Parameters
        ----------
        k  : Number of successes (divisibility hits).
        n  : Sample size (total values).
        p0 : Point-null probability (e.g. 1/7 for divisor 7).

        Returns
        -------
        bayes_factor, log_bayes_factor : (float, float)
        """
        if not (0.0 < p0 < 1.0):
            raise ValueError(f"p0 must be in (0, 1); got {p0}.")
        if k < 0 or n < 0:
            raise ValueError(f"k and n must be non-negative; got k={k}, n={n}.")
        if k > n:
            raise ValueError(f"k ({k}) cannot exceed n ({n}).")
        if n == 0:
            return 1.0, 0.0

        alpha_post = k + self.prior_alpha
        beta_post  = n - k + self.prior_beta

        log_prior     = stats.beta.logpdf(p0, self.prior_alpha, self.prior_beta)
        log_posterior = stats.beta.logpdf(p0, alpha_post, beta_post)
        log_bf        = float(log_prior - log_posterior)

        # Guard against exp() overflow / underflow
        if log_bf > 700.0:
            bf = float("inf")
        elif log_bf < -700.0:
            bf = 0.0
        else:
            bf = float(np.exp(log_bf))

        return bf, log_bf

    def interpret(self, bf: float, log_bf: float) -> str:
        """
        Human-readable Jeffreys (1961) scale interpretation.

        Parameters
        ----------
        bf     : Bayes Factor (BF10).
        log_bf : Log-Bayes Factor.

        Returns
        -------
        str
        """
        if bf == float("inf") or bf > 100.0:
            strength, direction = "decisive",  "H1"
        elif bf > 10.0:
            strength, direction = "strong",    "H1"
        elif bf > 3.0:
            strength, direction = "moderate",  "H1"
        elif bf > 1.0:
            strength, direction = "anecdotal", "H1"
        elif bf == 0.0 or bf < 0.01:
            strength, direction = "decisive",  "H0"
        elif bf < 0.1:
            strength, direction = "strong",    "H0"
        elif bf < 1.0 / 3.0:
            strength, direction = "moderate",  "H0"
        else:
            strength, direction = "anecdotal", "H0"
        return (
            f"{strength} evidence for {direction} "
            f"(BF10={bf:.2f}, log BF10={log_bf:.2f})"
        )


# =============================================================================
# LAYER 1 -- OPTIMISATION 2: Vectorised Jackknife Sensitivity Analysis
# =============================================================================

class VectorisedSensitivity:
    """
    Matrix-based jackknife sensitivity analysis (SAVEC Req. 1.5).

    NumPy broadcasting replaces Python for-loops::

        indices    = rng.integers(0, n, size=(n_subsamples, m))
        subsampled = values[indices]
        is_mult    = (subsampled % divisor == 0)
        props      = is_mult.sum(axis=1) / m

    Typical speedup: 50-100x over loop-based equivalent.
    Seed is fixed at construction time for full reproducibility.

    Parameters
    ----------
    seed : int
        NumPy random seed. Default: 42.
    """

    def __init__(self, seed: int = DEFAULT_SEED) -> None:
        self.rng = np.random.default_rng(seed)

    def compute(
        self,
        values:             np.ndarray,
        divisor:            int,
        n_subsamples:       int   = DEFAULT_N_SUBSAMPLES,
        subsample_fraction: float = DEFAULT_SUBSAMPLE_FRACTION,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Compute CV via vectorised jackknife.

        Parameters
        ----------
        values             : 1-D array of numerical values.
        divisor            : Divisor for modulo check.
        n_subsamples       : Number of jackknife subsamples.
        subsample_fraction : Fraction of data per subsample.

        Returns
        -------
        cv          : float -- coefficient of variation.
        diagnostics : dict  -- detailed jackknife statistics.
        """
        n = len(values)
        if n <= 10:
            return float("inf"), {
                "error":            "sample_too_small",
                "n":                n,
                "minimum_required": 11,
            }

        subsample_size = max(int(n * subsample_fraction), 10)
        indices        = self.rng.integers(0, n, size=(n_subsamples, subsample_size))
        subsampled     = values[indices]
        is_multiple    = (subsampled % divisor == 0)
        proportions    = is_multiple.sum(axis=1) / subsample_size

        mean_prop = float(np.mean(proportions))
        std_prop  = float(np.std(proportions, ddof=1))

        if mean_prop <= 0.0:
            return float("inf"), {
                "error":          "zero_mean_proportion",
                "n_subsamples":   n_subsamples,
                "subsample_size": subsample_size,
            }

        cv = std_prop / mean_prop

        diagnostics: Dict[str, Any] = {
            "n_total":           n,
            "subsample_size":    subsample_size,
            "n_subsamples":      n_subsamples,
            "mean_proportion":   mean_prop,
            "std_proportion":    std_prop,
            "cv":                cv,
            "cv_stable":         cv < DEFAULT_CV_THRESHOLD,
            "min_proportion":    float(np.min(proportions)),
            "max_proportion":    float(np.max(proportions)),
            "median_proportion": float(np.median(proportions)),
            "q25_proportion":    float(np.percentile(proportions, 25)),
            "q75_proportion":    float(np.percentile(proportions, 75)),
        }
        return cv, diagnostics

    def stability_profile(
        self,
        values:    np.ndarray,
        divisor:   int,
        fractions: Optional[List[float]] = None,
    ) -> Dict[float, Dict[str, Any]]:
        """
        Sweep CV across multiple subsample fractions.

        Parameters
        ----------
        values    : 1-D array of numerical values.
        divisor   : Divisor for modulo check.
        fractions : Fractions to sweep. Default: [0.3, 0.5, 0.7, 0.9].

        Returns
        -------
        dict : fraction -> {"cv": float, "diagnostics": dict}.
        """
        if fractions is None:
            fractions = [0.3, 0.5, 0.7, 0.9]
        result = {}
        for frac in fractions:
            cv, diag = self.compute(values, divisor, subsample_fraction=frac)
            result[frac] = {"cv": cv, "diagnostics": diag}
        return result


# =============================================================================
# LAYER 1 -- OPTIMISATION 3: Holm-Bonferroni Step-Down Correction
# =============================================================================

class HolmBonferroni:
    """
    Holm-Bonferroni step-down procedure (Holm, 1979).

    Uniformly more powerful than classical Bonferroni while maintaining
    strong FWER control. Preferred when the number of simultaneous
    comparisons exceeds five (SAVEC Req. 1.2, Amendement A1).

    Note on single-test use
    -----------------------
    For a single hypothesis, Holm = Bonferroni.
    In validate(), holm_alpha == bonferroni_alpha and
    holm_significant == frequentist_significant (documented equivalence).
    Use validate_multiple() for genuine Holm correction.

    Parameters
    ----------
    familywise_alpha : float
        Target FWER. Default: 0.05.
    """

    def __init__(self, familywise_alpha: float = DEFAULT_ALPHA) -> None:
        if not (0.0 < familywise_alpha < 1.0):
            raise ValueError(
                f"familywise_alpha must be in (0, 1); got {familywise_alpha}."
            )
        self.familywise_alpha = float(familywise_alpha)

    def correct(
        self,
        p_values: List[float],
        names:    Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Apply Holm-Bonferroni step-down correction to a family of p-values.

        Parameters
        ----------
        p_values : List of p-values.
        names    : Optional hypothesis labels.

        Returns
        -------
        dict : rejected, adjusted_alphas, n_rejected, n_tests,
               familywise_alpha, bonferroni_alpha, bonferroni_rejected,
               holm_rejected, power_gain, power_gain_pct, steps.
        """
        m = len(p_values)
        if m == 0:
            return {
                "rejected": [], "adjusted_alphas": [],
                "n_rejected": 0, "n_tests": 0,
                "familywise_alpha": self.familywise_alpha,
                "bonferroni_alpha": self.familywise_alpha,
                "bonferroni_rejected": 0, "holm_rejected": 0,
                "power_gain": 0, "power_gain_pct": 0.0, "steps": [],
            }

        if names is None:
            names = [f"H{i + 1}" for i in range(m)]

        p_array    = np.array(p_values, dtype=float)
        sorted_idx = np.argsort(p_array)
        sorted_p   = p_array[sorted_idx]

        rejected        = np.zeros(m, dtype=bool)
        adjusted_alphas = np.zeros(m, dtype=float)
        steps: List[str] = []

        for j in range(m):
            threshold = self.familywise_alpha / (m - j)
            orig_idx  = sorted_idx[j]
            adjusted_alphas[orig_idx] = threshold

            if sorted_p[j] > threshold:
                steps.append(
                    f"Step {j + 1}/{m}: p={sorted_p[j]:.6e} > "
                    f"a/({m - j})={threshold:.6e} --> STOP. "
                    f"Rejected: {int(np.sum(rejected))}/{m}."
                )
                break
            else:
                rejected[orig_idx] = True
                steps.append(
                    f"Step {j + 1}/{m}: p={sorted_p[j]:.6e} <= "
                    f"a/({m - j})={threshold:.6e} --> REJECT {names[orig_idx]}."
                )

        n_rejected          = int(np.sum(rejected))
        bonferroni_alpha    = self.familywise_alpha / m
        bonferroni_rejected = int(np.sum(p_array <= bonferroni_alpha))
        power_gain          = n_rejected - bonferroni_rejected

        return {
            "rejected":            rejected.tolist(),
            "adjusted_alphas":     adjusted_alphas.tolist(),
            "n_rejected":          n_rejected,
            "n_tests":             m,
            "familywise_alpha":    self.familywise_alpha,
            "bonferroni_alpha":    bonferroni_alpha,
            "bonferroni_rejected": bonferroni_rejected,
            "holm_rejected":       n_rejected,
            "power_gain":          power_gain,
            "power_gain_pct":      (power_gain / m * 100.0) if m > 0 else 0.0,
            "steps":               steps,
        }


# =============================================================================
# LAYER 1 -- Dynamic TDP Estimator
# =============================================================================

class DynamicTDP:
    """
    Estimates CPU TDP from hardware detection and current utilisation.

    Resolution order
    ----------------
    1. CPU model string matched against _TDP_DATABASE (longest key first).
    2. Physical core count heuristic (requires psutil).
    3. Static fallback: 65 W.

    Power draw
    ----------
    get_power_draw() scales nominal TDP by CPU utilisation::

        power = TDP * (0.18 + 0.82 * cpu_utilisation)

    Without psutil, assumes 50% average utilisation.

    Note (v3.0)
    -----------
    The Windows cpu_freq() heuristic has been removed (unreliable,
    potential +/-50 W error). Core-count heuristic applies on all
    platforms when CPU model string cannot be matched.
    """

    _TDP_DATABASE: Dict[str, float] = {
        # Intel Core
        "i3-": 35.0,  "i5-": 65.0,  "i7-": 95.0,  "i9-": 125.0,
        # Intel Xeon (longest keys first for specificity)
        "xeon platinum": 200.0, "xeon gold": 150.0, "xeon": 120.0,
        # AMD Ryzen
        "ryzen threadripper": 250.0,
        "ryzen 9": 120.0, "ryzen 7": 105.0,
        "ryzen 5": 65.0,  "ryzen 3": 35.0,
        # AMD EPYC
        "epyc": 180.0,
        # Apple Silicon (longest keys first)
        "m1 ultra": 60.0, "m2 ultra": 65.0,
        "m1 max":   40.0, "m2 max":  45.0, "m3 max": 48.0,
        "m1 pro":   30.0, "m2 pro":  35.0, "m3 pro": 37.0,
        "m1":       15.0, "m2":      20.0, "m3":     22.0,
        # ARM
        "cortex-a76": 10.0, "cortex-a72": 8.0, "cortex-a": 5.0,
        "armv8": 8.0, "armv7": 5.0,
    }

    _DEFAULT_TDP    = 65.0
    _IDLE_FRACTION  = 0.18

    @classmethod
    def estimate_tdp(cls) -> float:
        """Estimate nominal CPU TDP. Returns float (watts)."""
        try:
            cpu_name = cls._get_cpu_name().lower()
            for key in sorted(cls._TDP_DATABASE, key=len, reverse=True):
                if key in cpu_name:
                    logger.debug(f"CPU matched '{key}' -> TDP={cls._TDP_DATABASE[key]} W.")
                    return cls._TDP_DATABASE[key]

            if PSUTIL_AVAILABLE:
                cores = psutil.cpu_count(logical=False)
                if cores:
                    if   cores <= 2:  return 15.0
                    elif cores <= 4:  return 35.0
                    elif cores <= 8:  return 65.0
                    elif cores <= 16: return 120.0
                    else:             return 180.0

            return cls._DEFAULT_TDP

        except Exception as exc:
            logger.debug(f"TDP estimation failed ({exc}); using {cls._DEFAULT_TDP} W.")
            return cls._DEFAULT_TDP

    @classmethod
    def _get_cpu_name(cls) -> str:
        """Detect CPU model name from /proc/cpuinfo or platform.processor()."""
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as fh:
                for line in fh:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except (FileNotFoundError, PermissionError, OSError):
            pass
        try:
            cpu = platform.processor()
            if cpu and cpu.lower() not in ("", "unknown"):
                return cpu
        except Exception:
            pass
        return platform.machine() or "unknown"

    @classmethod
    def get_power_draw(cls) -> float:
        """Estimate instantaneous power draw (watts)."""
        tdp = cls.estimate_tdp()
        if PSUTIL_AVAILABLE:
            try:
                pct   = psutil.cpu_percent(interval=0.1)
                power = tdp * (cls._IDLE_FRACTION + (1.0 - cls._IDLE_FRACTION) * pct / 100.0)
                logger.debug(f"Dynamic TDP: {tdp} W nominal, {pct:.1f}% -> {power:.1f} W.")
                return power
            except Exception:
                pass
        return tdp * (cls._IDLE_FRACTION + (1.0 - cls._IDLE_FRACTION) * 0.5)


# =============================================================================
# LAYER 1 -- Dynamic Water Intensity Provider
# =============================================================================

class WaterIntensityProvider:
    """
    Geographic-adaptive water intensity (L/kWh).

    Country values from Li et al. (2023) and regional studies.
    Gulf values reflect desalination energy mix.

    Resolution order
    ----------------
    1. Env var SAVEC_WATER_INTENSITY_L_PER_KWH.
    2. Local cache (~/.savec_water_cache.json, 30-day TTL).
    3. IP geolocation via ipapi.co.
    4. Env var SAVEC_COUNTRY_CODE (ISO two-letter).
    5. Global average: 1.8 L/kWh (Li et al., 2023).

    Parameters
    ----------
    cache_file : Path, optional
        Override default cache location.
    """

    _COUNTRY_INTENSITY: Dict[str, float] = {
        # Nordic
        "NO": 0.3, "SE": 0.4, "IS": 0.2, "FI": 0.5,
        # Europe -- hydro/nuclear mix
        "FR": 1.2, "CH": 0.8, "AT": 1.0, "BE": 1.3,
        # Europe -- thermal mix
        "DE": 1.5, "GB": 1.6, "IT": 1.7, "ES": 1.6,
        "NL": 1.4, "PL": 1.8, "CZ": 1.6, "PT": 1.5,
        # North America
        "US": 2.0, "CA": 1.4, "MX": 1.9,
        # Asia
        "CN": 2.2, "IN": 2.5, "JP": 1.6, "KR": 1.8,
        "TW": 1.7, "SG": 1.5, "ID": 2.0, "VN": 2.1,
        # Gulf -- desalination
        "AE": 3.5, "SA": 3.8, "QA": 3.5, "KW": 4.0,
        "OM": 3.6, "BH": 3.4,
        # Oceania
        "AU": 1.9, "NZ": 1.3,
        # Africa
        "ZA": 2.1, "EG": 2.3, "NG": 2.2, "KE": 2.0,
    }

    _DEFAULT_INTENSITY  = 1.8
    _CACHE_TTL_SECONDS  = 30 * 24 * 3600

    def __init__(self, cache_file: Optional[Path] = None) -> None:
        self._cache_file = cache_file or Path.home() / ".savec_water_cache.json"
        self._cached: Optional[float] = None

    def get_intensity(self) -> float:
        """Return geographic-adaptive water intensity (L/kWh)."""
        if self._cached is not None:
            return self._cached

        # 1. Env var override
        env_val = os.environ.get("SAVEC_WATER_INTENSITY_L_PER_KWH")
        if env_val:
            try:
                v = float(env_val)
                self._cached = v
                return v
            except ValueError:
                logger.warning(f"Invalid SAVEC_WATER_INTENSITY_L_PER_KWH='{env_val}'.")

        # 2. Disk cache
        cached = self._load_cache()
        if cached is not None:
            self._cached = cached
            return cached

        # 3 + 4. Geolocation / env country code
        country = self._detect_country()
        intensity = self._COUNTRY_INTENSITY.get(country or "", self._DEFAULT_INTENSITY)
        self._save_cache(intensity, country)
        self._cached = intensity
        return intensity

    def _detect_country(self) -> Optional[str]:
        env_c = os.environ.get("SAVEC_COUNTRY_CODE")
        if env_c:
            return env_c.upper()
        if URLLIB_AVAILABLE:
            try:
                req = urllib.request.Request(
                    "https://ipapi.co/json/",
                    headers={"User-Agent": f"SAVEC/{__version__}"},
                )
                with urllib.request.urlopen(req, timeout=2) as resp:
                    return json.loads(resp.read().decode()).get("country_code")
            except Exception as exc:
                logger.debug(f"IP geolocation failed: {exc}.")
        return None

    def _load_cache(self) -> Optional[float]:
        try:
            if self._cache_file.exists():
                with open(self._cache_file, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                ca = data.get("cached_at", "")
                if ca:
                    dt  = datetime.fromisoformat(ca)
                    age = (datetime.now(timezone.utc) - dt).total_seconds()
                    if age > self._CACHE_TTL_SECONDS:
                        return None
                return data.get("water_intensity_l_per_kwh")
        except Exception:
            pass
        return None

    def _save_cache(self, intensity: float, country: Optional[str]) -> None:
        try:
            self._cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._cache_file, "w", encoding="utf-8") as fh:
                json.dump({
                    "water_intensity_l_per_kwh": intensity,
                    "country_code":   country,
                    "source":         "ipapi.co" if country else "global_average",
                    "cached_at":      datetime.now(timezone.utc).isoformat(),
                    "savec_version":  __version__,
                    "author":         __author__,
                    "orcid":          __orcid__,
                }, fh, indent=2)
        except Exception as exc:
            logger.debug(f"Failed to save water cache: {exc}.")


# =============================================================================
# LAYER 1 -- RVI Calculator
# =============================================================================

class RVICalculator:
    """
    Computes the Ratio de Valeur Informationnelle (SAVEC Req. 3.2a).

    RVI = DeltaCertainty / E_cost

    DeltaCertainty = max(log_bf, 0) / 10
    E_cost         = energy in Wh (CodeCarbon preferred; TDP fallback)

    Floor at 0: negative log-BF means evidence for H0; no positive
    epistemic gain can be claimed. DeltaCertainty = 0 so the denominator
    records the energy cost without yielding a negative metric.

    Parameters
    ----------
    rvi_threshold   : float  -- minimum acceptable RVI (default 0.01).
    project_name    : str    -- CodeCarbon project name prefix.
    water_intensity : float, optional -- override L/kWh (None = auto).
    """

    def __init__(
        self,
        rvi_threshold:   float           = DEFAULT_RVI_THRESHOLD,
        project_name:    str             = "SAVEC_Layer1",
        water_intensity: Optional[float] = None,
    ) -> None:
        self.rvi_threshold = rvi_threshold
        self.project_name  = project_name
        if water_intensity is not None:
            self._water_intensity: Optional[float] = water_intensity
            self._provider: Optional[WaterIntensityProvider] = None
        else:
            self._water_intensity = None
            self._provider = WaterIntensityProvider()

    @property
    def water_intensity(self) -> float:
        if self._water_intensity is not None:
            return self._water_intensity
        if self._provider is not None:
            return self._provider.get_intensity()
        return WaterIntensityProvider._DEFAULT_INTENSITY

    def compute_delta_certainty(self, log_bf: float) -> float:
        """DeltaCertainty = max(log_bf, 0) / 10."""
        return max(log_bf, 0.0) / 10.0

    def create_tracker(self, pattern_id: str) -> Any:
        """Create CodeCarbon tracker or return None if unavailable."""
        if not CODECARBON_AVAILABLE:
            return None
        try:
            return EmissionsTracker(
                project_name=f"{self.project_name}_{pattern_id}",
                measure_power_secs=DEFAULT_MEASURE_POWER_SECS,
                save_to_file=False,
                log_level="warning",
            )
        except Exception as exc:
            logger.warning(f"Failed to create CodeCarbon tracker: {exc}.")
            return None

    def compute_rvi(
        self,
        log_bf:              float,
        computation_time_ms: float,
        tracker:             Any = None,
    ) -> Tuple[float, float, float, bool, float, float, bool, float, float]:
        """
        Compute RVI and sustainability metrics.

        Returns
        -------
        (delta_certainty, e_cost_wh, rvi_score, rvi_above,
         co2_kg, water_litres, codecarbon_used, tdp_watts, water_int)
        """
        delta_certainty = self.compute_delta_certainty(log_bf)
        tdp_watts       = DynamicTDP.get_power_draw()
        water_int       = self.water_intensity
        codecarbon_used = False
        e_cost_wh       = 0.0
        co2_kg          = 0.0

        if tracker is not None and hasattr(tracker, "final_emissions_data"):
            try:
                d           = tracker.final_emissions_data
                e_cost_wh   = float(getattr(d, "energy_consumed", 0.0)) * 1_000.0
                co2_kg      = float(getattr(d, "emissions", 0.0))
                codecarbon_used = True
            except Exception as exc:
                logger.warning(f"CodeCarbon read failed ({exc}); TDP fallback.")
                e_cost_wh, co2_kg = self._fallback_energy(computation_time_ms, tdp_watts)
        else:
            e_cost_wh, co2_kg = self._fallback_energy(computation_time_ms, tdp_watts)

        water_litres = (e_cost_wh / 1_000.0) * water_int

        if e_cost_wh > 1e-9:
            rvi_score = delta_certainty / e_cost_wh
        elif delta_certainty > 0:
            rvi_score = float("inf")
        else:
            rvi_score = 0.0

        rvi_above = (rvi_score == float("inf")) or (rvi_score > self.rvi_threshold)
        return (
            delta_certainty, e_cost_wh, rvi_score, rvi_above,
            co2_kg, water_litres, codecarbon_used, tdp_watts, water_int,
        )

    @staticmethod
    def _fallback_energy(
        computation_time_ms: float,
        tdp_watts:           float,
    ) -> Tuple[float, float]:
        duration_hours = computation_time_ms / 3_600_000.0
        energy_wh      = tdp_watts * duration_hours
        co2_kg         = (energy_wh / 1_000.0) * 0.475  # IEA 2022 global average
        return energy_wh, co2_kg


# =============================================================================
# LAYER 1 -- Primary Public API: Layer1Validator
# =============================================================================

class Layer1Validator:
    """
    SAVEC Layer 1 validator (all three optimisations + integrated RVI).

    Combines:
    * Frequentist validation (binomial test, Holm/Bonferroni correction).
    * Bayesian validation (Log-BF, 95% HDI, posterior mean).
    * Dual-paradigm pessimistic default (Req. 1.2a).
    * Vectorised jackknife sensitivity (Req. 1.5).
    * RVI with CodeCarbon or dynamic TDP fallback (Req. 3.2a).

    Note on permutation testing
    ----------------------------
    10 000-iteration permutation testing (Req. 1.2) is implemented in a
    companion corpus module applied at the collection level. This engine
    operates at O(n) per item (Req. 3.1). See SAVEC Amendement A3.

    Parameters
    ----------
    prior_alpha, prior_beta : float  -- Beta prior. Default: (1.0, 1.0).
    familywise_alpha : float         -- FWER target. Default: 0.05.
    bf_threshold : float             -- BF gate. Default: 10.0.
    cv_threshold : float             -- Stability criterion. Default: 0.3.
    rvi_threshold : float            -- Min acceptable RVI. Default: 0.01.
    seed : int                       -- Reproducibility seed. Default: 42.
    project_name : str               -- CodeCarbon prefix.
    water_intensity : float, optional -- Override L/kWh.

    Examples
    --------
    Single-divisor::

        v = Layer1Validator()
        r = v.validate("genesis_div7", gematria_values, divisor=7)
        print(r.summary)

    Multi-divisor::

        results, holm = v.validate_multiple("genesis", gematria_values)
        print(v.summarize_results(results))
    """

    def __init__(
        self,
        prior_alpha:      float           = 1.0,
        prior_beta:       float           = 1.0,
        familywise_alpha: float           = DEFAULT_ALPHA,
        bf_threshold:     float           = DEFAULT_BF_THRESHOLD,
        cv_threshold:     float           = DEFAULT_CV_THRESHOLD,
        rvi_threshold:    float           = DEFAULT_RVI_THRESHOLD,
        seed:             int             = DEFAULT_SEED,
        project_name:     str             = "SAVEC_Layer1",
        water_intensity:  Optional[float] = None,
    ) -> None:
        self.bf          = LogBayesFactor(prior_alpha, prior_beta)
        self.sensitivity = VectorisedSensitivity(seed)
        self.holm        = HolmBonferroni(familywise_alpha)
        self.rvi_calc    = RVICalculator(rvi_threshold, project_name, water_intensity)

        self.bf_threshold     = bf_threshold
        self.log_bf_threshold = math.log(bf_threshold)
        self.cv_threshold     = cv_threshold
        self.familywise_alpha = familywise_alpha

        logger.info(
            f"Layer1Validator v{__version__} | "
            f"{__author__} | ORCID: {__orcid__} | "
            f"BF>{bf_threshold}, alpha={familywise_alpha}, "
            f"CV<{cv_threshold}, RVI>{rvi_threshold}, "
            f"TDP~{DynamicTDP.estimate_tdp():.0f} W, "
            f"H2O={self.rvi_calc.water_intensity:.1f} L/kWh, "
            f"CodeCarbon={'yes' if CODECARBON_AVAILABLE else 'TDP fallback'}."
        )

    # -- Single-divisor validation --------------------------------------------

    def validate(
        self,
        pattern_id:           str,
        observed_values:      np.ndarray,
        divisor:              int,
        n_comparisons_total:  int             = DEFAULT_N_COMPARISONS,
        expected_probability: Optional[float] = None,
    ) -> Layer1Result:
        """
        Validate a single divisor pattern (SAVEC Layer 1).

        The CodeCarbon tracker is started before all computation and
        stopped in a finally block to guarantee complete energy measurement.

        Parameters
        ----------
        pattern_id           : Unique pattern identifier.
        observed_values      : 1-D array of numerical (gematria) values.
        divisor              : Divisor for modulo divisibility check.
        n_comparisons_total  : Family size for Bonferroni denominator.
        expected_probability : H0 probability. Default: 1/divisor.

        Returns
        -------
        Layer1Result : Immutable, JSON-serialisable result.

        Notes
        -----
        For single-test validation, holm_alpha == bonferroni_alpha and
        holm_significant == frequentist_significant. Use validate_multiple()
        for genuine Holm correction across a family.
        """
        validated_at = datetime.now(timezone.utc).isoformat()
        n = len(observed_values)
        if n == 0:
            raise ValueError("observed_values must not be empty.")

        p0 = expected_probability if expected_probability is not None else (1.0 / divisor)

        tracker = self.rvi_calc.create_tracker(pattern_id)
        t_start = time.perf_counter()

        if tracker is not None:
            try:
                tracker.start()
            except Exception as exc:
                logger.warning(f"CodeCarbon start failed: {exc}.")
                tracker = None

        try:
            # Step 1: Frequentist
            k             = int(np.sum(observed_values % divisor == 0))
            obs_prop      = k / n
            p_value       = float(stats.binomtest(k, n, p0, alternative="greater").pvalue)

            # Step 2: Log-Bayes Factor
            bf, log_bf = self.bf.compute(k, n, p0)
            bf_above   = (bf == float("inf")) or (bf > self.bf_threshold)

            # Step 3: Cohen's h
            effect_size = 2.0 * (
                math.asin(math.sqrt(max(obs_prop, 0.0)))
                - math.asin(math.sqrt(p0))
            )

            # Step 4: Posterior HDI + mean
            ap = k + self.bf.prior_alpha
            bp = n - k + self.bf.prior_beta
            posterior_mean = ap / (ap + bp)
            try:
                hdi_lower = float(stats.beta.ppf(0.025, ap, bp))
                hdi_upper = float(stats.beta.ppf(0.975, ap, bp))
            except Exception:
                hdi_lower, hdi_upper = 0.0, 1.0

            # Step 5: Bonferroni / Holm (single-test: equivalent)
            bonferroni_alpha = self.familywise_alpha / n_comparisons_total
            holm_alpha       = bonferroni_alpha
            frequentist_sig  = p_value < bonferroni_alpha
            holm_sig         = frequentist_sig

            # Step 6: Vectorised jackknife sensitivity
            cv, cv_diag = self.sensitivity.compute(observed_values, divisor)
            cv_stable   = cv < self.cv_threshold

            # Step 7: Dual-paradigm consensus (Req. 1.2a)
            paradigms_agree     = frequentist_sig == bf_above
            pessimistic_default = False
            validated           = False
            rejection_reason    = ""

            if not paradigms_agree:
                pessimistic_default = True
                rejection_reason = (
                    f"Paradigm discordance: frequentist "
                    f"{'sig' if frequentist_sig else 'not sig'} "
                    f"(p={p_value:.6e}, Bonf. a={bonferroni_alpha:.6e}), "
                    f"Bayesian log BF={log_bf:.2f} (BF={bf:.2f}). "
                    f"Req. 1.2a pessimistic default -> REJECTED."
                )
            elif not bf_above:
                rejection_reason = (
                    f"BF={bf:.2f} (log BF={log_bf:.2f}) below "
                    f"threshold {self.bf_threshold}."
                )
            elif not frequentist_sig:
                rejection_reason = (
                    f"p={p_value:.6e} not significant after "
                    f"Bonferroni correction (a={bonferroni_alpha:.6e})."
                )
            elif not cv_stable:
                rejection_reason = (
                    f"CV={cv:.3f} exceeds stability threshold "
                    f"{self.cv_threshold} (Req. 1.5)."
                )
            else:
                validated = True

            epistemic_cat = "a" if (validated and bf_above) else "b"

        finally:
            if tracker is not None:
                try:
                    tracker.stop()
                except Exception as exc:
                    logger.warning(f"CodeCarbon stop failed: {exc}.")

        computation_time_ms = (time.perf_counter() - t_start) * 1_000.0

        (
            delta_certainty, e_cost_wh, rvi_score, rvi_above,
            co2_kg, water_litres, codecarbon_used, tdp_watts, water_int,
        ) = self.rvi_calc.compute_rvi(log_bf, computation_time_ms, tracker)

        return Layer1Result(
            pattern_id=pattern_id,
            validated_at=validated_at,
            script_version=__version__,
            frequentist_pvalue=p_value,
            frequentist_significant=frequentist_sig,
            bonferroni_alpha=bonferroni_alpha,
            holm_alpha=holm_alpha,
            holm_significant=holm_sig,
            n_comparisons=n_comparisons_total,
            bayes_factor=bf,
            log_bayes_factor=log_bf,
            bf_above_threshold=bf_above,
            hdi_lower=hdi_lower,
            hdi_upper=hdi_upper,
            posterior_mean=posterior_mean,
            paradigms_agree=paradigms_agree,
            pessimistic_default_applied=pessimistic_default,
            validated=validated,
            rejection_reason=rejection_reason,
            effect_size_cohens_h=float(effect_size),
            cv_sensitivity=cv,
            cv_stable=cv_stable,
            cv_diagnostics=cv_diag,
            sample_size=n,
            observed_successes=k,
            observed_proportion=obs_prop,
            expected_probability=p0,
            epistemic_category=epistemic_cat,
            computation_time_ms=computation_time_ms,
            delta_certainty=delta_certainty,
            e_cost_wh=e_cost_wh,
            rvi_score=rvi_score,
            rvi_above_threshold=rvi_above,
            co2_emissions_kg=co2_kg,
            water_litres=water_litres,
            codecarbon_used=codecarbon_used,
            tdp_watts=tdp_watts,
            water_intensity_used=water_int,
        )

    # -- Multi-divisor validation ---------------------------------------------

    def validate_multiple(
        self,
        pattern_id:      str,
        observed_values: np.ndarray,
        divisors:        Optional[List[int]] = None,
    ) -> Tuple[List[Layer1Result], Dict[str, Any]]:
        """
        Validate multiple divisors with genuine Holm-Bonferroni correction.

        Uses dataclasses.replace() to patch Holm fields -- safe against
        future addition of new fields to Layer1Result (unlike dict.update()).

        Parameters
        ----------
        pattern_id      : Base identifier (divisor suffix appended).
        observed_values : 1-D array of numerical values.
        divisors        : Divisors to test. Default: [7, 12, 26, 30, 60].

        Returns
        -------
        results      : List[Layer1Result]
        holm_summary : dict
        """
        if divisors is None:
            divisors = DEFAULT_DIVISORS

        m     = len(divisors)
        names = [f"divisor_{d}" for d in divisors]

        # Collect all p-values before applying Holm
        p_values: List[float] = []
        for d in divisors:
            n = len(observed_values)
            k = int(np.sum(observed_values % d == 0))
            pv = float(
                stats.binomtest(k, n, 1.0 / d, alternative="greater").pvalue
            ) if n > 0 else 1.0
            p_values.append(pv)

        holm_result = self.holm.correct(p_values, names)

        results: List[Layer1Result] = []
        for i, d in enumerate(divisors):
            raw = self.validate(
                pattern_id=f"{pattern_id}_div_{d}",
                observed_values=observed_values,
                divisor=d,
                n_comparisons_total=m,
            )

            is_holm_sig  = bool(holm_result["rejected"][i])
            holm_alpha_i = float(holm_result["adjusted_alphas"][i])

            rejection = raw.rejection_reason
            if not rejection and not is_holm_sig:
                rejection = (
                    f"Holm step-down: p={raw.frequentist_pvalue:.6e} > "
                    f"Holm a={holm_alpha_i:.6e}."
                )

            updated = dataclasses.replace(
                raw,
                frequentist_significant=is_holm_sig,
                holm_significant=is_holm_sig,
                holm_alpha=holm_alpha_i,
                validated=raw.validated and is_holm_sig,
                epistemic_category=(
                    "a" if (raw.validated and is_holm_sig and raw.bf_above_threshold)
                    else "b"
                ),
                rejection_reason=rejection,
            )
            results.append(updated)

        return results, holm_result

    # -- Summary table --------------------------------------------------------

    def summarize_results(self, results: List[Layer1Result]) -> str:
        """Formatted summary table for a list of Layer1Results."""
        w = 80
        lines = [
            "=" * w,
            f"SAVEC LAYER 1 -- SUMMARY  v{__version__}",
            f"Author: {__author__}  |  ORCID: {__orcid__}  |  DOI: {__doi__}",
            "=" * w,
            f"{'Divisor':<10} {'p-value':<14} {'BF':<10} {'CV':<8} "
            f"{'Holm':<8} {'RVI':<12} {'Status'}",
            "-" * w,
        ]
        for r in results:
            div = r.pattern_id.split("_")[-1]
            lines.append(
                f"{div:<10} {r.frequentist_pvalue:<14.4e} "
                f"{r.bayes_factor:<10.2f} "
                f"{r.cv_sensitivity:<8.3f} {str(r.holm_significant):<8} "
                f"{r.rvi_score:<12.4f} {'PASS' if r.validated else 'FAIL'}"
            )
        if results:
            r0 = results[0]
            lines.extend([
                "-" * w,
                f"Hardware: TDP~{r0.tdp_watts:.0f} W | "
                f"H2O={r0.water_intensity_used:.1f} L/kWh | "
                f"CodeCarbon={'yes' if r0.codecarbon_used else 'TDP fallback'}",
                "=" * w,
            ])
        return "\n".join(lines)


# =============================================================================
# LAYER 2 -- Access Level Hierarchy
# =============================================================================

class AccessLevel(IntEnum):
    """
    Restriction hierarchy for culturally significant materials.

    Higher integer = more restricted.
    max() over a set of AccessLevel values always selects the most
    protective level, implementing Axiom 2 (pessimistic default).

    Levels
    ------
    PUBLIC        (1) : Unrestricted access.
    INSTITUTIONAL (2) : Community-approved institutional access.
    COMMUNITY     (3) : Community members only.
    RESTRICTED    (4) : Specific authorised individuals only.
    SACRED_SECRET (5) : Maximum restriction. Hard Block applies.
    """
    PUBLIC        = 1
    INSTITUTIONAL = 2
    COMMUNITY     = 3
    RESTRICTED    = 4
    SACRED_SECRET = 5


# =============================================================================
# LAYER 2 -- GovernanceProtocol Data Class
# =============================================================================

@dataclass(frozen=True)
class GovernanceProtocol:
    """
    A single governance rule from one identified authority.

    Parameters
    ----------
    authority_id : str
        Unique identifier of the issuing authority.
    access_level : AccessLevel
        Minimum restriction level this authority mandates.
    can_export : bool
        Whether this authority permits digital export.
    requires_manual_audit : bool
        Whether a human delegate must review before any action.
    description : str
        Free-text rationale (logged in audit trail).
    epistemic_basis : str
        "statistical_layer1" | "expert_rule" | "community_authority".
        Maps to SAVEC Section 5.1 categories a / b / c.
    """
    authority_id:          str
    access_level:          AccessLevel
    can_export:            bool
    requires_manual_audit: bool
    description:           str
    epistemic_basis:       str = "community_authority"


# =============================================================================
# LAYER 2 -- Exceptions
# =============================================================================

class GovernanceConflictError(Exception):
    """
    Raised when the governance engine issues a Hard Block.

    Hard Block conditions:
      (a) No authority identified (governance void), OR
      (b) At least one authority prohibits export AND
          resolved access level >= RESTRICTED.

    This is the computational enforcement of SAVEC Req. 2.2:
    the system halts -- it does not merely warn.
    """
    pass


# =============================================================================
# LAYER 2 -- GovernanceResolver
# =============================================================================

class GovernanceResolver:
    """
    Layer 2 conflict-resolution engine (SAVEC Req. 2.1-2.5).

    Resolution rules  (Axiom 2 -- pessimistic default)
    ---------------------------------------------------
    1. access_level  : max()  -- most restrictive level wins.
    2. can_export    : all()  -- one veto = False.
    3. manual_audit  : any()  -- one request = True.

    These three operations translate the statistical pessimistic default
    (Req. 1.2a) into governance logic.

    Hard Block
    ----------
    Raised automatically when: no protocols, OR
    (not can_export AND resolved_level >= RESTRICTED).

    Audit trail
    -----------
    Every resolution generates a SHA-256 hash stored alongside the full
    log entry. Enables post-hoc verification that no unauthorised export
    occurred (Req. 2.2, CARE Responsibility principle).

    Epistemic prudence flag
    -----------------------
    If any input protocol has epistemic_basis != "statistical_layer1",
    the resolved protocol carries a note in its description. This signals
    to Layer 3 that governance rests on non-validated evidence
    (Section 5.1, category b).

    Parameters
    ----------
    item_id : str
        Unique identifier for the heritage item.
    """

    def __init__(self, item_id: str) -> None:
        self.item_id     = item_id
        self.audit_trail: List[Dict[str, Any]] = []

    def resolve(self, protocols: List[GovernanceProtocol]) -> GovernanceProtocol:
        """
        Resolve conflicts between multiple governance protocols.

        Parameters
        ----------
        protocols : List of GovernanceProtocol from all relevant authorities.

        Returns
        -------
        GovernanceProtocol : Consensus protocol (most restrictive).

        Raises
        ------
        GovernanceConflictError
            If no protocols, or Hard Block condition met.
        """
        if not protocols:
            self._log_void()
            raise GovernanceConflictError(
                f"GovernanceEscalationError [{self.item_id}]: "
                f"No governance authority identified. "
                f"Export blocked pending community engagement. "
                f"(SAVEC Req. 2.2 Hard Block -- governance void.)"
            )

        # Axiom 2 -- pessimistic resolution
        winning_level = max(p.access_level for p in protocols)
        can_export    = all(p.can_export for p in protocols)
        manual_audit  = any(p.requires_manual_audit for p in protocols)

        # Epistemic prudence flag
        non_stat = [p for p in protocols if p.epistemic_basis != "statistical_layer1"]
        prudence_note = (
            f"EPISTEMIC_PRUDENCE: {len(non_stat)}/{len(protocols)} protocol(s) "
            f"lack Layer 1 statistical validation."
            if non_stat else
            "All protocols backed by Layer 1 statistical validation."
        )

        resolved = GovernanceProtocol(
            authority_id          = "SAVEC_CONSENSUS_ENGINE",
            access_level          = winning_level,
            can_export            = can_export,
            requires_manual_audit = manual_audit,
            description           = (
                f"Consensus from {len(protocols)} authority(ies). {prudence_note}"
            ),
            epistemic_basis = (
                "statistical_layer1" if not non_stat else "mixed_epistemic_basis"
            ),
        )

        self._log_resolution(protocols, resolved)

        # Hard Block enforcement (after logging, before returning)
        if not can_export and winning_level >= AccessLevel.RESTRICTED:
            raise GovernanceConflictError(
                f"GovernanceEscalationError [{self.item_id}]: "
                f"Hard Block. Access={winning_level.name}, "
                f"can_export=False. One or more authorities prohibit export "
                f"at RESTRICTED or above. "
                f"(SAVEC Req. 2.2 -- system halts, does not warn.)"
            )

        return resolved

    def _log_resolution(
        self,
        inputs: List[GovernanceProtocol],
        output: GovernanceProtocol,
    ) -> None:
        """Create SHA-256-hashed immutable audit record."""
        entry: Dict[str, Any] = {
            "item_id":             self.item_id,
            "timestamp":           datetime.now(timezone.utc).isoformat(),
            "savec_version":       __version__,
            "author":              __author__,
            "orcid":               __orcid__,
            "n_protocols":         len(inputs),
            "input_authorities":   [p.authority_id for p in inputs],
            "input_bases":         [p.epistemic_basis for p in inputs],
            "resolved_level":      output.access_level.name,
            "can_export":          output.can_export,
            "audit_required":      output.requires_manual_audit,
            "epistemic_basis":     output.epistemic_basis,
            "description":         output.description,
        }
        log_hash = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode("utf-8")
        ).hexdigest()
        self.audit_trail.append({"hash": log_hash, "data": entry})
        logger.info(
            f"GovernanceResolver [{self.item_id}]: "
            f"{output.access_level.name} | SHA-256={log_hash[:12]}..."
        )

    def _log_void(self) -> None:
        """Log a governance-void (no protocols supplied) event."""
        entry: Dict[str, Any] = {
            "item_id":       self.item_id,
            "timestamp":     datetime.now(timezone.utc).isoformat(),
            "savec_version": __version__,
            "event":         "GOVERNANCE_VOID",
            "result":        "HARD_BLOCK",
        }
        log_hash = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode("utf-8")
        ).hexdigest()
        self.audit_trail.append({"hash": log_hash, "data": entry})
        logger.warning(
            f"GovernanceResolver [{self.item_id}]: "
            f"GOVERNANCE_VOID -> Hard Block | SHA-256={log_hash[:12]}..."
        )

    def export_audit_trail(self) -> str:
        """Return the full audit trail as a formatted JSON string."""
        return json.dumps(self.audit_trail, indent=2, ensure_ascii=False)


# =============================================================================
# LAYER 2 -- ContextualRVI (sensitivity-tier-aware threshold)
# =============================================================================

class ContextualRVI:
    """
    Sensitivity-tier-aware RVI threshold modulation.

    The base RVI threshold (0.01) is calibrated for generic validation.
    When an item is classified at a higher sensitivity tier, the epistemic
    obligation to validate rigorously outweighs the obligation to minimise
    energy. ContextualRVI encodes this asymmetry via the Ethical
    Justification multiplier J.

    Asymmetry constraint  (critical)
    ---------------------------------
    J >= 1.0 always. J can only tighten the effective threshold.
    It can NEVER loosen it. An item classified SACRED_SECRET requires
    MORE rigorous validation, not cheaper computation.

    Effective threshold
    -------------------
    rvi_effective = rvi_base_adjusted * J(access_level)

    J values
    --------
    PUBLIC:        1.0  (no modulation)
    INSTITUTIONAL: 1.2
    COMMUNITY:     1.5
    RESTRICTED:    2.0
    SACRED_SECRET: 3.0

    Large-corpus relaxation
    -----------------------
    For n > 10 000 (permutation-testing regime), energy costs scale
    non-linearly. A log-scale relaxation is applied to the base threshold
    BEFORE multiplying by J::

        rvi_base_adjusted = rvi_base / (1 + log10(n / 10_000))

    The J multiplier is applied on top. The effective threshold can never
    fall below rvi_base * 0.5 (safety floor).

    Parameters
    ----------
    base_threshold : float  -- Default: DEFAULT_RVI_THRESHOLD (0.01).
    """

    _J_TABLE: Dict[int, float] = {
        AccessLevel.PUBLIC:        1.0,
        AccessLevel.INSTITUTIONAL: 1.2,
        AccessLevel.COMMUNITY:     1.5,
        AccessLevel.RESTRICTED:    2.0,
        AccessLevel.SACRED_SECRET: 3.0,
    }

    def __init__(self, base_threshold: float = DEFAULT_RVI_THRESHOLD) -> None:
        if base_threshold <= 0:
            raise ValueError(f"base_threshold must be positive; got {base_threshold}.")
        self.base_threshold = base_threshold

    def j_multiplier(self, access_level: AccessLevel) -> float:
        """Return J >= 1.0 for the given tier."""
        return self._J_TABLE.get(int(access_level), 1.0)

    def effective_threshold(
        self,
        access_level: AccessLevel,
        n_corpus:     int = 0,
    ) -> float:
        """
        Compute the effective RVI threshold for a given context.

        Parameters
        ----------
        access_level : Governance tier of the item.
        n_corpus     : Corpus size (enables log-scale base relaxation).

        Returns
        -------
        float : Effective threshold >= base_threshold * 0.5.
        """
        base = self.base_threshold

        if n_corpus > 10_000:
            relaxation = 1.0 + math.log10(n_corpus / 10_000)
            base = base / relaxation

        j   = self.j_multiplier(access_level)
        eff = base * j

        # Safety floor: effective threshold can never fall below 50% of base
        return max(eff, self.base_threshold * 0.5)

    def evaluate(
        self,
        rvi_score:    float,
        access_level: AccessLevel,
        n_corpus:     int = 0,
    ) -> Dict[str, Any]:
        """
        Evaluate an RVI score against the contextual threshold.

        Parameters
        ----------
        rvi_score    : RVI computed by RVICalculator.
        access_level : Governance tier.
        n_corpus     : Corpus size.

        Returns
        -------
        dict : rvi_score, access_level, j_multiplier, effective_threshold,
               base_threshold, n_corpus, passes, margin, interpretation.
        """
        eff    = self.effective_threshold(access_level, n_corpus)
        j      = self.j_multiplier(access_level)
        passes = (rvi_score == float("inf")) or (rvi_score >= eff)
        margin = rvi_score - eff if rvi_score != float("inf") else float("inf")

        if passes:
            interp = (
                f"RVI={rvi_score:.5f} >= threshold {eff:.5f} "
                f"(J={j:.1f} x base={self.base_threshold:.3f}, "
                f"tier={access_level.name}). PASS."
            )
        else:
            interp = (
                f"RVI={rvi_score:.5f} < threshold {eff:.5f} "
                f"(J={j:.1f} x base={self.base_threshold:.3f}, "
                f"tier={access_level.name}). "
                f"Deficit={abs(margin):.5f}. FAIL -- "
                f"epistemic investment insufficient for sensitivity tier."
            )

        return {
            "rvi_score":           rvi_score,
            "access_level":        access_level.name,
            "j_multiplier":        j,
            "effective_threshold": eff,
            "base_threshold":      self.base_threshold,
            "n_corpus":            n_corpus,
            "passes":              passes,
            "margin":              margin,
            "interpretation":      interp,
        }


# =============================================================================
# LAYER 2 -- EpistemicBridgeResult + resolve_layer1_to_layer2()
# =============================================================================

@dataclass(frozen=True)
class EpistemicBridgeResult:
    """
    Structured Layer 1 -> Layer 2 hand-off record.

    Combined confidence score
    -------------------------
    Asymmetric by design:
    - Category a + clear governance -> highest confidence.
    - Category b -> capped at 0.5 regardless of governance clarity.
    - Hard Block (governance void) -> 0.0.

    This asymmetry prevents a strong governance record from
    compensating for statistically unvalidated evidence.

    Parameters
    ----------
    layer1_result : Layer1Result
    governance_protocol : GovernanceProtocol | None
        None if Hard Block was raised.
    governance_error : str
        GovernanceConflictError message, or empty string.
    hard_block : bool
    contextual_rvi_eval : Dict[str, Any]
        Output of ContextualRVI.evaluate().
    combined_confidence : float  -- [0, 1].
    epistemic_note : str
    resolved_at : str  -- ISO 8601 UTC.
    savec_version : str
    """
    layer1_result:       Layer1Result
    governance_protocol: Optional[GovernanceProtocol]
    governance_error:    str
    hard_block:          bool
    contextual_rvi_eval: Dict[str, Any]
    combined_confidence: float
    epistemic_note:      str
    resolved_at:         str
    savec_version:       str

    @property
    def summary(self) -> str:
        """Human-readable hand-off summary."""
        if self.hard_block:
            gov_status = f"HARD BLOCK -- {self.governance_error}"
        else:
            p = self.governance_protocol
            gov_status = (
                f"{p.access_level.name} | "
                f"export={'YES' if p.can_export else 'NO'} | "
                f"audit={'YES' if p.requires_manual_audit else 'NO'}"
            )
        outcome = (
            "PASS"
            if (not self.hard_block and self.layer1_result.validated)
            else "BLOCKED/REJECTED"
        )
        return "\n".join([
            f"SAVEC EPISTEMIC BRIDGE v{self.savec_version} -- {outcome}",
            f"  Resolved at:         {self.resolved_at}",
            f"  Layer 1 validated:   {self.layer1_result.validated} "
            f"(BF={self.layer1_result.bayes_factor:.2f}, "
            f"cat={self.layer1_result.epistemic_category})",
            f"  Layer 2 governance:  {gov_status}",
            f"  RVI (contextual):    "
            f"{self.contextual_rvi_eval.get('interpretation', 'N/A')}",
            f"  Combined confidence: {self.combined_confidence:.3f}",
            f"  Epistemic note:      {self.epistemic_note}",
        ])


def resolve_layer1_to_layer2(
    layer1_result:      Layer1Result,
    protocols:          List[GovernanceProtocol],
    access_level:       AccessLevel,
    n_corpus:           int   = 0,
    base_rvi_threshold: float = DEFAULT_RVI_THRESHOLD,
) -> EpistemicBridgeResult:
    """
    Formalise the Layer 1 -> Layer 2 dependency (SAVEC Section 5.1).

    The governance decision is only as sound as the Layer 1 classification
    that triggered it. This function carries that dependency explicitly
    into the combined_confidence score and epistemic_note.

    Parameters
    ----------
    layer1_result       : Output of Layer1Validator.validate().
    protocols           : GovernanceProtocol list from relevant authorities.
    access_level        : Governance tier for ContextualRVI modulation.
    n_corpus            : Corpus size (log-scale RVI relaxation if > 10 000).
    base_rvi_threshold  : Base threshold before J modulation.

    Returns
    -------
    EpistemicBridgeResult : Immutable hand-off record.
    """
    resolved_at = datetime.now(timezone.utc).isoformat()
    crvi        = ContextualRVI(base_rvi_threshold)
    rvi_eval    = crvi.evaluate(layer1_result.rvi_score, access_level, n_corpus)
    resolver    = GovernanceResolver(layer1_result.pattern_id)

    gov_protocol: Optional[GovernanceProtocol] = None
    gov_error    = ""
    hard_block   = False

    try:
        gov_protocol = resolver.resolve(protocols)
    except GovernanceConflictError as exc:
        gov_error  = str(exc)
        hard_block = True
        logger.warning(gov_error)

    # Combined confidence -- asymmetric design
    bf = layer1_result.bayes_factor
    l1_conf = (bf / (bf + 1.0)) if bf != float("inf") else 1.0

    if hard_block:
        combined = 0.0
    elif layer1_result.epistemic_category == "a":
        gov_clarity = (
            1.0
            if (gov_protocol and gov_protocol.epistemic_basis == "statistical_layer1")
            else 0.7
        )
        combined = min(l1_conf * gov_clarity, 1.0)
    else:
        # Category b: cap at 0.5 regardless of governance quality
        combined = min(l1_conf * 0.5, 0.5)

    # Epistemic note
    if hard_block:
        note = (
            "Layer 2 cannot proceed: governance void or Hard Block. "
            "Item requires community engagement before any processing."
        )
    elif layer1_result.epistemic_category == "b":
        note = (
            "Layer 1 did not statistically validate this pattern "
            "(epistemic category b). Layer 2 governance rests on expert "
            "rule or community authority. Epistemic prudence flag active: "
            "automated dissemination suppressed."
        )
    else:
        note = (
            "Layer 1 statistical validation confirmed (category a). "
            "Layer 2 governance decision is epistemically grounded."
        )

    return EpistemicBridgeResult(
        layer1_result       = layer1_result,
        governance_protocol = gov_protocol,
        governance_error    = gov_error,
        hard_block          = hard_block,
        contextual_rvi_eval = rvi_eval,
        combined_confidence = round(combined, 4),
        epistemic_note      = note,
        resolved_at         = resolved_at,
        savec_version       = __version__,
    )


# =============================================================================
# Demonstration & Benchmark
# =============================================================================

def main() -> int:
    """
    Demonstrate Layer 1 optimisations and Layer 2 governance bridge.

    Returns 0 on success.
    """
    w = 70
    print("=" * w)
    print(f"SAVEC INTEGRATION ENGINE  v{__version__}")
    print(f"Author:        {__author__}")
    print(f"ORCID:         {__orcid__}")
    print(f"DOI:           {__doi__}")
    print(f"CodeCarbon:    {'available' if CODECARBON_AVAILABLE else 'TDP fallback'}")
    print(f"TDP estimate:  {DynamicTDP.estimate_tdp():.0f} W")
    print(f"Water intens.: {WaterIntensityProvider().get_intensity():.1f} L/kWh")
    print("=" * w)

    rng       = np.random.default_rng(DEFAULT_SEED)
    validator = Layer1Validator()

    # -- Demo 1: Log-BF numerical stability -----------------------------------
    print(f"\n{'─' * 50}")
    print("OPT 1: Log-Bayes Factor -- Numerical Stability")
    print(f"{'─' * 50}")
    for name, k, n, p0 in [
        ("n=100",          5,      100,   1 / 7),
        ("n=500",         80,      500,   1 / 7),
        ("n=10 000",   1_500,   10_000,   1 / 7),
        ("n=100 000",  15_000, 100_000,   1 / 7),
    ]:
        bf, log_bf = validator.bf.compute(k, n, p0)
        interp     = validator.bf.interpret(bf, log_bf)
        try:
            naive_str = f"{stats.beta.pdf(p0, 1, 1) / stats.beta.pdf(p0, k + 1, n - k + 1):.6e}"
        except Exception:
            naive_str = "OVERFLOW"
        print(f"  {name}: log BF={log_bf:.4f}, BF={bf:.2e}, naive={naive_str}")
        print(f"    -> {interp}")

    # -- Demo 2: Vectorised jackknife benchmark --------------------------------
    print(f"\n{'─' * 50}")
    print("OPT 2: Vectorised Jackknife -- Speed Benchmark")
    print(f"{'─' * 50}")
    for n_bench in [500, 5_000, 50_000]:
        vals = rng.integers(1, 1_000, n_bench)

        t0 = time.perf_counter()
        cv_vec, _ = validator.sensitivity.compute(vals, 7)
        t_vec = (time.perf_counter() - t0) * 1_000.0

        t0 = time.perf_counter()
        m_s, props_loop = max(n_bench // 2, 10), []
        for _ in range(100):
            idx = rng.choice(n_bench, size=m_s, replace=False)
            props_loop.append(int(np.sum(vals[idx] % 7 == 0)) / m_s)
        mean_p  = np.mean(props_loop)
        t_loop  = (time.perf_counter() - t0) * 1_000.0
        speedup = t_loop / t_vec if t_vec > 0 else float("inf")
        print(
            f"  n={n_bench:>7,}: vec={t_vec:6.2f} ms, "
            f"loop={t_loop:6.2f} ms, speedup={speedup:.1f}x, CV={cv_vec:.4f}"
        )

    # -- Demo 3: Holm-Bonferroni vs Bonferroni --------------------------------
    print(f"\n{'─' * 50}")
    print("OPT 3: Holm-Bonferroni -- Power Comparison")
    print(f"{'─' * 50}")
    sim_p    = [0.001, 0.04, 0.08, 0.15, 0.60]
    sim_name = ["div_7", "div_12", "div_26", "div_30", "div_60"]
    hr       = validator.holm.correct(sim_p, sim_name)
    print(f"  Bonferroni rejects: {hr['bonferroni_rejected']} / "
          f"Holm rejects: {hr['holm_rejected']} / "
          f"Power gain: +{hr['power_gain']}")
    for step in hr["steps"]:
        print(f"    {step}")

    # -- Demo 4: Single-divisor validation + RVI --------------------------------
    print(f"\n{'─' * 50}")
    print("DEMO 4: Single-Divisor Validation + Dynamic RVI")
    print(f"{'─' * 50}")
    base   = rng.integers(1, 1_000, 500)
    extras = rng.integers(1, 143, 50) * 7
    gv     = np.concatenate([base, extras])
    result = validator.validate(
        pattern_id="demo_genesis_div7",
        observed_values=gv,
        divisor=7,
    )
    print(result.summary)

    # -- Demo 5: Multi-divisor + Holm ------------------------------------------
    print(f"\n{'─' * 50}")
    print("DEMO 5: Multi-Divisor + Holm-Bonferroni")
    print(f"{'─' * 50}")
    results, holm_out = validator.validate_multiple("demo_genesis", gv)
    print(
        f"  Holm: {holm_out['holm_rejected']}/{holm_out['n_tests']} rejected "
        f"(power gain: +{holm_out['power_gain']})\n"
    )
    print(validator.summarize_results(results))

    # -- Demo 6: GovernanceResolver -------------------------------------------
    print(f"\n{'─' * 50}")
    print("DEMO 6: Layer 2 -- GovernanceResolver")
    print(f"{'─' * 50}")

    # Case A: Two authorities -- RESTRICTED + no export -> Hard Block
    protocols_a = [
        GovernanceProtocol(
            authority_id="Wiradjuri_Council",
            access_level=AccessLevel.COMMUNITY,
            can_export=False,
            requires_manual_audit=True,
            description="Ceremonial site -- community members only.",
            epistemic_basis="community_authority",
        ),
        GovernanceProtocol(
            authority_id="AIATSIS",
            access_level=AccessLevel.RESTRICTED,
            can_export=False,
            requires_manual_audit=True,
            description="Institutional restriction pending consent.",
            epistemic_basis="expert_rule",
        ),
    ]
    print("\n  Case A: Wiradjuri site (RESTRICTED + export=False)")
    resolver_a = GovernanceResolver("wiradjuri_ceremonial_001")
    try:
        resolver_a.resolve(protocols_a)
    except GovernanceConflictError as e:
        print(f"  HARD BLOCK: {str(e)[:100]}...")
    if resolver_a.audit_trail:
        print(f"  SHA-256: {resolver_a.audit_trail[-1]['hash'][:32]}...")

    # Case B: Governance void
    print("\n  Case B: Griot recording (no authority identified)")
    resolver_b = GovernanceResolver("griot_recording_1970s")
    try:
        resolver_b.resolve([])
    except GovernanceConflictError as e:
        print(f"  HARD BLOCK (void): {str(e)[:100]}...")

    # -- Demo 7: ContextualRVI tier modulation ---------------------------------
    print(f"\n{'─' * 50}")
    print("DEMO 7: ContextualRVI -- Tier-Adaptive Threshold")
    print(f"{'─' * 50}")
    crvi = ContextualRVI(base_threshold=DEFAULT_RVI_THRESHOLD)
    for level in AccessLevel:
        ev  = crvi.evaluate(0.025, level)
        tag = "PASS" if ev["passes"] else "FAIL"
        print(
            f"  {level.name:<14}: J={ev['j_multiplier']:.1f}  "
            f"threshold={ev['effective_threshold']:.4f}  RVI=0.025 -> {tag}"
        )

    # -- Demo 8: EpistemicBridge (Layer 1 -> Layer 2) --------------------------
    print(f"\n{'─' * 50}")
    print("DEMO 8: EpistemicBridge -- Layer 1 -> Layer 2 Hand-off")
    print(f"{'─' * 50}")
    bridge = resolve_layer1_to_layer2(
        layer1_result=results[0],
        protocols=[
            GovernanceProtocol(
                authority_id="Scholarly_Community",
                access_level=AccessLevel.PUBLIC,
                can_export=True,
                requires_manual_audit=False,
                description="Open scholarly corpus -- no sovereignty concerns.",
                epistemic_basis="statistical_layer1",
            )
        ],
        access_level=AccessLevel.PUBLIC,
        n_corpus=len(gv),
    )
    print(bridge.summary)

    print(f"\n{'=' * w}")
    print("All demos completed successfully.")
    print(f"{'=' * w}")
    return 0


if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s | %(name)s | %(message)s",
    )
    sys.exit(main())
