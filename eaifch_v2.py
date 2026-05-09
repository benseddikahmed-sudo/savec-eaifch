#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EAIFCH 2.0 — Ethical AI Framework for Cultural Heritage
========================================================

Module 0 : Governance & Taxonomy Management
Module 7 : AI Oversight & Human-in-the-Loop

Design Principle: "Maximum community authority with minimum computational privilege."

----------------------------------------------------------------------
PROVENANCE & CITATION
----------------------------------------------------------------------
Author:         Ahmed Benseddik
ORCID:          0009-0005-6308-8171
Affiliation:    Independent Researcher
DOI:            10.17605/OSF.IO/Y8VBU
OSF:            osf.io/y8vbu
License:        MIT
Date:           2026-05
Status:         Prototype

----------------------------------------------------------------------
DEPENDENCY
----------------------------------------------------------------------
Requires savec_integration_engine_v31.py in the same directory.

----------------------------------------------------------------------
VERSION HISTORY
----------------------------------------------------------------------
v1.0.0  (2024-2025)  Original EAIFCH: six modules, GovernanceEscalation
                     Error Hard Block, CARE operationalisation, Green AI
                     metrics (< 0.002g CO2 / 10 000 assessments).

v2.0.0  (2026-05)    MODULE 0: TaxonomyVersion (semantic versioning,
                     Git-like immutability), CommunityFork (community
                     autonomy layer), BooleanOverrideRule (auditable
                     community exceptions, upward-only elevation),
                     ConflictResolver (3-level cascade).
                     MODULE 7: AIBsandbox (ethical LLM bounding),
                     ConstitutionalRules CR-1 to CR-5, LLMOutputValidator,
                     LLMAdapter (abstract interface), SparkingSessionRecord.
                     epistemic_basis: 5-value enum with confidence_discount.
                     Sunset mechanism: 5-state GovernanceProtocol lifecycle.
                     datetime.now(timezone.utc) throughout (Py 3.12 compat).

----------------------------------------------------------------------
EAIFCH 2.0 REQUIREMENTS IMPLEMENTED
----------------------------------------------------------------------
M0-R1  TaxonomyVersion: semantic versioning, immutability, SHA-256.
M0-R2  CommunityFork: community autonomy, upward-only overrides.
M0-R3  BooleanOverrideRule: auditable named exception rules.
M0-R4  ConflictResolver: 3-level cascade with Hard Block provisions.
M7-R1  AIBsandbox: task whitelist/blacklist enforcement.
M7-R2  ConstitutionalRules CR-1 to CR-5: inviolable constraints.
M7-R3  LLMOutputValidator: human validation workflow, confidence_discount.
M7-R4  SparkingSessionRecord: traced collaborative session.
M7-R5  AIRefusalRecord: archived documentation of blocked tasks.
SPEC-D1 Fuzzy logic rejected; BooleanOverrideRule retained (auditable).
SPEC-D2 epistemic_basis: 5-value enum with confidence_discount table.
SPEC-D3 Sunset mechanism: 5-state lifecycle for GovernanceProtocol.
SPEC-D4 Non-delegation axiom: no algorithm produces a final governance
        decision without identified, timestamped human action.
"""

from __future__ import annotations

# =============================================================================
# Module-level metadata  (single source of truth)
# =============================================================================

__version__     = "2.0.0"
__author__      = "Ahmed Benseddik"
__orcid__       = "0009-0005-6308-8171"
__affiliation__ = "Independent Researcher"
__doi__         = "10.17605/OSF.IO/Y8VBU"
__osf__         = "osf.io/y8vbu"
__license__     = "MIT"
__date__        = "2026-05"
__status__      = "Prototype"

MODULE_METADATA: dict = {
    "name":        "eaifch_v2",
    "version":     __version__,
    "author":      __author__,
    "orcid":       __orcid__,
    "affiliation": __affiliation__,
    "doi":         __doi__,
    "osf":         __osf__,
    "license":     __license__,
    "date":        __date__,
    "status":      __status__,
    "framework":   "EAIFCH 2.0 -- Ethical AI Framework for Cultural Heritage",
    "modules":     "Module 0 (Governance & Taxonomy) + Module 7 (AI Oversight)",
    "depends_on":  "savec_integration_engine_v31.py",
    "journal":     "Journal of Cultural Analytics",
    "design_principle": "Maximum community authority with minimum computational privilege",
}

# =============================================================================
# Standard library
# =============================================================================

import abc
import dataclasses
import hashlib
import json
import logging
import warnings
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# SAVEC v3.1 dependency
# =============================================================================

try:
    from savec_integration_engine_v31 import (
        AccessLevel,
        GovernanceProtocol,
        GovernanceConflictError,
        GovernanceResolver,
        EpistemicBridgeResult,
        resolve_layer1_to_layer2,
        Layer1Result,
        DEFAULT_RVI_THRESHOLD,
        __version__ as SAVEC_VERSION,
    )
    SAVEC_AVAILABLE = True
except ImportError:
    SAVEC_AVAILABLE = False
    SAVEC_VERSION   = "not found"
    warnings.warn(
        "savec_integration_engine_v31.py not found.\n"
        "Place it alongside this file for full SAVEC integration.\n"
        "Module 0 and Module 7 run in stub mode without it.",
        UserWarning, stacklevel=2,
    )
    from enum import IntEnum

    class AccessLevel(IntEnum):  # type: ignore[no-redef]
        PUBLIC=1; INSTITUTIONAL=2; COMMUNITY=3; RESTRICTED=4; SACRED_SECRET=5

    class GovernanceConflictError(Exception): pass  # type: ignore[no-redef]

    @dataclass(frozen=True)
    class GovernanceProtocol:  # type: ignore[no-redef]
        authority_id: str; access_level: "AccessLevel"
        can_export: bool; requires_manual_audit: bool
        description: str; epistemic_basis: str = "community_authority"

    DEFAULT_RVI_THRESHOLD = 0.01
    Layer1Result = None  # type: ignore[assignment,misc]

# =============================================================================
# Logging
# =============================================================================

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# =============================================================================
# Constants
# =============================================================================

DEFAULT_SUNSET_MONTHS     = 24
DEFAULT_REVALIDATION_DAYS = 90

DEFAULT_CONFIDENCE_DISCOUNT_AI = 0.15

# Epistemic basis values (SPEC-D2)
EPISTEMIC_BASIS_VALUES = (
    "statistical_layer1",
    "expert_human",
    "ai_assisted_human_validated",
    "ai_generated_unvalidated",
    "community_authority",
)

CONFIDENCE_DISCOUNT: Dict[str, float] = {
    "statistical_layer1":          0.00,
    "expert_human":                0.00,
    "ai_assisted_human_validated": DEFAULT_CONFIDENCE_DISCOUNT_AI,
    "ai_generated_unvalidated":    float("inf"),  # Blocked
    "community_authority":         0.00,
}

# Module 7 task lists
PERMITTED_TASKS = frozenset([
    "preliminary_sensitivity_classification",
    "metadata_summary_non_sensitive",
    "pattern_candidate_detection_phase1",
    "contextual_translation",
    "research_exploration",
    "governance_deliberation",
    "confidential_sparring",
])

REFUSED_TASKS = frozenset([
    "theological_interpretation",
    "spiritual_interpretation",
    "sacred_content_generation",
    "final_governance_decision",
    "community_authority_evaluation",
    "taxonomy_direct_modification",
    "fork_direct_modification",
    "generate_ip_claim",
    "claim_ownership",
    "publish_without_attribution",
    "interpret",
    "paraphrase",
    "summarise_content",
    "translate_sacred",
])


def validate_epistemic_basis(basis: str) -> bool:
    return basis in EPISTEMIC_BASIS_VALUES

def can_feed_layer2(basis: str) -> bool:
    return basis != "ai_generated_unvalidated"

def get_confidence_discount(basis: str) -> float:
    return CONFIDENCE_DISCOUNT.get(basis, 0.0)


# =============================================================================
# MODULE 0 -- 0.1: TaxonomyVersion + TaxonomyRegistry
# =============================================================================

@dataclass(frozen=True)
class TaxonomyVersion:
    """
    Immutable SHA-256-signed snapshot of the central taxonomy.

    Versioning: MAJOR.MINOR.PATCH (semver).
    MAJOR: AccessLevel structure changed.
    MINOR: Indicators added or removed.
    PATCH: Labels, legal refs, language additions.

    Once registered, a version cannot be modified.
    Any change creates a new version.
    """
    major:          int
    minor:          int
    patch:          int
    published_at:   str
    published_by:   str
    description:    str
    indicators:     Dict[str, Any]
    access_levels:  Tuple[str, ...]
    change_type:    str           # "MAJOR" | "MINOR" | "PATCH"
    parent_version: Optional[str]
    audit_hash:     str = ""

    @property
    def version_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def is_compatible_with(self, other: "TaxonomyVersion") -> bool:
        """Backward-compatible if MAJOR versions match."""
        return self.major == other.major

    def compute_hash(self) -> str:
        d = {
            "version":        self.version_string,
            "published_at":   self.published_at,
            "published_by":   self.published_by,
            "description":    self.description,
            "indicators":     self.indicators,
            "access_levels":  list(self.access_levels),
            "change_type":    self.change_type,
            "parent_version": self.parent_version,
        }
        return hashlib.sha256(
            json.dumps(d, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def summary(self) -> str:
        return (
            f"v{self.version_string} ({self.change_type}) | "
            f"{self.published_at[:10]} by {self.published_by} | "
            f"{len(self.indicators)} indicators | "
            f"SHA-256: {self.audit_hash[:16]}..."
        )


class TaxonomyRegistry:
    """
    Append-only registry of TaxonomyVersions.

    Enforces semver increment rules and version immutability.
    Provides migration reports for backward-compatibility validation.
    """

    def __init__(self, initial_version: Optional[TaxonomyVersion] = None) -> None:
        self._versions: List[TaxonomyVersion] = []
        if initial_version is not None:
            signed = self._sign(initial_version)
            self._versions.append(signed)
            logger.info(f"TaxonomyRegistry: root {signed.version_string} registered.")

    def register(self, version: TaxonomyVersion) -> TaxonomyVersion:
        """
        Register a new version. Validates parent reference and semver increment.

        Raises ValueError on constraint violation.
        Returns the signed version (audit_hash populated).
        """
        if not self._versions:
            signed = self._sign(version)
            self._versions.append(signed)
            return signed

        current = self._versions[-1]

        if version.parent_version != current.version_string:
            raise ValueError(
                f"Parent mismatch: expected '{current.version_string}', "
                f"got '{version.parent_version}'."
            )
        self._validate_increment(current, version)
        signed = self._sign(version)
        self._versions.append(signed)
        logger.info(
            f"TaxonomyRegistry: v{signed.version_string} "
            f"({signed.change_type}) registered."
        )
        return signed

    def _validate_increment(
        self, current: TaxonomyVersion, new: TaxonomyVersion
    ) -> None:
        c = (current.major, current.minor, current.patch)
        n = (new.major,     new.minor,     new.patch)
        valid = (
            n == (c[0]+1, 0,      0     ) or   # MAJOR
            n == (c[0],   c[1]+1, 0     ) or   # MINOR
            n == (c[0],   c[1],   c[2]+1)       # PATCH
        )
        if not valid:
            raise ValueError(
                f"Invalid semver increment: {current.version_string} -> "
                f"{new.version_string}."
            )

    @staticmethod
    def _sign(v: TaxonomyVersion) -> TaxonomyVersion:
        return dataclasses.replace(v, audit_hash=v.compute_hash())

    @property
    def current(self) -> Optional[TaxonomyVersion]:
        return self._versions[-1] if self._versions else None

    @property
    def history(self) -> List[TaxonomyVersion]:
        return list(self._versions)

    def get_version(self, vs: str) -> Optional[TaxonomyVersion]:
        for v in self._versions:
            if v.version_string == vs:
                return v
        return None

    def migration_report(self, from_vs: str, to_vs: str) -> Dict[str, Any]:
        """
        Document indicator additions, removals, weight changes between versions.
        Required for backward-compatibility validation (M0-R1).
        """
        vf = self.get_version(from_vs)
        vt = self.get_version(to_vs)
        if vf is None or vt is None:
            raise ValueError(f"Version(s) not found: '{from_vs}', '{to_vs}'.")

        ind_f = set(vf.indicators)
        ind_t = set(vt.indicators)
        added   = sorted(ind_t - ind_f)
        removed = sorted(ind_f - ind_t)
        weight_changes = {
            k: {"from": vf.indicators[k].get("weight"), "to": vt.indicators[k].get("weight")}
            for k in (ind_f & ind_t)
            if vf.indicators[k].get("weight") != vt.indicators[k].get("weight")
        }
        change_types, recording = [], False
        for v in self._versions:
            if v.version_string == from_vs:
                recording = True; continue
            if recording:
                change_types.append(v.change_type)
            if v.version_string == to_vs:
                break
        return {
            "from_version":       from_vs,
            "to_version":         to_vs,
            "indicators_added":   added,
            "indicators_removed": removed,
            "weight_changes":     weight_changes,
            "is_compatible":      vf.is_compatible_with(vt),
            "change_types":       change_types,
            "eaifch_version":     __version__,
        }


# =============================================================================
# MODULE 0 -- 0.2: BooleanOverrideRule  (SPEC-D1)
# =============================================================================

@dataclass(frozen=True)
class BooleanOverrideRule:
    """
    Named, auditable exception rule that ELEVATES sensitivity tier.

    Design rationale (SPEC-D1 -- Fuzzy logic rejected):
    Fuzzy outputs are difficult to audit: "your indicators created
    exponential sensitivity" is not defensible when a community
    challenges a classification. BooleanOverrideRule is:
      - Named (rule_id)
      - Versioned with its CommunityFork
      - Audited in every decision it influences
      - Revocable by the signing authority

    Asymmetry constraint (inviolable):
    A rule can ONLY elevate sensitivity, never lower it.
    Downward rules are silently ignored with a warning (enforced in
    CommunityFork.apply_overrides).

    Parameters
    ----------
    rule_id              : Unique identifier within the fork.
    description          : Human-readable description.
    trigger_indicators   : ALL must be active to trigger (AND logic).
    override_access_level: Tier assigned when triggered (must be >=
                           computed level at application time).
    signed_by            : Signing community delegate.
    created_at           : ISO 8601 UTC.
    languages            : {lang_code -> description translation}.
    """
    rule_id:               str
    description:           str
    trigger_indicators:    Tuple[str, ...]
    override_access_level: AccessLevel
    signed_by:             str
    created_at:            str
    languages:             Dict[str, str] = field(default_factory=dict)

    def evaluate(self, active_indicators: List[str]) -> bool:
        """True if ALL trigger_indicators are active."""
        return all(i in active_indicators for i in self.trigger_indicators)

    @property
    def audit_entry(self) -> Dict[str, Any]:
        return {
            "rule_id":               self.rule_id,
            "override_access_level": self.override_access_level.name,
            "trigger_indicators":    list(self.trigger_indicators),
            "signed_by":             self.signed_by,
            "created_at":            self.created_at,
            "eaifch_version":        __version__,
        }


# =============================================================================
# MODULE 0 -- 0.3: CommunityFork
# =============================================================================

@dataclass
class CommunityFork:
    """
    Community autonomy layer superimposed on the central taxonomy.

    A fork does NOT overwrite the central taxonomy -- it adds
    community-specific overrides and weight adjustments.

    Parameters
    ----------
    fork_id            : Unique identifier (community + timestamp slug).
    community_id       : Stable community identifier.
    base_version       : Parent TaxonomyVersion string.
    signed_by          : Signing community delegate.
    valid_from         : ISO 8601 UTC start of validity.
    valid_until        : ISO 8601 UTC end (None = indefinite).
    overrides          : BooleanOverrideRules (upward-only).
    weight_adjustments : {indicator -> new_weight}.
    language_additions : {indicator -> {lang_code -> label}}.
    description        : Fork purpose description.
    audit_hash         : SHA-256 at signing time.
    """
    fork_id:            str
    community_id:       str
    base_version:       str
    signed_by:          str
    valid_from:         str
    valid_until:        Optional[str]
    overrides:          List[BooleanOverrideRule]
    weight_adjustments: Dict[str, float]
    language_additions: Dict[str, Dict[str, str]]
    description:        str
    audit_hash:         str = ""

    def validate(self, registry: TaxonomyRegistry) -> List[str]:
        """
        Validate fork against the registry.

        Returns list of error strings (empty = valid).
        """
        errors: List[str] = []
        base = registry.get_version(self.base_version)
        if base is None:
            errors.append(f"base_version '{self.base_version}' not in registry.")
            return errors

        known = set(base.indicators)
        for ind in self.weight_adjustments:
            if ind not in known:
                errors.append(f"weight_adjustment: unknown indicator '{ind}'.")
        for rule in self.overrides:
            for ind in rule.trigger_indicators:
                if ind not in known:
                    errors.append(
                        f"Rule '{rule.rule_id}': unknown trigger '{ind}'."
                    )
        return errors

    def sign(self) -> "CommunityFork":
        """Compute and set audit_hash. Returns self."""
        d = {
            "fork_id":            self.fork_id,
            "community_id":       self.community_id,
            "base_version":       self.base_version,
            "signed_by":          self.signed_by,
            "valid_from":         self.valid_from,
            "valid_until":        self.valid_until,
            "overrides":          [r.rule_id for r in self.overrides],
            "weight_adjustments": self.weight_adjustments,
            "description":        self.description,
            "eaifch_version":     __version__,
        }
        self.audit_hash = hashlib.sha256(
            json.dumps(d, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        logger.info(
            f"CommunityFork '{self.fork_id}' signed | "
            f"SHA-256: {self.audit_hash[:16]}..."
        )
        return self

    def is_active(self, at: Optional[datetime] = None) -> bool:
        now = at or datetime.now(timezone.utc)
        try:
            if now < datetime.fromisoformat(self.valid_from):
                return False
            if self.valid_until and now > datetime.fromisoformat(self.valid_until):
                return False
        except (ValueError, TypeError):
            return False
        return True

    def apply_overrides(
        self,
        computed_level:    AccessLevel,
        active_indicators: List[str],
    ) -> Tuple[AccessLevel, List[str]]:
        """
        Apply BooleanOverrideRules to the additively computed level.

        Asymmetry constraint enforced: result >= computed_level always.
        Downward rules are ignored with a warning.

        Returns (final_level, triggered_rule_ids).
        """
        current:   AccessLevel = computed_level
        triggered: List[str]   = []

        for rule in self.overrides:
            if rule.evaluate(active_indicators):
                if rule.override_access_level >= current:
                    current = rule.override_access_level
                    triggered.append(rule.rule_id)
                    logger.debug(
                        f"Rule '{rule.rule_id}' triggered: "
                        f"{computed_level.name} -> {current.name}."
                    )
                else:
                    logger.warning(
                        f"Rule '{rule.rule_id}' attempted to LOWER "
                        f"sensitivity ({computed_level.name} -> "
                        f"{rule.override_access_level.name}). "
                        f"Asymmetry constraint enforced -- ignored."
                    )
        return current, triggered

    def get_label(self, indicator: str, language: str) -> Optional[str]:
        return self.language_additions.get(indicator, {}).get(language)


# =============================================================================
# MODULE 0 -- 0.4: GovernanceProtocolRecord + Sunset lifecycle (SPEC-D3)
# =============================================================================

class ProtocolLifecycleState(Enum):
    """
    Five-state lifecycle for GovernanceProtocol instances.

    ACTIVE               : Signed, within validity period.
    PENDING_REVALIDATION : sunset_date reached; Hard Block maintained;
                           90-day revalidation window opened.
    EXPIRED              : Revalidation window elapsed; Hard Block
                           permanent until explicit resolution.
    RENEWED              : Revalidation completed; back to ACTIVE.
    PERMANENT            : Declared by community authority (sunset=None).
                           Requires archived justification + succession doc.
    """
    ACTIVE               = "ACTIVE"
    PENDING_REVALIDATION = "PENDING_REVALIDATION"
    EXPIRED              = "EXPIRED"
    RENEWED              = "RENEWED"
    PERMANENT            = "PERMANENT"


@dataclass
class GovernanceProtocolRecord:
    """
    A GovernanceProtocol wrapped with lifecycle metadata.

    Parameters
    ----------
    protocol                : SAVEC v3.1 GovernanceProtocol.
    item_id                 : Heritage item identifier.
    created_at              : ISO 8601 UTC.
    sunset_date             : ISO 8601 UTC expiry. None = PERMANENT.
    revalidation_deadline   : Set when PENDING_REVALIDATION entered.
    state                   : ProtocolLifecycleState.
    permanent_justification : Required for PERMANENT state.
    succession_authority    : Who holds authority if community restructures.
    renewal_history         : Log of renewals.
    audit_trail             : SHA-256-hashed state transitions.
    """
    protocol:                GovernanceProtocol
    item_id:                 str
    created_at:              str
    sunset_date:             Optional[str]
    revalidation_deadline:   Optional[str]
    state:                   ProtocolLifecycleState
    permanent_justification: str
    succession_authority:    str
    renewal_history:         List[Dict[str, str]]
    audit_trail:             List[Dict[str, Any]]

    def check_and_update_state(
        self, at: Optional[datetime] = None
    ) -> "GovernanceProtocolRecord":
        """Evaluate current time and update lifecycle state. Returns self."""
        now = at or datetime.now(timezone.utc)

        if self.state in (
            ProtocolLifecycleState.PERMANENT,
            ProtocolLifecycleState.EXPIRED,
            ProtocolLifecycleState.RENEWED,
        ):
            return self

        if self.sunset_date is None:
            self._transition(
                ProtocolLifecycleState.PENDING_REVALIDATION, now,
                "no_sunset_date_not_permanent"
            )
            return self

        sunset = datetime.fromisoformat(self.sunset_date)

        if self.state == ProtocolLifecycleState.ACTIVE and now >= sunset:
            deadline = (now + timedelta(days=DEFAULT_REVALIDATION_DAYS)).isoformat()
            self.revalidation_deadline = deadline
            self._transition(
                ProtocolLifecycleState.PENDING_REVALIDATION, now,
                "sunset_date_reached"
            )
            logger.warning(
                f"Protocol [{self.item_id}] -> PENDING_REVALIDATION. "
                f"Deadline: {deadline[:10]}."
            )

        elif self.state == ProtocolLifecycleState.PENDING_REVALIDATION:
            if self.revalidation_deadline is None:
                self._transition(
                    ProtocolLifecycleState.EXPIRED, now, "missing_deadline"
                )
            elif now >= datetime.fromisoformat(self.revalidation_deadline):
                self._transition(
                    ProtocolLifecycleState.EXPIRED, now,
                    "revalidation_deadline_exceeded"
                )
                logger.error(
                    f"Protocol [{self.item_id}] EXPIRED. "
                    f"Hard Block permanent until resolution."
                )
        return self

    def renew(
        self,
        renewed_by:      str,
        new_sunset_date: str,
        at:              Optional[datetime] = None,
    ) -> "GovernanceProtocolRecord":
        """
        Complete revalidation. Transitions to RENEWED then ACTIVE.

        Raises ValueError if current state does not allow renewal.
        """
        if self.state not in (
            ProtocolLifecycleState.ACTIVE,
            ProtocolLifecycleState.PENDING_REVALIDATION,
        ):
            raise ValueError(
                f"Cannot renew protocol in state '{self.state.value}'."
            )
        now = at or datetime.now(timezone.utc)
        self.sunset_date           = new_sunset_date
        self.revalidation_deadline = None
        self.renewal_history.append({
            "renewed_at":      now.isoformat(),
            "renewed_by":      renewed_by,
            "new_sunset_date": new_sunset_date,
        })
        self._transition(ProtocolLifecycleState.RENEWED, now, "revalidation_completed")
        self.state = ProtocolLifecycleState.ACTIVE
        logger.info(
            f"Protocol [{self.item_id}] RENEWED by '{renewed_by}'. "
            f"New sunset: {new_sunset_date[:10]}."
        )
        return self

    def declare_permanent(
        self,
        signed_by:     str,
        justification: str,
        succession:    str,
        at:            Optional[datetime] = None,
    ) -> "GovernanceProtocolRecord":
        """
        Declare PERMANENT (no sunset).

        Requirements: community authority only (not external institution),
        non-empty justification, documented succession_authority.

        Raises ValueError if conditions not met.
        """
        if not justification.strip():
            raise ValueError("PERMANENT requires non-empty justification.")
        if not succession.strip():
            raise ValueError("PERMANENT requires documented succession_authority.")
        now = at or datetime.now(timezone.utc)
        self.sunset_date             = None
        self.revalidation_deadline   = None
        self.permanent_justification = justification
        self.succession_authority    = succession
        self._transition(
            ProtocolLifecycleState.PERMANENT, now,
            f"declared_permanent_by_{signed_by}"
        )
        logger.info(
            f"Protocol [{self.item_id}] PERMANENT by '{signed_by}'."
        )
        return self

    def _transition(
        self, new_state: ProtocolLifecycleState, at: datetime, reason: str
    ) -> None:
        entry = {
            "item_id":        self.item_id,
            "from_state":     self.state.value,
            "to_state":       new_state.value,
            "reason":         reason,
            "timestamp":      at.isoformat(),
            "eaifch_version": __version__,
        }
        log_hash = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()
        self.audit_trail.append({"hash": log_hash, "data": entry})
        self.state = new_state

    @property
    def is_hard_blocked(self) -> bool:
        return (
            self.state in (
                ProtocolLifecycleState.PENDING_REVALIDATION,
                ProtocolLifecycleState.EXPIRED,
                ProtocolLifecycleState.PERMANENT,
            )
            or not self.protocol.can_export
        )

    @property
    def summary(self) -> str:
        sunset_str = self.sunset_date[:10] if self.sunset_date else "PERMANENT"
        return (
            f"Protocol [{self.item_id}]: {self.state.value} | "
            f"Sunset: {sunset_str} | "
            f"HardBlock: {self.is_hard_blocked} | "
            f"Renewals: {len(self.renewal_history)}"
        )


def create_protocol_record(
    protocol:      GovernanceProtocol,
    item_id:       str,
    sunset_months: int  = DEFAULT_SUNSET_MONTHS,
    permanent:     bool = False,
    justification: str  = "",
    succession:    str  = "",
    at:            Optional[datetime] = None,
) -> GovernanceProtocolRecord:
    """
    Factory: wrap a GovernanceProtocol in a lifecycle record.

    Parameters
    ----------
    protocol      : SAVEC v3.1 GovernanceProtocol.
    item_id       : Heritage item identifier.
    sunset_months : Validity period in months (default 24).
    permanent     : If True, declare PERMANENT immediately.
    justification : Required when permanent=True.
    succession    : Required when permanent=True.
    at            : Creation timestamp (default: now UTC).
    """
    now = at or datetime.now(timezone.utc)

    if permanent:
        if not justification.strip():
            raise ValueError("PERMANENT record requires justification.")
        if not succession.strip():
            raise ValueError("PERMANENT record requires succession_authority.")
        record = GovernanceProtocolRecord(
            protocol=protocol, item_id=item_id,
            created_at=now.isoformat(), sunset_date=None,
            revalidation_deadline=None,
            state=ProtocolLifecycleState.ACTIVE,
            permanent_justification="", succession_authority="",
            renewal_history=[], audit_trail=[],
        )
        record.declare_permanent(
            signed_by=protocol.authority_id,
            justification=justification,
            succession=succession,
            at=now,
        )
    else:
        sunset_date = (now + timedelta(days=sunset_months * 30)).isoformat()
        record = GovernanceProtocolRecord(
            protocol=protocol, item_id=item_id,
            created_at=now.isoformat(), sunset_date=sunset_date,
            revalidation_deadline=None,
            state=ProtocolLifecycleState.ACTIVE,
            permanent_justification="", succession_authority="",
            renewal_history=[], audit_trail=[],
        )
        record._transition(ProtocolLifecycleState.ACTIVE, now, "created")

    return record


# =============================================================================
# MODULE 0 -- 0.5: ConflictResolver
# =============================================================================

class ConflictResolutionLevel(Enum):
    """
    Three-level cascade for inter-community disputes.

    AUTOMATIC  : AccessLevels agree -> pessimistic default applied.
    MEDIATION  : AccessLevels differ -> 30-day window, provisional block.
    ESCALATION : Mediation failed/void -> permanent Hard Block.
    """
    AUTOMATIC  = "AUTOMATIC"
    MEDIATION  = "MEDIATION"
    ESCALATION = "ESCALATION"


@dataclass(frozen=True)
class ConflictResolutionResult:
    """
    Output of ConflictResolver.resolve_conflict().

    Parameters
    ----------
    item_id                : Heritage item identifier.
    resolution_level       : ConflictResolutionLevel.
    resolved_protocol      : GovernanceProtocol if AUTOMATIC; None otherwise.
    mediation_deadline     : ISO 8601 UTC deadline (MEDIATION only).
    provisional_hard_block : True for MEDIATION and ESCALATION.
    conflict_description   : Human-readable description.
    audit_hash             : SHA-256 of the resolution record.
    resolved_at            : ISO 8601 UTC.
    """
    item_id:                str
    resolution_level:       ConflictResolutionLevel
    resolved_protocol:      Optional[GovernanceProtocol]
    mediation_deadline:     Optional[str]
    provisional_hard_block: bool
    conflict_description:   str
    audit_hash:             str
    resolved_at:            str

    @property
    def summary(self) -> str:
        if self.resolution_level == ConflictResolutionLevel.AUTOMATIC:
            lvl = (
                self.resolved_protocol.access_level.name
                if self.resolved_protocol else "N/A"
            )
            return (
                f"Conflict [{self.item_id}]: AUTOMATIC | Level={lvl} | "
                f"SHA-256: {self.audit_hash[:16]}..."
            )
        elif self.resolution_level == ConflictResolutionLevel.MEDIATION:
            dl = self.mediation_deadline[:10] if self.mediation_deadline else "N/A"
            return (
                f"Conflict [{self.item_id}]: MEDIATION | "
                f"Deadline: {dl} | HardBlock: True"
            )
        return (
            f"Conflict [{self.item_id}]: ESCALATION | "
            f"Permanent HardBlock | Funding advocacy triggered."
        )


class ConflictResolver:
    """
    Three-level cascade conflict resolution (EAIFCH 2.0 Spec § 2.4).

    Level 1 (AUTOMATIC) : AccessLevels agree -> max/all/any default.
    Level 2 (MEDIATION) : Levels differ -> 30-day window + block.
    Level 3 (ESCALATION): Void or failed mediation -> permanent block.

    Axiom: At every level, choose the most protective decision.

    Parameters
    ----------
    item_id        : Heritage item under dispute.
    mediation_days : Duration of mediation window (default 30).
    """

    def __init__(self, item_id: str, mediation_days: int = 30) -> None:
        self.item_id        = item_id
        self.mediation_days = mediation_days
        self.audit_trail:   List[Dict[str, Any]] = []

    def resolve_conflict(
        self,
        protocols: List[GovernanceProtocol],
        escalated: bool = False,
        at:        Optional[datetime] = None,
    ) -> ConflictResolutionResult:
        """
        Resolve conflict between community protocols.

        Parameters
        ----------
        protocols : Competing GovernanceProtocols.
        escalated : If True, skip to ESCALATION (mediation failed).
        at        : Timestamp (default: now UTC).

        Returns ConflictResolutionResult.
        """
        now         = at or datetime.now(timezone.utc)
        resolved_at = now.isoformat()

        if not protocols:
            return self._escalate("Governance void -- no protocols.", resolved_at)

        if escalated:
            return self._escalate("Mediation failed or deadline exceeded.", resolved_at)

        access_levels = {p.access_level for p in protocols}

        if len(access_levels) == 1:
            resolved = GovernanceProtocol(
                authority_id="EAIFCH_CONFLICT_RESOLVER",
                access_level=max(p.access_level for p in protocols),
                can_export=all(p.can_export for p in protocols),
                requires_manual_audit=any(p.requires_manual_audit for p in protocols),
                description=(
                    f"Automatic resolution from {len(protocols)} protocols. "
                    f"Level: {next(iter(access_levels)).name}."
                ),
                epistemic_basis=(
                    "statistical_layer1"
                    if all(p.epistemic_basis == "statistical_layer1" for p in protocols)
                    else "mixed_epistemic_basis"
                ),
            )
            result = ConflictResolutionResult(
                item_id=self.item_id,
                resolution_level=ConflictResolutionLevel.AUTOMATIC,
                resolved_protocol=resolved,
                mediation_deadline=None,
                provisional_hard_block=not resolved.can_export,
                conflict_description=(
                    f"AccessLevels agreed: {next(iter(access_levels)).name}. "
                    f"Pessimistic default applied."
                ),
                audit_hash=self._hash({
                    "item_id": self.item_id, "level": "AUTOMATIC",
                    "resolved_level": resolved.access_level.name,
                    "resolved_at": resolved_at,
                }),
                resolved_at=resolved_at,
            )
        else:
            names    = sorted([l.name for l in access_levels])
            deadline = (now + timedelta(days=self.mediation_days)).isoformat()
            result   = ConflictResolutionResult(
                item_id=self.item_id,
                resolution_level=ConflictResolutionLevel.MEDIATION,
                resolved_protocol=None,
                mediation_deadline=deadline,
                provisional_hard_block=True,
                conflict_description=(
                    f"AccessLevels disagree: {names}. "
                    f"Mediation required. Provisional HardBlock active."
                ),
                audit_hash=self._hash({
                    "item_id": self.item_id, "level": "MEDIATION",
                    "deadline": deadline, "resolved_at": resolved_at,
                }),
                resolved_at=resolved_at,
            )

        self.audit_trail.append({
            "level":       result.resolution_level.value,
            "resolved_at": result.resolved_at,
            "hash":        result.audit_hash,
        })
        return result

    def _escalate(self, reason: str, resolved_at: str) -> ConflictResolutionResult:
        result = ConflictResolutionResult(
            item_id=self.item_id,
            resolution_level=ConflictResolutionLevel.ESCALATION,
            resolved_protocol=None,
            mediation_deadline=None,
            provisional_hard_block=True,
            conflict_description=f"ESCALATION: {reason}",
            audit_hash=self._hash({
                "item_id": self.item_id, "level": "ESCALATION",
                "reason": reason, "resolved_at": resolved_at,
            }),
            resolved_at=resolved_at,
        )
        self.audit_trail.append({
            "level": "ESCALATION", "resolved_at": resolved_at,
            "hash": result.audit_hash,
        })
        logger.error(f"ConflictResolver [{self.item_id}]: ESCALATION. {reason}")
        return result

    def _hash(self, data: Dict[str, Any]) -> str:
        data["eaifch_version"] = __version__
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()


# =============================================================================
# MODULE 7 -- 7.1: ConstitutionalRules (CR-1 to CR-5)
# =============================================================================

@dataclass(frozen=True)
class ConstitutionalRule:
    """
    Inviolable LLM constraint derived from CARE Principles.

    Cannot be overridden by user instructions.
    blocks_on_violation=True  -> violation halts task + AIRefusalRecord.
    blocks_on_violation=False -> structural enforcement (output stage).

    check(context) -> (passes: bool, violation_message: str)
    """
    rule_id:             str
    name:                str
    description:         str
    blocks_on_violation: bool = True

    def check(self, context: Dict[str, Any]) -> Tuple[bool, str]:
        task      = context.get("task_type", "")
        level_val = context.get("item_sensitivity", 0)

        if self.rule_id == "CR-1":
            if task in ("generate_ip_claim", "claim_ownership", "publish_without_attribution"):
                return False, (
                    "CR-1: LLM cannot claim ownership of community-governed materials."
                )
            return True, ""

        if self.rule_id == "CR-2":
            if (level_val >= AccessLevel.SACRED_SECRET.value
                    and task in ("interpret", "paraphrase", "summarise_content",
                                 "translate_sacred")):
                return False, (
                    "CR-2: LLM cannot interpret/paraphrase SACRED_SECRET materials."
                )
            return True, ""

        # CR-3, CR-4, CR-5: enforced structurally at output stage
        return True, ""


CONSTITUTIONAL_RULES: List[ConstitutionalRule] = [
    ConstitutionalRule(
        rule_id="CR-1", name="Non-appropriation", blocks_on_violation=True,
        description=(
            "LLM cannot produce content presenting community-governed "
            "materials as intellectual property of the operator."
        ),
    ),
    ConstitutionalRule(
        rule_id="CR-2", name="Non-sacred-interpretation", blocks_on_violation=True,
        description=(
            "LLM cannot interpret, paraphrase, or summarise SACRED_SECRET "
            "materials regardless of request formulation."
        ),
    ),
    ConstitutionalRule(
        rule_id="CR-3", name="Explicit uncertainty", blocks_on_violation=False,
        description=(
            "Every output must include an uncertainty_statement documenting "
            "analysis limits and where community expertise is required."
        ),
    ),
    ConstitutionalRule(
        rule_id="CR-4", name="Complete traceability", blocks_on_violation=False,
        description=(
            "Every interaction logged: prompt SHA-256, model version, UTC "
            "timestamp, assigned reviewer, validation status. Confidential "
            "sparring: content restricted, hash preserved."
        ),
    ),
    ConstitutionalRule(
        rule_id="CR-5", name="Documented automatic refusal", blocks_on_violation=False,
        description=(
            "Every refusal generates an AIRefusalRecord: governance data "
            "documenting that a high-risk task was attempted and blocked."
        ),
    ),
]


# =============================================================================
# MODULE 7 -- 7.2: Data structures
# =============================================================================

@dataclass(frozen=True)
class AIRefusalRecord:
    """
    Immutable record of an AIBsandbox automatic refusal (CR-5).

    Every refusal is governance data: it documents that a high-risk
    task was attempted and blocked by the constitutional architecture.
    """
    refusal_id:     str
    item_id:        str
    task_type:      str
    refusal_reason: str
    violated_rules: List[str]
    requester_id:   str
    refused_at:     str
    audit_hash:     str

    @property
    def summary(self) -> str:
        return (
            f"AIRefusalRecord [{self.refusal_id}] | "
            f"Item: {self.item_id} | Task: {self.task_type} | "
            f"Rules: {self.violated_rules} | "
            f"SHA-256: {self.audit_hash[:16]}..."
        )


@dataclass
class LLMOutputRecord:
    """
    Mutable record of an LLM output through the validation lifecycle.

    epistemic_basis starts as "ai_generated_unvalidated".
    After confirm(): "ai_assisted_human_validated".
    can_feed_layer2 is True only after human confirmation.

    Parameters
    ----------
    output_id             : SHA-256 prefix of item+task+timestamp.
    item_id               : Heritage item identifier.
    task_type             : Task executed within the sandbox.
    prompt_hash           : SHA-256 of the prompt (content not stored).
    raw_output            : LLM-produced text.
    uncertainty_statement : CR-3 compliance statement.
    model_id              : LLM model identifier and version.
    produced_at           : ISO 8601 UTC.
    validation_status     : "pending" | "human_confirmed" | "human_rejected".
    validated_by          : Human reviewer identifier (set on confirm/reject).
    validated_at          : ISO 8601 UTC (set on confirm/reject).
    confidence_discount   : Applied when computing combined_confidence.
    epistemic_basis       : Set to "ai_assisted_human_validated" on confirm.
    audit_hash            : SHA-256 of the record state.
    """
    output_id:             str
    item_id:               str
    task_type:             str
    prompt_hash:           str
    raw_output:            str
    uncertainty_statement: str
    model_id:              str
    produced_at:           str
    validation_status:     str            = "pending"
    validated_by:          Optional[str]  = None
    validated_at:          Optional[str]  = None
    confidence_discount:   float          = DEFAULT_CONFIDENCE_DISCOUNT_AI
    epistemic_basis:       str            = "ai_generated_unvalidated"
    audit_hash:            str            = ""

    def confirm(
        self,
        reviewer_id:           str,
        uncertainty_statement: Optional[str] = None,
        at:                    Optional[datetime] = None,
    ) -> "LLMOutputRecord":
        """
        Human confirmation. Transitions to ai_assisted_human_validated.

        Parameters
        ----------
        reviewer_id           : Human reviewer identifier.
        uncertainty_statement : Optional override of CR-3 statement.
        at                    : Timestamp (default: now UTC).
        """
        now = at or datetime.now(timezone.utc)
        self.validation_status = "human_confirmed"
        self.validated_by      = reviewer_id
        self.validated_at      = now.isoformat()
        self.epistemic_basis   = "ai_assisted_human_validated"
        self.confidence_discount = DEFAULT_CONFIDENCE_DISCOUNT_AI
        if uncertainty_statement:
            self.uncertainty_statement = uncertainty_statement
        self._sign()
        logger.info(
            f"LLMOutputRecord [{self.output_id}] confirmed by '{reviewer_id}'."
        )
        return self

    def reject(
        self,
        reviewer_id: str,
        reason:      str,
        at:          Optional[datetime] = None,
    ) -> "LLMOutputRecord":
        """
        Human rejection. epistemic_basis remains ai_generated_unvalidated.

        Parameters
        ----------
        reviewer_id : Human reviewer identifier.
        reason      : Rejection rationale (archived in raw_output).
        at          : Timestamp (default: now UTC).
        """
        now = at or datetime.now(timezone.utc)
        self.validation_status = "human_rejected"
        self.validated_by      = reviewer_id
        self.validated_at      = now.isoformat()
        self.raw_output        = f"[REJECTED by {reviewer_id}: {reason}]"
        self._sign()
        logger.info(
            f"LLMOutputRecord [{self.output_id}] rejected by '{reviewer_id}'."
        )
        return self

    def _sign(self) -> None:
        d = {
            "output_id":         self.output_id,
            "item_id":           self.item_id,
            "task_type":         self.task_type,
            "prompt_hash":       self.prompt_hash,
            "validation_status": self.validation_status,
            "validated_by":      self.validated_by,
            "validated_at":      self.validated_at,
            "epistemic_basis":   self.epistemic_basis,
            "eaifch_version":    __version__,
        }
        self.audit_hash = hashlib.sha256(
            json.dumps(d, sort_keys=True).encode()
        ).hexdigest()

    @property
    def can_feed_layer2(self) -> bool:
        """True only if human_confirmed."""
        return self.validation_status == "human_confirmed"

    @property
    def summary(self) -> str:
        return (
            f"LLMOutputRecord [{self.output_id}] | "
            f"Status: {self.validation_status} | "
            f"Basis: {self.epistemic_basis} | "
            f"Discount: {self.confidence_discount:.2f} | "
            f"Reviewer: {self.validated_by or 'pending'}"
        )


@dataclass(frozen=True)
class SparkingSessionRecord:
    """
    Immutable record of a traced AI Sparring Partner session.

    Sparring outputs do NOT feed Module 1 / Layer 2 directly.
    Confidential sessions: prompt content restricted to community;
    session_hash preserved for audit integrity.
    """
    session_id:     str
    session_type:   str
    item_ids:       Tuple[str, ...]
    n_turns:        int
    model_id:       str
    human_reviewer: str
    community_id:   Optional[str]
    confidential:   bool
    started_at:     str
    ended_at:       str
    session_hash:   str

    @property
    def summary(self) -> str:
        tag = " [CONFIDENTIAL]" if self.confidential else ""
        return (
            f"SparkingSession [{self.session_id}]{tag} | "
            f"Type: {self.session_type} | Turns: {self.n_turns} | "
            f"Items: {len(self.item_ids)} | "
            f"Reviewer: {self.human_reviewer} | "
            f"SHA-256: {self.session_hash[:16]}..."
        )


# =============================================================================
# MODULE 7 -- 7.3: LLMAdapter (abstract interface)
# =============================================================================

class LLMAdapter(abc.ABC):
    """
    Abstract interface for any LLM entering the AIBsandbox.

    Any LLM (API-based or local) must implement this interface.
    The sandbox enforces ConstitutionalRules regardless of which
    LLM is plugged in.

    The prototype does NOT call any real LLM API. It defines the
    contract that any LLM must satisfy.
    """

    @property
    @abc.abstractmethod
    def model_id(self) -> str:
        """Return model identifier string."""

    @abc.abstractmethod
    def generate(
        self,
        prompt:     str,
        max_tokens: int = 1000,
        system:     str = "",
    ) -> Tuple[str, str]:
        """
        Generate (output_text, uncertainty_statement).

        The uncertainty_statement is required by CR-3.
        If the LLM cannot produce one, the sandbox injects a default.
        """

    def estimated_energy_wh(self, n_tokens: int) -> float:
        """
        Estimate energy cost in Wh (feeds Module 6 cost preview).
        Override for known models. Default: 0.0 (unknown).
        """
        return 0.0


class MockLLMAdapter(LLMAdapter):
    """Mock LLM for testing and demonstration. No external API calls."""

    @property
    def model_id(self) -> str:
        return "mock-llm-v1.0-eaifch-demo"

    def generate(
        self,
        prompt:     str,
        max_tokens: int = 1000,
        system:     str = "",
    ) -> Tuple[str, str]:
        output = (
            f"[Mock output for {len(prompt)}-char prompt] "
            f"Metadata analysis suggests ceremonial object characteristics. "
            f"Further community consultation recommended."
        )
        uncertainty = (
            "Analysis based on metadata only. No direct object examination. "
            "Community expertise required to validate cultural significance."
        )
        return output, uncertainty


# =============================================================================
# MODULE 7 -- 7.4: AIBsandbox
# =============================================================================

class AIBsandbox:
    """
    Ethical bounding system for LLM use in EAIFCH 2.0 (Module 7).

    Enforces:
    - Task whitelist / blacklist.
    - ConstitutionalRules CR-1 to CR-5 (pre-execution).
    - CR-3 (uncertainty_statement) at output stage.
    - Full prompt hashing + audit trail (CR-4).
    - AIRefusalRecord for every blocked task (CR-5).

    Non-delegation axiom (SPEC-D4, inviolable):
    No AIBsandbox output constitutes a final governance decision.
    LLMOutputRecord objects require human confirmation before
    feeding Module 1 or Layer 2.

    Parameters
    ----------
    llm                  : LLMAdapter implementation.
    constitutional_rules : Override CONSTITUTIONAL_RULES if needed.
    """

    def __init__(
        self,
        llm:                  LLMAdapter,
        constitutional_rules: Optional[List[ConstitutionalRule]] = None,
    ) -> None:
        self.llm          = llm
        self.rules        = constitutional_rules or CONSTITUTIONAL_RULES
        self.output_log:  List[LLMOutputRecord]       = []
        self.refusal_log: List[AIRefusalRecord]        = []
        self.session_log: List[SparkingSessionRecord]  = []

    def execute_task(
        self,
        item_id:      str,
        task_type:    str,
        prompt:       str,
        context:      Dict[str, Any],
        requester_id: str,
    ) -> "LLMOutputRecord | AIRefusalRecord":
        """
        Execute a bounded task within the sandbox.

        Parameters
        ----------
        item_id      : Heritage item identifier.
        task_type    : Task type (checked against PERMITTED/REFUSED_TASKS).
        prompt       : User prompt (SHA-256 hashed, not stored raw).
        context      : Task context for ConstitutionalRule evaluation.
                       Keys: task_type, access_level, item_sensitivity,
                       has_community_authority, requester_is_community_member.
        requester_id : Human requester identifier.

        Returns
        -------
        LLMOutputRecord   : Task permitted and rules passed.
        AIRefusalRecord   : Task refused or rules violated.
        """
        now         = datetime.now(timezone.utc)
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()

        # Step 1: Task blacklist check
        if task_type in REFUSED_TASKS:
            return self._refuse(
                item_id=item_id, task_type=task_type,
                reason=f"Task '{task_type}' is on the refused task list.",
                violated_rules=["TASK_BLACKLIST"],
                requester_id=requester_id, at=now,
            )

        # Step 2: Task whitelist check
        if task_type not in PERMITTED_TASKS:
            return self._refuse(
                item_id=item_id, task_type=task_type,
                reason=f"Task '{task_type}' is not in the permitted task list.",
                violated_rules=["TASK_NOT_PERMITTED"],
                requester_id=requester_id, at=now,
            )

        # Step 3: ConstitutionalRule pre-execution checks
        ctx      = {**context, "task_type": task_type}
        violated = [
            rule.rule_id
            for rule in self.rules
            if rule.blocks_on_violation and not rule.check(ctx)[0]
        ]
        if violated:
            msgs = "; ".join(
                rule.check(ctx)[1]
                for rule in self.rules
                if rule.rule_id in violated
            )
            return self._refuse(
                item_id=item_id, task_type=task_type,
                reason=f"ConstitutionalRule(s) violated: {msgs}",
                violated_rules=violated,
                requester_id=requester_id, at=now,
            )

        # Step 4: Generate output
        system_prompt = self._system_prompt()
        try:
            raw_output, uncertainty = self.llm.generate(
                prompt=prompt, system=system_prompt
            )
        except Exception as exc:
            return self._refuse(
                item_id=item_id, task_type=task_type,
                reason=f"LLM generation failed: {exc}",
                violated_rules=["LLM_ERROR"],
                requester_id=requester_id, at=now,
            )

        # Step 5: CR-3 enforcement
        if not uncertainty or not uncertainty.strip():
            uncertainty = (
                "No uncertainty statement provided by the model. "
                "Community expertise required to validate this output."
            )

        # Step 6: Build output record
        output_id = hashlib.sha256(
            f"{item_id}{task_type}{now.isoformat()}".encode()
        ).hexdigest()[:16]

        record = LLMOutputRecord(
            output_id=output_id, item_id=item_id, task_type=task_type,
            prompt_hash=prompt_hash, raw_output=raw_output,
            uncertainty_statement=uncertainty, model_id=self.llm.model_id,
            produced_at=now.isoformat(),
        )
        record._sign()
        self.output_log.append(record)
        logger.info(
            f"AIBsandbox: '{task_type}' for '{item_id}' -> "
            f"output [{record.output_id}]. Awaiting human validation."
        )
        return record

    def start_sparring_session(
        self,
        session_type:   str,
        item_ids:       List[str],
        human_reviewer: str,
        community_id:   Optional[str] = None,
        confidential:   bool          = False,
    ) -> SparkingSessionRecord:
        """
        Create a traced AI Sparring Partner session record.

        Outputs do not feed Module 1 / Layer 2 directly.
        Confidential sessions restrict prompt content to the community.

        Parameters
        ----------
        session_type   : "research_exploration" | "governance_deliberation"
                         | "confidential_sparring".
        item_ids       : Items discussed.
        human_reviewer : Session facilitator.
        community_id   : Community whose materials are discussed.
        confidential   : If True, prompt content restricted.
        """
        valid_types = {
            "research_exploration", "governance_deliberation", "confidential_sparring"
        }
        if session_type not in valid_types:
            raise ValueError(
                f"Invalid session_type '{session_type}'. "
                f"Must be one of: {sorted(valid_types)}."
            )

        now        = datetime.now(timezone.utc)
        session_id = hashlib.sha256(
            f"{session_type}{human_reviewer}{now.isoformat()}".encode()
        ).hexdigest()[:16]

        meta = {
            "session_id":    session_id, "session_type": session_type,
            "item_ids":      sorted(item_ids), "human_reviewer": human_reviewer,
            "community_id":  community_id, "confidential": confidential,
            "started_at":    now.isoformat(), "eaifch_version": __version__,
        }
        session_hash = hashlib.sha256(
            json.dumps(meta, sort_keys=True).encode()
        ).hexdigest()

        record = SparkingSessionRecord(
            session_id=session_id, session_type=session_type,
            item_ids=tuple(item_ids), n_turns=0,
            model_id=self.llm.model_id, human_reviewer=human_reviewer,
            community_id=community_id, confidential=confidential,
            started_at=now.isoformat(), ended_at=now.isoformat(),
            session_hash=session_hash,
        )
        self.session_log.append(record)
        logger.info(
            f"AIBsandbox: sparring session [{session_id}] started | "
            f"type={session_type} | confidential={confidential}"
        )
        return record

    def _refuse(
        self,
        item_id:       str,
        task_type:     str,
        reason:        str,
        violated_rules:List[str],
        requester_id:  str,
        at:            datetime,
    ) -> AIRefusalRecord:
        refusal_id = hashlib.sha256(
            f"{item_id}{task_type}{at.isoformat()}".encode()
        ).hexdigest()[:16]
        entry = {
            "refusal_id": refusal_id, "item_id": item_id,
            "task_type": task_type, "reason": reason,
            "violated_rules": violated_rules, "requester_id": requester_id,
            "refused_at": at.isoformat(), "eaifch_version": __version__,
        }
        audit_hash = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()
        record = AIRefusalRecord(
            refusal_id=refusal_id, item_id=item_id, task_type=task_type,
            refusal_reason=reason, violated_rules=violated_rules,
            requester_id=requester_id, refused_at=at.isoformat(),
            audit_hash=audit_hash,
        )
        self.refusal_log.append(record)
        logger.warning(f"AIBsandbox REFUSAL [{refusal_id}]: {task_type} | {reason}")
        return record

    def _system_prompt(self) -> str:
        rules_text = "\n".join(f"  {r.rule_id}: {r.description}" for r in self.rules)
        return (
            f"You are operating within the EAIFCH 2.0 ethical sandbox "
            f"(v{__version__}). The following constitutional rules are "
            f"inviolable:\n{rules_text}\n\n"
            f"Always include a clear uncertainty_statement in your output."
        )

    @property
    def stats(self) -> Dict[str, Any]:
        confirmed = sum(1 for r in self.output_log if r.validation_status == "human_confirmed")
        rejected  = sum(1 for r in self.output_log if r.validation_status == "human_rejected")
        pending   = sum(1 for r in self.output_log if r.validation_status == "pending")
        return {
            "outputs_produced":  len(self.output_log),
            "outputs_confirmed": confirmed,
            "outputs_rejected":  rejected,
            "outputs_pending":   pending,
            "refusals":          len(self.refusal_log),
            "sparring_sessions": len(self.session_log),
            "model_id":          self.llm.model_id,
            "eaifch_version":    __version__,
            "savec_version":     SAVEC_VERSION,
        }


# =============================================================================
# Demonstration
# =============================================================================

def main() -> int:
    """
    Demonstrate Module 0 and Module 7 components.
    Returns 0 on success.
    """
    w = 70
    print("=" * w)
    print(f"EAIFCH 2.0  --  Module 0 + Module 7  --  v{__version__}")
    print(f"Author:      {__author__}")
    print(f"ORCID:       {__orcid__}")
    print(f"DOI:         {__doi__}")
    print(f"SAVEC:       v{SAVEC_VERSION} ({'linked' if SAVEC_AVAILABLE else 'stub mode'})")
    print(f"Principle:   {MODULE_METADATA['design_principle']}")
    print("=" * w)

    now = datetime.now(timezone.utc)

    # ---- MODULE 0 | Demo 1: TaxonomyRegistry --------------------------------
    print(f"\n{'─' * 50}")
    print("MODULE 0 | Demo 1: TaxonomyVersion + Registry")
    print(f"{'─' * 50}")

    indicators = {
        "object_ceremonial_use":   {"weight": 20, "description": "Ceremonial use"},
        "access_restricted_oral":  {"weight": 15, "description": "Oral restriction"},
        "non_member_requester":    {"weight": 10, "description": "Non-member requester"},
        "sacred_site_association": {"weight": 25, "description": "Sacred site link"},
        "repatriation_claim":      {"weight": 15, "description": "Repatriation claim"},
    }

    v100 = TaxonomyVersion(
        major=1, minor=0, patch=0,
        published_at=now.isoformat(),
        published_by="EAIFCH_Governance_Council",
        description="Initial central taxonomy.",
        indicators=indicators,
        access_levels=tuple(l.name for l in AccessLevel),
        change_type="MAJOR", parent_version=None, audit_hash="",
    )
    registry = TaxonomyRegistry(initial_version=v100)
    print(f"  Root:       {registry.current.summary}")

    v101 = TaxonomyVersion(
        major=1, minor=0, patch=1,
        published_at=now.isoformat(),
        published_by="EAIFCH_Governance_Council",
        description="Added Warlpiri labels.",
        indicators=indicators,
        access_levels=tuple(l.name for l in AccessLevel),
        change_type="PATCH", parent_version="1.0.0", audit_hash="",
    )
    registry.register(v101)
    print(f"  Patch:      {registry.current.summary}")

    report = registry.migration_report("1.0.0", "1.0.1")
    print(f"  Migration:  compatible={report['is_compatible']}, "
          f"added={report['indicators_added']}, "
          f"removed={report['indicators_removed']}")

    # ---- MODULE 0 | Demo 2: CommunityFork + BooleanOverrideRule -------------
    print(f"\n{'─' * 50}")
    print("MODULE 0 | Demo 2: CommunityFork + BooleanOverrideRule")
    print(f"{'─' * 50}")

    override = BooleanOverrideRule(
        rule_id="InitiationProtocol_Override",
        description=(
            "Ceremonial use + non-member requester -> SACRED_SECRET."
        ),
        trigger_indicators=("object_ceremonial_use", "non_member_requester"),
        override_access_level=AccessLevel.SACRED_SECRET,
        signed_by="Wiradjuri_Council_Elder",
        created_at=now.isoformat(),
        languages={"en": "Initiation override", "wrl": "Yalumba ngurra-ku"},
    )

    fork = CommunityFork(
        fork_id="wiradjuri_fork_2026_05",
        community_id="Wiradjuri_Nation",
        base_version="1.0.1",
        signed_by="Wiradjuri_Council_Elder",
        valid_from=now.isoformat(),
        valid_until=(now + timedelta(days=24 * 30)).isoformat(),
        overrides=[override],
        weight_adjustments={"sacred_site_association": 35.0},
        language_additions={
            "object_ceremonial_use":   {"wrl": "Yalumba marliya-ku"},
            "sacred_site_association": {"wrl": "Ngurra yalumba-ku"},
        },
        description="Wiradjuri fork: elevated sacred site weight + initiation rule.",
    )
    errors = fork.validate(registry)
    if errors:
        print(f"  Errors: {errors}")
    else:
        fork.sign()
        print(f"  Signed:  {fork.fork_id} | SHA-256: {fork.audit_hash[:32]}...")
        print(f"  Active:  {fork.is_active()}")

    # Apply overrides -- upward elevation
    level_a, triggered_a = fork.apply_overrides(
        AccessLevel.RESTRICTED,
        ["object_ceremonial_use", "non_member_requester", "repatriation_claim"],
    )
    print(f"\n  Case A (triggers rule):")
    print(f"    RESTRICTED -> {level_a.name} | Rules: {triggered_a}")

    # Asymmetry constraint -- downward rule silently ignored
    bad_rule = BooleanOverrideRule(
        rule_id="Bad_Downward_Rule",
        description="Attempts to lower sensitivity (demo only).",
        trigger_indicators=("repatriation_claim",),
        override_access_level=AccessLevel.PUBLIC,
        signed_by="Demo", created_at=now.isoformat(),
    )
    bad_fork = CommunityFork(
        fork_id="bad_demo", community_id="Demo",
        base_version="1.0.1", signed_by="Demo",
        valid_from=now.isoformat(), valid_until=None,
        overrides=[bad_rule], weight_adjustments={},
        language_additions={}, description="Asymmetry demo.",
    )
    bad_fork.sign()
    level_b, triggered_b = bad_fork.apply_overrides(
        AccessLevel.SACRED_SECRET, ["repatriation_claim"]
    )
    print(f"  Case B (downward rule -- asymmetry constraint):")
    print(f"    SACRED_SECRET -> {level_b.name} | Rules: {triggered_b} (empty = blocked)")

    # ---- MODULE 0 | Demo 3: Sunset lifecycle --------------------------------
    print(f"\n{'─' * 50}")
    print("MODULE 0 | Demo 3: GovernanceProtocol Lifecycle")
    print(f"{'─' * 50}")

    if SAVEC_AVAILABLE:
        proto = GovernanceProtocol(
            authority_id="Wiradjuri_Council",
            access_level=AccessLevel.COMMUNITY,
            can_export=False, requires_manual_audit=True,
            description="Ceremonial site.", epistemic_basis="community_authority",
        )

        rec_active = create_protocol_record(proto, "item_active_001", sunset_months=24)
        print(f"  ACTIVE:    {rec_active.summary}")

        rec_expired = create_protocol_record(
            proto, "item_expired_001", sunset_months=1,
            at=now - timedelta(days=100),
        )
        rec_expired.check_and_update_state(at=now)
        print(f"  EXPIRED:   {rec_expired.summary}")

        rec_pending = create_protocol_record(
            proto, "item_pending_001", sunset_months=1,
            at=now - timedelta(days=32),
        )
        rec_pending.check_and_update_state(at=now)
        print(f"  PENDING:   {rec_pending.summary}")
        rec_pending.renew(
            renewed_by="Wiradjuri_Council_2026",
            new_sunset_date=(now + timedelta(days=730)).isoformat(),
        )
        print(f"  RENEWED:   {rec_pending.summary}")

        rec_perm = create_protocol_record(
            GovernanceProtocol(
                authority_id="Wiradjuri_Council",
                access_level=AccessLevel.SACRED_SECRET,
                can_export=False, requires_manual_audit=True,
                description="Sacred knowledge.", epistemic_basis="community_authority",
            ),
            item_id="item_sacred_001",
            permanent=True,
            justification="Sacred knowledge -- no digitisation pathway in community law.",
            succession="Wiradjuri_Law_Custodians_Assembly",
        )
        print(f"  PERMANENT: {rec_perm.summary}")
    else:
        print("  (SAVEC not linked -- lifecycle demo in stub mode)")
        proto_stub = GovernanceProtocol(
            authority_id="Wiradjuri_Council",
            access_level=AccessLevel.COMMUNITY,
            can_export=False, requires_manual_audit=True,
            description="Stub.", epistemic_basis="community_authority",
        )
        rec = create_protocol_record(proto_stub, "stub_001", sunset_months=24)
        print(f"  ACTIVE (stub): {rec.summary}")

    # ---- MODULE 0 | Demo 4: ConflictResolver --------------------------------
    print(f"\n{'─' * 50}")
    print("MODULE 0 | Demo 4: ConflictResolver")
    print(f"{'─' * 50}")

    make_proto = lambda aid, lvl, exp, audit, basis: GovernanceProtocol(
        authority_id=aid, access_level=lvl, can_export=exp,
        requires_manual_audit=audit,
        description=f"{aid} protocol.", epistemic_basis=basis,
    )

    # Case A: agree -> AUTOMATIC
    r_a = ConflictResolver("shared_001").resolve_conflict([
        make_proto("Community_A", AccessLevel.COMMUNITY, False, True,  "community_authority"),
        make_proto("Community_B", AccessLevel.COMMUNITY, False, False, "expert_human"),
    ])
    print(f"  Case A (agree):    {r_a.summary}")

    # Case B: differ -> MEDIATION
    r_b = ConflictResolver("shared_002").resolve_conflict([
        make_proto("Community_C", AccessLevel.PUBLIC,        True,  False, "expert_human"),
        make_proto("Community_D", AccessLevel.SACRED_SECRET, False, True,  "community_authority"),
    ])
    print(f"  Case B (differ):   {r_b.summary}")

    # Case C: void -> ESCALATION
    r_c = ConflictResolver("shared_003").resolve_conflict([], escalated=True)
    print(f"  Case C (escalate): {r_c.summary}")

    # ---- MODULE 7 | Demo 5: AIBsandbox + ConstitutionalRules ----------------
    print(f"\n{'─' * 50}")
    print("MODULE 7 | Demo 5: AIBsandbox + ConstitutionalRules")
    print(f"{'─' * 50}")

    sandbox = AIBsandbox(MockLLMAdapter())
    ctx = {
        "access_level": AccessLevel.COMMUNITY.name,
        "item_sensitivity": AccessLevel.COMMUNITY.value,
        "has_community_authority": True,
        "requester_is_community_member": False,
    }

    out_a = sandbox.execute_task(
        "item_001", "preliminary_sensitivity_classification",
        "Classify sensitivity of this metadata...", ctx, "researcher_benseddik",
    )
    print(f"\n  Permitted task: {out_a.summary}")

    out_b = sandbox.execute_task(
        "item_002", "theological_interpretation",
        "Interpret the theology of this object...",
        {**ctx, "item_sensitivity": AccessLevel.SACRED_SECRET.value},
        "researcher_external",
    )
    print(f"  Refused (blacklist):  {out_b.summary}")

    out_c = sandbox.execute_task(
        "item_003", "interpret",
        "Paraphrase this sacred ceremony...",
        {**ctx, "item_sensitivity": AccessLevel.SACRED_SECRET.value},
        "researcher_external",
    )
    print(f"  Refused (CR-2):       {out_c.summary}")

    out_d = sandbox.execute_task(
        "item_004", "unknown_task",
        "Do something unspecified...", ctx, "researcher_benseddik",
    )
    print(f"  Refused (not listed): {out_d.summary}")

    # ---- MODULE 7 | Demo 6: LLMOutputValidator workflow --------------------
    print(f"\n{'─' * 50}")
    print("MODULE 7 | Demo 6: LLMOutputValidator Workflow")
    print(f"{'─' * 50}")

    if isinstance(out_a, LLMOutputRecord):
        print(f"\n  Before: basis={out_a.epistemic_basis} | "
              f"can_feed_layer2={out_a.can_feed_layer2}")
        out_a.confirm(reviewer_id="community_elder_wiradjuri")
        print(f"  After:  basis={out_a.epistemic_basis} | "
              f"can_feed_layer2={out_a.can_feed_layer2} | "
              f"discount={out_a.confidence_discount:.2f}")

    print(f"\n  Epistemic basis table:")
    for basis in EPISTEMIC_BASIS_VALUES:
        disc    = get_confidence_discount(basis)
        blocked = not can_feed_layer2(basis)
        disc_str = "BLOCKED" if disc == float("inf") else f"{disc:.2f}"
        print(f"    {basis:<40} discount={disc_str:<8} blocked={blocked}")

    # ---- MODULE 7 | Demo 7: Sparring sessions -------------------------------
    print(f"\n{'─' * 50}")
    print("MODULE 7 | Demo 7: AI Sparring Partner Sessions")
    print(f"{'─' * 50}")

    sess_a = sandbox.start_sparring_session(
        "research_exploration", ["item_001", "item_002"],
        "researcher_benseddik", community_id="Wiradjuri_Nation",
    )
    print(f"\n  Public session:       {sess_a.summary}")

    sess_b = sandbox.start_sparring_session(
        "confidential_sparring", ["item_sacred_001"],
        "community_elder_wiradjuri", community_id="Wiradjuri_Nation",
        confidential=True,
    )
    print(f"  Confidential session: {sess_b.summary}")

    # ---- Summary stats ------------------------------------------------------
    print(f"\n{'─' * 50}")
    print("MODULE 7 | Sandbox Statistics")
    print(f"{'─' * 50}")
    for k, v in sandbox.stats.items():
        print(f"  {k:<32}: {v}")

    print(f"\n{'=' * w}")
    print("All demos completed successfully.")
    print(f"EAIFCH 2.0 v{__version__}  |  SAVEC v{SAVEC_VERSION}")
    print(f"{'=' * w}")
    return 0


if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s | %(name)s | %(message)s",
    )
    sys.exit(main())
