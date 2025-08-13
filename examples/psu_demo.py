from __future__ import annotations


from devices.psu import PSU, VirtualPsuStrategy
from devices.psu.yaml_config_loader import YamlPSUConfigLoader
from adapters.psu import SimAdapter
def main() -> None:
    loader = YamlPSUConfigLoader()  # defaults to the psu module directory
    psu = PSU(model="RIGOL-DP832", adapter=SimAdapter(), config_loader=loader, strategy=VirtualPsuStrategy())

    psu.connect()
    print("Capabilities:", psu.get_capabilities())

    psu.set("voltage", 5.0)
    psu.set("current_limit", 0.2)
    psu.set("output", True)

    v = psu.read("voltage")
    i = psu.read("current")
    t = psu.read("temp")
    print(f"Measured: V={v:.3f}V, I={i:.3f}A, T={t:.1f}C, OUT={psu.read('output')}")

    # Demonstrate power cycle
    psu.set("power_cycle", None)
    print("After cycle, OUT=", psu.read("output"))

    psu.disconnect()


if __name__ == "__main__":
    main()
