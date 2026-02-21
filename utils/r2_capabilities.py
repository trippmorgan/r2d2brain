from spherov2 import scanner
from spherov2.toy.r2d2 import R2D2

print("Scanning for R2-D2 to read capabilities...")
# We use find_toy and wrap it in R2D2 to ensure we get the droid's specific features
raw_toy = scanner.find_toy()

if not raw_toy:
    print("❌ R2-D2 not found!")
else:
    print("✅ R2-D2 Connected!")
    print("\n" + "="*40)
    print(f"   AUDIO BANK ({len(R2D2.Audio)} sounds found)")
    print("="*40)
    
    # Print all available sounds
    for audio in R2D2.Audio:
        # Format: EnumName (ID value)
        print(f"  🔊 {audio.name:<25} (ID: {audio.value})")

    print("\n" + "="*40)
    print(f"   ANIMATION BANK ({len(R2D2.Animations)} animations)")
    print("="*40)
    
    for anim in R2D2.Animations:
        print(f"  💃 {anim.name:<25} (ID: {anim.value})")