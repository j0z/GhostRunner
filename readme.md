Ghost Runner - readme
=====================

Current Version: 06.16.2012
---------------------------
Changed
-------
* somber.bind_key(key,function) - Binds a key to a callback function
* somber.add_sprite(file) - Internal use only (used by somber.get_sprite())
* somber.get_sprite(file) - Searches sprite cache for image, returns surface if found (else: creates and caches)
* somber.set_background(file) - Draws 'file' to background surface and blits to screen
* Added automatic sprite caching
* Collisions