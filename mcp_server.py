from fastmcp import FastMCP
import json

mcp = FastMCP(name="OmniRelayEnterpriseMCP")

UPSTREAM_DISTRIBUTOR_DB = {
    "SKU-PWR-65W": {"name": "65W GaN Fast Charger", "rdc_units": 3500, "unit_price": 24.50, "lead_time_hrs": 2},
    "SKU-ANC-HEADSET": {"name": "Wireless ANC Headphones", "rdc_units": 1200, "unit_price": 89.00, "lead_time_hrs": 3},
    "SKU-SSD-1TB": {"name": "NVMe 1TB External SSD", "rdc_units": 450, "unit_price": 110.00, "lead_time_hrs": 4}
}

MICRO_HUB_DB = {
    "HUB-DOWNTOWN-01": {
        "SKU-PWR-65W": {"stock": 3, "min_threshold": 20, "burn_rate_hr": 4.5},
        "SKU-ANC-HEADSET": {"stock": 1, "min_threshold": 10, "burn_rate_hr": 2.0}
    },
    "HUB-METRO-EAST": {
        "SKU-SSD-1TB": {"stock": 0, "min_threshold": 5, "burn_rate_hr": 1.2}
    }
}

@mcp.tool()
def check_microhub_inventory(hub_id: str, sku_id: str) -> str:
    """Inspects real-time inventory and calculates stockout risk at an urban micro-hub."""
    hub = MICRO_HUB_DB.get(hub_id.upper(), {})
    item = hub.get(sku_id.upper())
    if not item:
        return json.dumps({"error": f"Item {sku_id} is not mapped to {hub_id}"})
    
    hours_remaining = round(item["stock"] / max(item["burn_rate_hr"], 0.1), 1)
    return json.dumps({
        "hub_id": hub_id.upper(),
        "sku": sku_id.upper(),
        "current_stock": item["stock"],
        "min_safe_threshold": item["min_threshold"],
        "hours_to_stockout": hours_remaining,
        "critical_alert": item["stock"] < item["min_threshold"]
    })

@mcp.tool()
def query_upstream_wholesaler(sku_id: str) -> str:
    """Queries central wholesale distributor inventory and pricing."""
    item = UPSTREAM_DISTRIBUTOR_DB.get(sku_id.upper())
    if not item:
        return json.dumps({"error": f"SKU {sku_id} not available in wholesale catalog"})
    return json.dumps({"sku": sku_id.upper(), "details": item})

@mcp.tool()
def dispatch_transfer_order(hub_id: str, sku_id: str, quantity: int) -> str:
    """Commits rapid intra-city stock transfer from upstream distributor to local micro-hub."""
    transfer_id = f"TRF-{hub_id[-4:]}-{sku_id[:6]}-AUTO"
    return json.dumps({
        "status": "DISPATCH_COMMITTED",
        "transfer_id": transfer_id,
        "destination_hub": hub_id.upper(),
        "sku": sku_id.upper(),
        "units_dispatched": quantity,
        "telematics_eta": "35 mins"
    })

if __name__ == "__main__":
    mcp.run()
