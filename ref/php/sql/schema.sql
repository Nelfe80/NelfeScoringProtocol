-- Schéma des tables scoring (référence). SQLite pour les tests ; adaptable MariaDB
-- (TEXT→VARCHAR, INTEGER PRIMARY KEY AUTOINCREMENT→BIGINT AUTO_INCREMENT, index idem).
-- En prod NelfePlay, les clés device vivent plutôt sur account_devices (colonnes
-- ajoutées) ; ici on isole pour la démonstration.

CREATE TABLE scoring_devices (
  device_id       TEXT PRIMARY KEY,
  key_id          TEXT NOT NULL,
  public_key_pem  TEXT NOT NULL,
  trust_level     TEXT NOT NULL DEFAULT 'cng_software',   -- tpm | cng_software | unknown
  risk_score      INTEGER NOT NULL DEFAULT 0,
  revoked_at      TEXT
);

CREATE TABLE scoring_issuers (
  key_id          TEXT PRIMARY KEY,
  public_key_pem  TEXT NOT NULL,
  revoked_at      TEXT
);

-- Consommation : idempotence (session) + usage unique (ticket) en une table.
CREATE TABLE scoring_consumed (
  session_id  TEXT PRIMARY KEY,
  ticket_id   TEXT NOT NULL UNIQUE,
  consumed_at TEXT NOT NULL
);

CREATE TABLE scoring_revoked_listeners ( sha256 TEXT PRIMARY KEY );
CREATE TABLE scoring_suspended ( rom_group TEXT NOT NULL, ruleset TEXT NOT NULL, PRIMARY KEY (rom_group, ruleset) );
-- Sessions marquées « anomalie statistique » (en prod : moteur de risque) → held.
CREATE TABLE scoring_stat_anomaly ( session_id TEXT PRIMARY KEY );

-- Audit de toutes les soumissions traitées (session_id UNIQUE = idempotence dure).
CREATE TABLE score_submissions (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT NOT NULL UNIQUE,
  device_id    TEXT NOT NULL,
  rom_group    TEXT NOT NULL,
  ruleset      TEXT NOT NULL,
  metric_value TEXT NOT NULL,
  verdict      TEXT NOT NULL,          -- published | held | refused
  reason_code  TEXT NOT NULL DEFAULT '',
  received_at  TEXT NOT NULL
);

-- Scores PUBLIÉS uniquement (ce qui classe).
CREATE TABLE scores (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  submission_id INTEGER NOT NULL,
  rom_group     TEXT NOT NULL,
  ruleset       TEXT NOT NULL,
  player_ref    TEXT,
  metric_value  INTEGER NOT NULL,
  accepted_at   TEXT NOT NULL
);
CREATE INDEX idx_scores_board ON scores (rom_group, ruleset, metric_value);
