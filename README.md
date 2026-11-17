# Xbox Reward Hunter Phase 2 — iPhone + GitHub Pages

This is a **public RSS discovery dashboard**, not a gift-card code generator, automatic redemption system, or guarantee that any listed opportunity is active. No Microsoft account credentials are collected.

## iPhone-only setup

1. Sign in to [github.com](https://github.com) in Safari and create a **public** repository named `xbox-reward-hunter` (GitHub Pages on public repositories is available on GitHub Free). Do not upload personal data.
2. Upload the contents of this ZIP **preserving folders** (`hunter.py`, `docs/index.html`, `docs/offers.json`, `.github/workflows/scan.yml`, and this README) to the repository. On iPhone, GitHub's web uploader may not preserve folders from a ZIP automatically; extract it in the Files app and use GitHub's web editor to create nested files by their exact paths if necessary. The `.github` folder is essential.
3. In repository **Settings → Pages**, set **Build and deployment → Deploy from a branch**, branch `main`, folder `/docs`, then Save.
4. In **Settings → Actions → General**, under Workflow permissions, enable **Read and write permissions** if needed for the scan workflow to commit updates. Repository/organization policies may restrict this.
5. Open **Actions → Scan public Xbox reward leads → Run workflow**. Wait for the run to finish; RSS services can occasionally be unavailable.
6. Visit `https://YOUR_GITHUB_USERNAME.github.io/xbox-reward-hunter/` in Safari. Replace the username with your own. Use Share → Add to Home Screen to make it feel like an app.

The workflow attempts a scan every six hours (GitHub schedules are best-effort and can be delayed or disabled for inactive repositories). You can run a manual scan anytime. It may take several minutes for GitHub Pages to publish updated data. There is no push notification feature in this version.

## Classification limits

Google News RSS search results are **leads**, not proof of active or valid offers. An `Official-source lead` classification is based on the RSS source label and is **not authenticated**. Review the destination and campaign terms yourself. No codes are guessed, generated, or tested against Microsoft.

## Local test

Run `python hunter.py` from the project root; then serve `docs` with `python -m http.server 8000 --directory docs` and open `http://localhost:8000`. Requires network access to RSS feeds.
