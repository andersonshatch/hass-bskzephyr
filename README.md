# BSK Zephyr Home Assistant integration

## Important notes
1. Unofficial integration using an undocumented API. May break at any time.
1. Only works for [BSK Zephyr v2](https://www.bskhvac.com.tr/en/product-detail/heat-recovery-units/zephyr-decentrelized-heat-recovery-device) devices registered in the BSK Connect app. If you are using the BSK Zephyr app, download BSK Connect, login with your existing account and register your device in BSK Connect.
1. Works only with username and password. If you used Apple or Google login, create a new account with username and password and re-register your device / share it from your other account.

## Requirements
- Home Assistant version 2025.2 or newer
- [HACS](https://hacs.xyz/) installed

## Installation

### With My Home Assistant
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andersonshatch&repository=hass-bskzephyr&category=integration)
1. Click the button above to add this repo as a custom HACS repo, confirming by pressing Add
1. Press Download to add the integration

### Manually in HACS
1. Navigate to HACS and add a custom repo ([steps](https://hacs.xyz/docs/faq/custom_repositories)) using repository: `andersonshatch/hass-bskzephyr`, type: `integration`
2. Select the BSK Zephyr Connect integration which should appear under the New section
3. Press Download to add the integration

## Setup
1. Navigate to Settings -> Devices & Services and press Add Integration
2. Search for `BSK Zephyr`
1. Enter your username and password and press Submit

## Entities
This integration generates the following entities for each supported device:
- Sensors for temperature, humidity, filter and capsule status
- Selects for speed and mode
- Switch for power
- Number to control humidity boost (100% = humidity boost off)

## Example dashboard

<img width="481" alt="image" src="https://github.com/user-attachments/assets/98615435-5192-4581-b76a-a38e4556cf65" />

Using [custom button card](https://github.com/custom-cards/button-card)

<details>
  <summary>Lovelace YAML</summary>

```yaml
type: horizontal-stack
cards:
  - type: custom:button-card
    show_state: true
    show_name: false
    entity: switch.kitchen_power
    state:
      - value: "off"
        color: white
        icon: mdi:fan-off
      - value: "on"
        spin: true
        color: white
        icon: mdi:fan
  - type: custom:button-card
    name: Night
    entity: select.kitchen_fan_speed
    icon: mdi:weather-night
    state:
      - value: night
        color: green
    tap_action:
      action: call-service
      service: select.select_option
      data:
        entity_id: select.kitchen_fan_speed
        option: night
  - type: custom:button-card
    name: Low
    entity: select.kitchen_fan_speed
    icon: mdi:fan-speed-1
    state:
      - value: low
        color: green
    tap_action:
      action: call-service
      service: select.select_option
      data:
        entity_id: select.kitchen_fan_speed
        option: low
  - type: custom:button-card
    name: Medium
    entity: select.kitchen_fan_speed
    icon: mdi:fan-speed-2
    state:
      - value: medium
        color: green
    tap_action:
      action: call-service
      service: select.select_option
      data:
        entity_id: select.kitchen_fan_speed
        option: medium
  - type: custom:button-card
    name: High
    entity: select.kitchen_fan_speed
    icon: mdi:fan-speed-3
    state:
      - value: high
        color: green
    tap_action:
      action: call-service
      service: select.select_option
      data:
        entity_id: select.kitchen_fan_speed
        option: high
```
</details>
