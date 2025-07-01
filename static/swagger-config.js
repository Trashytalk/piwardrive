window.onload = () => {
  window.ui = SwaggerUIBundle({
    url: "/openapi.json",
    dom_id: "#swagger-ui",
    presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
    layout: "BaseLayout",
    docExpansion: "none",
    validatorUrl: null,
    oauth2RedirectUrl: window.location.origin + "/docs/oauth2-redirect",
  });
};
