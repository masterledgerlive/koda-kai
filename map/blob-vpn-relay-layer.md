# Blob VPN relay layer — plugin for this map

**Status: AVAILABLE — first relay live.** Tagged release:
`blob-vpn-gods-eye-plugin-v1`

The Blob VPN network (a VPN that answers with receipts — living directory on
Sui testnet, state in Walrus blobs, sealed private entries) publishes a live
relay feed that this globe can render as a layer:

- **Feed (GeoJSON, CORS-open):**
  https://arcade.highscores.live/arcade/blob-vpn/relays.geojson
- **Spec + generator:** https://github.com/masterledgerlive/blob-vpn/tree/main/plugin/gods-eye
- **Project page (live network panel):** https://arcade.highscores.live/arcade/blob-vpn.html
- **Code (MIT):** https://github.com/masterledgerlive/blob-vpn

## How the layer works

Each feature is one enrolled relay directory:

| property | meaning |
|---|---|
| `label` | relay's chosen name |
| `directory` | Sui testnet Directory object id |
| `head_blob` | current head blob id (Walrus) — the living state |
| `head_epoch` | Walrus epoch the head is paid through |
| `advances` | pointer advances — the relay's life sign |
| `status` | `live` when the head read back from the aggregator at generation time, else `unverified` |

Map it like the history feed: lat/lon from geometry, weight `1.0` when
`status == "live"` else `0.5`, description carries `head_blob`, `directory`,
`advances`. A relay whose head stops verifying renders **dimmed, not
deleted** — on this network, silence is data.

## First pin

**Kodakai Relay 001 — network root**, Clearwater, FL.
Directory `0xc1bf9f6a67a556d5e8f18f2e9bdb03ada54521329ee1cd06d2875eb577e54850`,
head `mGv9byIa_0DKXamS3tox-A8UL7U6yhcEj6Y9ZBn5wck` (epoch 567) at tag time.

## Adding a relay

Run the relay kit from the blob-vpn repo (`relay-kit/blob-relay.mjs watch /
heartbeat / enroll`), then add the directory to
`plugin/gods-eye/directories.json` there by pull request and regenerate the
feed with `make-feed.mjs`.

Honest scope: this is a **testnet coordination layer** — directories and
heartbeats are real on-chain actions; no production VPN traffic flows yet,
and the public launch is gated on legal review. No token, no coin.
