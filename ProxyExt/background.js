chrome.proxy.settings.set(
  {
    value: {
      mode: "pac_script",
      pacScript: {
        data: `
          function FindProxyForURL(url, host) {
            var auth = "PROXY username:password@your.proxy.com:port; DIRECT";
            var auth2 = "PROXY 127.0.0.1:8583";

            if (
              dnsDomainIs(host, "google-analytics.com") ||
              dnsDomainIs(host, "analytics.google.com")
            ) {
              return auth2;
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
