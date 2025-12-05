from spherov2.toy.r2d2 import R2D2

print("Some Audio options:")
for a in list(R2D2.Audio)[:30]:  # first 30 entries
    print(a.name, a.value)

print("\nSome Animation options:")
for anim in list(R2D2.Animations):
    print(anim.name, anim.value)
from spherov2.toy.r2d2 import R2D2
import spherov2

print("R2D2 attributes:")
print([x for x in dir(R2D2) if "play" in x.lower()])

print("\nSearching for PlaybackMode in module:")
for name in dir(spherov2):
    if "play" in name.lower():
        print(" -", name)

print("\nChecking IO class:")
from spherov2.sphero_edu import IO
print([x for x in dir(IO) if "play" in x.lower()])
