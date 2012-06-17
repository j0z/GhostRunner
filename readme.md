Ghost Runner - readme
=====================

Current Version: 06.17.2012
---------------------------
Changed
-------
* Added on_ground flag to character
* Rewrote collision logic

Previous Version: 06.16.2012
---------------------------
Changed
-------
* Fixed sprite drawing off-center
* somber.bind_key(key,function) - Binds a key to a callback function
* somber.add_sprite(file) - Internal use only (used by somber.get_sprite())
* somber.get_sprite(file) - Searches sprite cache for image, returns surface if found (else: creates and caches)
* somber.set_background(file) - Draws 'file' to background surface and blits to screen
* Added automatic sprite caching
* Collisions