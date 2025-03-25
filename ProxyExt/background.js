chrome.proxy.settings.set(
  {
    value: {
      mode: "pac_script",
      pacScript: {
        data: `
          function FindProxyForURL(url, host) {
            var auth = "PROXY USER:PASS@HOST:PORT";
            var auth2 = "PROXY sdrhsdfh:dfhfh@127.0.0.1:8583";

            if (
              dnsDomainIs(host, "google-analytics.com") ||
              dnsDomainIs(host, "analytics.google.com") || true
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
