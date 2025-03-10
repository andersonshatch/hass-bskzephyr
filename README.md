# BSK Zephyr Home Assistant integration

## Important notes
1. Unofficial integration using an undocumented API. May break at any time.
1. Only works for BSK Zephyr v2 devices registered in the BSK Connect app. If you are using the BSK Zephyr app, download BSK Connect, login with your existing account and register your device in BSK Connect.
1. Works only with username and password. If you used Apple or Google login, create a new account with username and password and re-register your device / share it from your other account.

## Installation
1. Add a Custom Repository to HACS ([steps](https://hacs.xyz/docs/faq/custom_repositories)) - repository: `andersonshatch/hass-bskzephyr`, type: `integration`,
1. Restart home-assistant
1. Go to Settings -> Devices & Services and press Add Integration
1. Search for `BSK Zephyr`
1. Enter your username and password
