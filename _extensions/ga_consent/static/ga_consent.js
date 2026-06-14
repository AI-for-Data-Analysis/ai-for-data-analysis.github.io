(function () {
  "use strict";

  var config = window.PYDATA_GA_CONSENT || {};
  var storageKey = config.storageKey || "pydata_ga_consent";
  var storedConsent = getStoredConsent();

  if (storedConsent === "granted") {
    updateAnalyticsConsent("granted");
    return;
  }

  if (storedConsent === "denied") {
    updateAnalyticsConsent("denied");
    return;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showBanner);
  } else {
    showBanner();
  }

  function getStoredConsent() {
    try {
      return window.localStorage.getItem(storageKey);
    } catch (error) {
      return null;
    }
  }

  function setStoredConsent(value) {
    try {
      window.localStorage.setItem(storageKey, value);
    } catch (error) {
      return;
    }
  }

  function updateAnalyticsConsent(value) {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {
        analytics_storage: value,
      });
    }
  }

  function sendAcceptedPageView() {
    if (typeof window.gtag !== "function") {
      return;
    }

    window.gtag("event", "page_view", {
      page_title: document.title,
      page_location: window.location.href,
      page_path: window.location.pathname + window.location.search,
    });
  }

  function showBanner() {
    if (document.querySelector("[data-ga-consent-banner]")) {
      return;
    }

    var banner = document.createElement("section");
    banner.className = "ga-consent-banner";
    banner.setAttribute("data-ga-consent-banner", "");
    banner.setAttribute("aria-label", "Analytics consent");

    var message = document.createElement("p");
    message.className = "ga-consent-banner__message";
    message.textContent =
      config.bannerText ||
      "This site uses Google Analytics to understand lesson usage. You can accept or decline analytics cookies.";

    if (config.privacyUrl) {
      message.appendChild(document.createTextNode(" "));
      var privacyLink = document.createElement("a");
      privacyLink.href = config.privacyUrl;
      privacyLink.textContent = config.privacyText || "Privacy details";
      message.appendChild(privacyLink);
    }

    var actions = document.createElement("div");
    actions.className = "ga-consent-banner__actions";

    var declineButton = document.createElement("button");
    declineButton.type = "button";
    declineButton.className =
      "btn btn-sm btn-outline-secondary ga-consent-banner__button";
    declineButton.textContent = config.declineText || "Decline";
    declineButton.addEventListener("click", function () {
      setStoredConsent("denied");
      updateAnalyticsConsent("denied");
      dismissBanner(banner);
    });

    var acceptButton = document.createElement("button");
    acceptButton.type = "button";
    acceptButton.className = "btn btn-sm btn-primary ga-consent-banner__button";
    acceptButton.textContent = config.acceptText || "Accept analytics";
    acceptButton.addEventListener("click", function () {
      setStoredConsent("granted");
      updateAnalyticsConsent("granted");
      sendAcceptedPageView();
      dismissBanner(banner);
    });

    actions.appendChild(declineButton);
    actions.appendChild(acceptButton);
    banner.appendChild(message);
    banner.appendChild(actions);
    document.body.appendChild(banner);
  }

  function dismissBanner(banner) {
    banner.setAttribute("hidden", "");
    banner.remove();
  }
})();
