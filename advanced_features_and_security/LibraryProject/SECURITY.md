# Security Measures for HTTPS and Secure Redirects in Django

## Overview

This document explains the security settings implemented in the Django project to enforce HTTPS, protect cookies, and add HTTP security headers to enhance the overall security of the application.

---

## HTTPS Enforcement

- **SECURE_SSL_REDIRECT = True**  
  Redirects all incoming HTTP requests to HTTPS to ensure encrypted communication between client and server.

- **HTTP Strict Transport Security (HSTS)**  
  - `SECURE_HSTS_SECONDS = 31536000` (1 year)  
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`  
  - `SECURE_HSTS_PRELOAD = True`  
  These settings instruct browsers to always use HTTPS for this domain and its subdomains, and allow inclusion in browser preload lists.

---

## Secure Cookies

- **SESSION_COOKIE_SECURE = True**  
- **CSRF_COOKIE_SECURE = True**  
These ensure that session and CSRF cookies are only sent over secure HTTPS connections, protecting against cookie interception.

---

## HTTP Security Headers

- **X_FRAME_OPTIONS = "DENY"**  
  Prevents the site from being embedded in frames, protecting against clickjacking attacks.

- **SECURE_CONTENT_TYPE_NOSNIFF = True**  
  Stops browsers from MIME-sniffing a response away from the declared content-type, which helps prevent attacks based on content-type confusion.

- **SECURE_BROWSER_XSS_FILTER = True**  
  Enables the browser's built-in cross-site scripting (XSS) filter, helping to mitigate XSS attacks.

---

## Deployment Notes

- Ensure your web server (e.g., Nginx, Apache) is configured to serve your Django app over HTTPS using valid SSL/TLS certificates.
- Redirect HTTP traffic to HTTPS at the web server level as well for redundancy.
- Remember to set `DEBUG = False` in production to avoid exposing sensitive information.
- Monitor security headers and use tools like [Mozilla Observatory](https://observatory.mozilla.org/) to verify your security setup.

---

## Testing

- Manually test by accessing your site via HTTP and confirm it redirects to HTTPS.
- Verify that cookies have the `Secure` attribute set.
- Use browser dev tools to inspect HTTP response headers to confirm security headers are present.

---

## References

- [Django Security Middleware](https://docs.djangoproject.com/en/stable/topics/security/#security-middleware)
- [Mozilla HTTP Observatory](https://observatory.mozilla.org/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

---

*Document last updated: 2025-07-27*
