"""Google Analytics consent banner companion for PyData Sphinx Theme."""

from __future__ import annotations

import json
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset


STATIC_DIR = Path(__file__).parent / "static"


def _config(app: Sphinx) -> dict[str, str]:
    return {
        "storageKey": app.config.ga_consent_storage_key,
        "bannerText": app.config.ga_consent_banner_text,
        "acceptText": app.config.ga_consent_accept_text,
        "declineText": app.config.ga_consent_decline_text,
        "privacyUrl": app.config.ga_consent_privacy_url,
        "privacyText": app.config.ga_consent_privacy_text,
    }


def _early_consent_script(app: Sphinx) -> str:
    config_json = json.dumps(_config(app), sort_keys=True)
    script = """
window.PYDATA_GA_CONSENT = __CONFIG_JSON__;
(function () {
  var config = window.PYDATA_GA_CONSENT || {};
  var key = config.storageKey || "pydata_ga_consent";
  var stored = null;

  try {
    stored = window.localStorage.getItem(key);
  } catch (error) {
    stored = null;
  }

  window.dataLayer = window.dataLayer || [];

  if (stored === "granted" && !window.dataLayer.__pydataGaConsentPatched) {
    var originalPush = window.dataLayer.push;
    window.dataLayer.push = function () {
      var filteredCommands = [];

      for (var index = 0; index < arguments.length; index += 1) {
        var command = arguments[index];
        var isPyDataDeniedDefault =
          command &&
          command[0] === "consent" &&
          command[1] === "default" &&
          command[2] &&
          command[2].analytics_storage === "denied";

        if (!isPyDataDeniedDefault) {
          filteredCommands.push(command);
        }
      }

      if (!filteredCommands.length) {
        return window.dataLayer.length;
      }

      return originalPush.apply(window.dataLayer, filteredCommands);
    };
    window.dataLayer.__pydataGaConsentPatched = true;
  }

  window.gtag = window.gtag || function () {
    window.dataLayer.push(arguments);
  };

  window.gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: stored === "granted" ? "granted" : "denied"
  });
}());
"""
    return script.replace("__CONFIG_JSON__", config_json).strip()


def _add_assets(app: Sphinx) -> None:
    if app.builder.format != "html":
        return

    app.add_js_file(None, body=_early_consent_script(app), priority=1)
    app.add_css_file("ga_consent.css", priority=900)
    app.add_js_file("ga_consent.js", defer="defer", priority=900)


def _copy_assets(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or app.builder.format != "html":
        return

    copy_asset(str(STATIC_DIR), str(Path(app.outdir) / "_static"), force=True)


def setup(app: Sphinx) -> dict[str, object]:
    app.add_config_value("ga_consent_storage_key", "pydata_ga_consent", "html")
    app.add_config_value(
        "ga_consent_banner_text",
        "We use Google Analytics to understand how visitors use these open lessons. Accepting analytics helps us evaluate their reach and plan future lesson development. You can accept or decline analytics cookies.",
        "html",
    )
    app.add_config_value("ga_consent_accept_text", "Accept analytics", "html")
    app.add_config_value("ga_consent_decline_text", "Decline", "html")
    app.add_config_value("ga_consent_privacy_url", "", "html")
    app.add_config_value("ga_consent_privacy_text", "Privacy details", "html")

    app.connect("builder-inited", _add_assets)
    app.connect("build-finished", _copy_assets)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": "0.1.0",
    }
