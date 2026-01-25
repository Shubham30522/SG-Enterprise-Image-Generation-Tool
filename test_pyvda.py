
from pyvda import AppView, VirtualDesktop

def test_silent_desktop():
    print("Getting current desktop...")
    current = VirtualDesktop.current()
    print(f"Current Desktop: {current.number}")

    print("Creating new desktop...")
    # VirtualDesktop.create() typically creates it. 
    # Does it switch? Let's verify by checking current after create.
    new_desktop = VirtualDesktop.create()
    print(f"New Desktop Created: {new_desktop.number}")
    
    import time
    time.sleep(1)
    
    print("Checking where we are...")
    now_current = VirtualDesktop.current()
    print(f"Current Desktop is now: {now_current.number}")
    
    if now_current.number == current.number:
        print("SUCCESS: Did not switch!")
    else:
        print("FAILURE: Switched to new desktop.")
        # Switch back for sanity
        current.go()

if __name__ == "__main__":
    test_silent_desktop()
