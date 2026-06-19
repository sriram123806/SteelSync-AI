import band
import inspect

for name in ["Agent", "AgentRuntime", "BandLink", "ExecutionContext"]:
    print(f"\n===== {name} =====")

    obj = getattr(band, name, None)

    if obj is None:
        print("NOT FOUND")
        continue

    print("Module:", obj.__module__)

    print("\nMethods:")
    for item in dir(obj):
        if not item.startswith("_"):
            print(item)