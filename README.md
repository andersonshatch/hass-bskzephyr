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
