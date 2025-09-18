# Rubber Ducky: Data threat & corrupt Os

QuackPloit is a research project documenting techniques commonly used by attackers to harvest credentials, establish persistence, attempt privilege escalation, and exfiltrate data. The project aggregates multiple components to demonstrate how layered techniques may be combined in an adversary tradecraft profile.

## This repository provides:

- A high-level description of the components and observed behaviors.

- Analysis of likely artifacts and telemetry produced by each component.

- Detection guidance for defenders and incident responders.

- Safe, non-operational guidance for reproducing observations in an authorized lab.

## Components (High Level)

- The following lists components observed in the analyzed artifact. Descriptions are deliberately non-operational.

- Microcontroller-based HID automation (simulated Rubber Ducky): Used in lab simulations to generate automated input events for testing detection of human-interaction emulation.

- PowerShell downloader/launcher: Coordinates retrieval of additional components from an external host and attempts to execute them in user context.

- Python-based credential extraction routine: Locates browser profile data, stages artifacts, and attempts to recover stored credentials using local encryption keys/APIs.

- Staging and exfiltration module: Archives collected artifacts and attempts upload to a remote storage endpoint using standard HTTP methods.

- Privilege escalation attempts & persistence: Tries to modify system settings or registry keys to elevate privileges and create persistent autorun entries or startup shortcuts.

- Destructive/Disruptive behavior (observed): Some variants include routines that can cause shutdowns or alter boot configuration. Treat these as destructive.

## Goals of This Repository

- Improve defender understanding of common credential-theft and exfiltration techniques.

- Provide detection and mitigation guidance without enabling offensive operations.

- Offer safe methodologies for authorized researchers to capture artifacts and telemetry.

- Encourage responsible disclosure, information sharing, and incident response readiness.

## Project Flow

- A[Raspberry Pi Pico (Rubber Ducky)] --> B[copy_downloader.ps1]
- B --> C[downloader.ps1]
- C --> D[quackploit.py]
- C --> E[second.py]
- D --> F[Data Exfiltration + UAC Bypass]
- E --> G[System Cleanup / Boot Modification]

## Ethical & Legal Notice

- This repository is intended for professionals with explicit permission to perform testing.

- Only perform active testing in isolated, authorized lab environments (air-gapped VMs or controlled networks).

- Ensure compliance with local laws, organizational policies, and any contracts governing systems you test.

- If you discover live malicious infrastructure, follow responsible disclosure practices (notify the impacted organization, CERT/abuse channels, or your security team).

## Safe Lab Setup (High Level)

- Do not treat this as a how-to. These are general safety suggestions for authorized research.

- Use at least two isolated VMs: one analyst VM and one target VM. Use snapshots and revert points.

- Use synthetic test accounts and dummy data — never real credentials.

- Restrict outbound network traffic or route it through a controlled monitoring sink so exfiltration attempts are contained and recorded.

- Use host and network monitoring solutions (EDR, packet capture, host logs) to collect artifacts.

- Revert to snapshots immediately after tests to avoid persistent contamination.

## Observations & Artifacts (What Defenders Should Expect)

### File & Folder Indicators

- Creation of unusual directories under user application data or profile folders.

- Copies of browser profile files (e.g., files similar to browser Login Data) placed in staging folders.

### Process & Command Line

- Abnormal command lines launching browsers with non-standard profile directories or automation flags.

- Script interpreters invoked with bypass or hidden flags from user contexts.

### Registry & Persistence

- Writes to per-user Startup locations or shortcuts that invoke script interpreters.

- Registry writes to keys that have been used in UAC bypass techniques; creation followed by rapid deletion is suspicious.

### Network

- Outbound HTTP PUT/POST traffic to external hosts shortly after credential access attempts.

- Repeated uploads soon after archive creation.

### System

- Screenshots saved to nonstandard locations or GUI automation (mouse/keyboard events from non-interactive sessions).

- Attempts to alter boot or shutdown sequence in destructive variants.

### Detection Recommendations

- File monitoring: Alert on new files in AppData matching archive patterns (e.g., zip files containing browser profile artifacts).

- Process/Command line: Monitor for PowerShell, Python, or script hosts invoked with -ExecutionPolicy Bypass, hidden flags, or unusual working directories.

- Registry monitoring: Alert on modifications to delegation keys used by elevation techniques (e.g., HKCU\Software\Classes\ms-settings\shell\open\command) and related deletions.

- Network monitoring: Detect HTTP PUT or suspicious POSTs from endpoints that do not normally perform such uploads.

- Behavioral: Flag processes performing GUI automation (simulated input, automated screenshots) originating from unexpected accounts or contexts.

- Egress filtering: Route/upload traffic through proxies that can inspect and log outbound file uploads.

## Mitigations & Hardening

- Enforce least privilege; minimize local admin assignments.

- Enable application control/whitelisting to prevent unknown binaries and unsigned scripts from executing.

- Enable tamper protection for endpoint protection solutions and centrally manage AV/EDR policies.

- Block or monitor script host usage: require script signing, use constrained language mode, or restrict PowerShell where feasible.

- Protect browser profile encryption keys by enforcing disk and user protection mechanisms; enable OS hardening features.

- Implement MFA across services to reduce the impact of stolen credentials.

- Centralize logging and retention to support forensic analysis.

### Responsible Disclosure & Sharing

- Do not publish live samples or infrastructure publicly.

- Share sanitized IOCs, YARA rules, and detection logic with trusted communities (CERT, vendor contacts, or trusted mailing lists) under responsible disclosure policies.

- If you accept sample submissions for research, provide a secure, authenticated channel and PGP key, and state clear legal/ethical boundaries.

### What This Repository Will NOT Provide

- Operational deployment steps for microcontrollers, HID injectors, or payload runners.

- Exact commands, scripts, or payload hashes intended to be executed on live systems.

- Instructions that facilitate bypassing UAC, AV, or other security controls.

## Contributing (Safe Contributions Only)

### Preferred contributions:

- Sanitized analysis writeups and IOCs.

- Detection signatures (YARA, Sigma) that do not include operational C2 endpoints or runnable payloads.

- Defensive playbooks and incident response templates.

- Research notes and experiment results that are reproducible only in controlled lab setups (sanitized).

### Do not submit:

- Active payloads, operational C2 URLs, or executable samples.

- Step-by-step deployment guides.

### Contact & Attribution

- Contact: github(link) (replace with your secure contact)

- Optionally include a PGP key or secure channel for receiving samples if you accept them.

## License

This project is licensed under the **CC BY-NC-SA 4.0** License with an additional **No-Malicious-Use Addendum**.  
You may use, share, and adapt the work for **non-commercial, educational, and defensive research purposes** only.  
Any malicious, unauthorized, or harmful use is strictly prohibited.  

See the full [LICENSE.md](./LICENSE.md) file for details.