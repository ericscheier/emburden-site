# Security policy

## Reporting a vulnerability

Please report security vulnerabilities privately to
`security@emrgi.org`. Do **not** open a public issue for security
problems.

Include:

- Affected project and version.
- Vulnerability class (e.g. auth bypass, data exposure, RCE,
  insecure default).
- Minimal reproducer or proof-of-concept.
- Your contact for follow-up.

## Response commitment

- **Acknowledgement**: within 5 business days of receipt.
- **Plan of action**: within 15 business days.
- **Coordinated disclosure**: we will work with you on a
  disclosure timeline, typically 90 days from acknowledgement or
  when a fix is available, whichever is earlier.

## Supported versions

For each Foundation project, security fixes are backported to:

- The current `main` branch (always).
- The most recent tagged minor release (typically).
- Older minor releases only when a critical vulnerability affects
  a broad user base and back-porting is feasible.

## Scope

Foundation projects are open-source research and analysis tools;
most do not process untrusted network input or user credentials
directly. Common in-scope issues:

- Unsafe deserialization of cached data.
- Path traversal in cache-writing functions.
- Insecure defaults that leak private data (e.g., API keys in
  cache paths or logs).
- Dependency vulnerabilities that propagate to Foundation code.

Out of scope: bugs in third-party data sources or upstream
dependencies (report those to the respective upstream).

## Attribution

Reporters who follow this policy are credited in the project's
release notes and offered ORCID linkage in the `AUTHORS.md` file,
unless they prefer to remain anonymous.
