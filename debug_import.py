import sys
import traceback

print("Attempting to import my_model...")
try:
    import my_model
    print("✅ SUCCESS: Module imported")
    
    # Check what's available
    attrs = dir(my_model)
    public_attrs = [x for x in attrs if not x.startswith('_')]
    print(f"\nTotal public attributes: {len(public_attrs)}")
    
    # Check for our function
    if hasattr(my_model, 'run_stage1_assessment'):
        print("✅ run_stage1_assessment found!")
    else:
        print("❌ run_stage1_assessment NOT found")
        
    # Print first 20 attributes
    print("\nPublic attributes:")
    for attr in sorted(public_attrs)[:20]:
        obj = getattr(my_model, attr)
        if callable(obj):
            print(f"  - {attr} (function)")
        else:
            print(f"  - {attr} ({type(obj).__name__})")
            
except Exception as e:
    print(f"❌ ERROR during import: {e}")
    traceback.print_exc()
