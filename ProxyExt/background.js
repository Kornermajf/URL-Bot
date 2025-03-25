chrome.proxy.settings.set(
  {
    value: {
      mode: "pac_script",
      pacScript: {
        data: `
          function FindProxyForURL(url, host) {
            var auth = "PROXY USER:PASS@HOST:PORT";

            if (
              dnsDomainIs(host, "google-analytics.com") ||
              dnsDomainIs(host, "analytics.google.com")
            ) {
              return auth;
            }
            return "DIRECT";
          }
        `,
      },
    },
    scope: "regular",
  },
  function () {
    console.log("Proxy settings applied");
  }
);
